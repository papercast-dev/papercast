from papercast.base import BaseProcessor, BaseSubscriber, BasePipelineComponent
from papercast.production import Production
from typing import Iterable, Dict, Any
from collections import defaultdict
import asyncio
from concurrent.futures import ThreadPoolExecutor


class Pipeline:
    def __init__(self, name: str):
        self.name = name
        self.connections = defaultdict(list)
        self.processors = {}
        self.collectors = {}
        self.subscribers = {}
        self.downstream_processors = {}
        self.executor = ThreadPoolExecutor()

    def _validate_name(self, name: str):
        if name in [p.name for p in self.processors.values()]:
            raise ValueError(f"Processor with name {name} already exists")

    def add_processor(self, name: str, processor: BasePipelineComponent):
        self._validate_name(name)
        setattr(processor, "name", name)

        self.processors[name] = processor

        if isinstance(processor, BaseProcessor):
            self.collectors[name] = processor

        elif isinstance(processor, BaseSubscriber):
            self.subscribers[name] = processor

        else:
            self.downstream_processors[name] = processor

    def connect(self, a_name: str, a_output: str, b_name: str, b_input: str):
        a_type = self.processors[a_name].output_types[a_output]
        b_type = self.processors[b_name].input_types[b_input]

        if not a_type == b_type:
            raise TypeError(
                f"Cannot connect {a_output} of {a_name} with type {a_type} to {b_input} of {b_name} with type {b_type}"
            )

        self.connections[a_name].append((a_output, b_name, b_input))

    def _topological_sort(self, processor_names: Iterable[str]) -> Iterable[str]:
        visited = set()
        sorted_processors = []

        def visit(processor_name: str):
            if processor_name not in visited:
                visited.add(processor_name)
                for _, next_processor_name, _ in self.connections[processor_name]:
                    visit(next_processor_name)
                sorted_processors.append(processor_name)

        for processor_name in processor_names:
            if not isinstance(processor_name, str):
                raise ValueError(f"Processor {processor_name} has no name")
            visit(processor_name)

        return sorted_processors[::-1]

    @property
    def input_types(self) -> Dict[str, Any]:
        input_types = {}
        for processor in self.collectors.values():
            input_types.update(processor.input_types)
        return input_types

    def _validate_run_kwargs(self, kwargs):
        input_kwargs = {k: v for k, v in kwargs.items() if k in self.input_types}
        options_kwargs = {k: v for k, v in kwargs.items() if k not in self.input_types}

        if len(input_kwargs) != 1:
            raise ValueError(
                f"Expected exactly one input argument, got {len(input_kwargs)}: {input_kwargs}"
            )

        input_key = list(input_kwargs.keys())[0]
        input_value = list(input_kwargs.values())[0]

        collector = [
            tuple(c) for c in self.collectors.items() if input_key in c[1].input_types
        ][0]

        return collector[0], collector[1], input_key, input_value, options_kwargs

    def get_downstream_processors(
        self, collector_subscriber_name: str
    ) -> Iterable[str]:
        """Get all processors downstream of the collector with name `collector_name`
        by recursively traversing the graph of connections.
        """
        downstream_processors = set()

        if not self.connections[collector_subscriber_name]:
            raise ValueError(
                f"Processor {collector_subscriber_name} is not connected to any downstream processors"
            )

        def visit(processor_name: str):
            if processor_name not in downstream_processors:
                downstream_processors.add(processor_name)
                for _, next_processor_name, _ in self.connections[processor_name]:
                    visit(next_processor_name)

        for _, downstream_processor, _ in self.connections[collector_subscriber_name]:
            visit(downstream_processor)

        return downstream_processors

    async def _run_subscriber(self, subscriber_name: str):
        subscriber = self.subscribers[subscriber_name]
        loop = asyncio.get_event_loop()
        processing_graph = self.get_downstream_processors(subscriber_name)
        sorted_processors = self._topological_sort(processing_graph)
        async for production in subscriber.subscribe():
            await loop.run_in_executor(
                None, self.process, production, sorted_processors
            )

    async def _run_in_server(self):
        await asyncio.gather(*[self._run_subscriber(name) for name in self.subscribers])

    def process(
        self, production: Production, collector_subscriber_name: str, **options
    ) -> None:
        """
        Run the pipeline synchronously on a production, from a collector or subscriber.
        """
        print(f"Processing production {production}...")
        processing_graph = self.get_downstream_processors(collector_subscriber_name)
        sorted_processors = self._topological_sort(processing_graph)
        for name in sorted_processors:
            print(f"Processing production {production} with {name}...")
            production = self.processors[name].process(production, **options)

    def run(self, **kwargs):
        """
        Run the pipeline synchronously, from kwargs.
        """
        (
            collector_name,
            collector,
            param,
            value,
            options,
        ) = self._validate_run_kwargs(kwargs)
        production = Production(**{param: value})
        production = collector.process(production, **options)
        self.process(production, collector_subscriber_name=collector_name, **options)
