import json
import inspect
import pytest
from papercast.base import BaseProcessor, BaseSubscriber, BasePipelineComponent
from papercast.production import Production
from papercast.pipelines import Pipeline


class MyCollector(BaseProcessor):
    input_types = {"some_input": str}
    output_types = {"collected": dict}

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    def process(self, production: Production, **options) -> Production:
        # do something with the input
        return Production(collected={"data": "example"})


class MyProcessor(BaseProcessor):
    input_types = {"collected": dict}
    output_types = {"processed": dict}

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    def process(self, production: Production, **options) -> Production:
        # do something with the input
        return Production(processed={"result": "success"})


class TestPipeline:
    @pytest.fixture
    def expected_dict(self):
        return {
            "name": "My Pipeline",
            "processors": {
                "My Collector": {
                    "type": "MyCollector",
                    "input_types": {"some_input": "str"},
                    "output_types": {"collected": "dict"},
                },
                "My Processor": {
                    "type": "MyProcessor",
                    "input_types": {"collected": "dict"},
                    "output_types": {"processed": "dict"},
                },
            },
            "connections": [
                {
                    "source": {"name": "My Collector", "output": "collected"},
                    "destination": {"name": "My Processor", "input": "collected"},
                }
            ],
        }

    def test_to_dict(self, expected_dict):
        pipeline = Pipeline("My Pipeline")

        collector = MyCollector("My Collector")
        processor = MyProcessor("My Processor")

        pipeline.add_processor(collector.name, collector)
        pipeline.add_processor(processor.name, processor)

        pipeline.connect(collector.name, "collected", processor.name, "collected")

        pipeline_dict = pipeline.to_dict()

        assert pipeline_dict == expected_dict

    def test_serialize(self, expected_dict):
        pipeline = Pipeline("My Pipeline")

        collector = MyCollector("My Collector")
        processor = MyProcessor("My Processor")

        pipeline.add_processor(collector.name, collector)
        pipeline.add_processor(processor.name, processor)

        pipeline.connect(collector.name, "collected", processor.name, "collected")

        pipeline_json = pipeline.serialize()

        expected_json = json.dumps(expected_dict, indent=4, default=str)

        assert pipeline_json == expected_json
