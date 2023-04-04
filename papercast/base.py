import logging
from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Dict

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

    @abstractmethod
    def process(self, input: Production, *args, **kwargs) -> Production:
        raise NotImplementedError



class BaseProcessor(BasePipelineComponent, ABC):
    def __init__(
        self,
    ) -> None:
        self.init_logger()
        self.name = None

    def init_logger(self, log_level: int = logging.INFO):
        self.logger = logging.getLogger(__name__)
        c_handler = logging.StreamHandler()
        c_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        c_handler.setLevel(log_level)
        c_handler.setFormatter(c_format)
        self.logger.addHandler(c_handler)

class BaseCollector(BasePipelineComponent, ABC):
    def __init__(
        self,
    ) -> None:
        pass

    def init_logger(self, log_level: int = logging.INFO):
        self.logger = logging.getLogger(__name__)
        c_handler = logging.StreamHandler()
        c_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        c_handler.setLevel(log_level)
        c_handler.setFormatter(c_format)
        self.logger.addHandler(c_handler)

    @abstractmethod
    def process(self, *args, **kwargs) -> Production:
        raise NotImplementedError


class BasePublisher(BasePipelineComponent, ABC):
    def __init__(
        self,
    ) -> None:
        pass

    def init_logger(self, log_level: int = logging.INFO):
        self.logger = logging.getLogger(__name__)
        c_handler = logging.StreamHandler()
        c_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        c_handler.setLevel(log_level)
        c_handler.setFormatter(c_format)
        self.logger.addHandler(c_handler)

    @abstractmethod
    def process(self, input: Production, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def input_types(self) -> Dict[str, Any]:
        pass
