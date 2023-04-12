import logging
from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Dict
import websockets
from websockets.client import connect
from typing import AsyncGenerator, AsyncIterable

from papercast.production import Production


class ValidationError(Exception):
    pass


def validate_inputs(func):
    @wraps(func)
    def wrapper(processor_instance, input_object):
        input_types = processor_instance.input_types
        for input_key in input_types:
            if not hasattr(input_object, input_key):
                raise ValidationError(
                    f"Input object is missing required attribute '{input_key}' for processor {processor_instance.__class__.__name__}"
                )

        return func(processor_instance, input_object)

    return wrapper


class BasePipelineComponent(ABC):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # cls.process = validate_inputs(cls.process) # type: ignore # TODO input validation

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return id(self) == id(other)

    def init_logger(self, log_level: int = logging.INFO):
        self.logger = logging.getLogger(__name__)
        c_handler = logging.StreamHandler()
        c_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        c_handler.setLevel(log_level)
        c_handler.setFormatter(c_format)
        self.logger.addHandler(c_handler)


class BaseProcessor(BasePipelineComponent, ABC):
    input_types: Dict[str, Any] = {}
    output_types: Dict[str, Any] = {}

    def __init__(
        self,
    ) -> None:
        self.init_logger()
        self.name = None

    @abstractmethod
    @validate_inputs
    def process(self, input: Production, *args, **kwargs) -> Production:
        raise NotImplementedError

    def from_kwargs(self, **kwargs):
        production = Production(**kwargs)
        return self.process(production)


class BaseSubscriber(BasePipelineComponent, ABC):
    def __init__(
        self,
    ) -> None:
        self.init_logger()

    @abstractmethod
    async def subscribe(self) -> Production:
        raise NotImplementedError


class BasePublisher(BasePipelineComponent, ABC):
    input_types: Dict[str, Any] = {}

    def __init__(
        self,
    ) -> None:
        pass

    @abstractmethod
    def process(self, input: Production, *args, **kwargs) -> None:
        raise NotImplementedError

    def from_kwargs(self, **kwargs):
        production = Production(**kwargs)
        return self.process(production)
