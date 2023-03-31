from dataclasses import dataclass


@dataclass
class Production:

    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)