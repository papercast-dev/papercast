import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from papercast.plugin_utils import load_plugins
from papercast.subscribers import *  # type: ignore
from papercast.types_plugins import *

_installed_plugins = load_plugins("types")

for name, plugin in _installed_plugins.items():
    globals()[name] = plugin

PathLike = Union[str, Path]

@dataclass
class TxtFile:
    path: PathLike


class MP3File:
    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.measured = False

    def measure(self):
        from mutagen.mp3 import MP3

        if not self.measured:
            statinfo = os.stat(self.path)
            self._size = str(statinfo.st_size)
            audio = MP3(self.path)
            self._length = str(audio.info.length)
            self.measured = True

    @property
    def size(self):
        if not self.measured:
            self.measure()
        return self._size

    @property
    def length(self):
        if not self.measured:
            self.measure()
        return self._length


@dataclass
class VttFile:
    path: PathLike


@dataclass
class VttMeta:
    path: PathLike


@dataclass
class PDFFile:
    path: PathLike


@dataclass
class Author:
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    affiliation: Optional[str] = None
    email: Optional[str] = None


@dataclass
class RichVTT:
    vtt: str
    images: List[Any]
    equations: List[Any]
    figures: List[Any]
    log_level: int = logging.INFO

    def init_logger(self, log_level: int = logging.INFO):
        self.logger = logging.getLogger(__name__)
        c_handler = logging.StreamHandler()
        c_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        c_handler.setLevel(log_level)
        c_handler.setFormatter(c_format)
        self.logger.addHandler(c_handler)

    def save(self, filepath: str):
        """
        Parameters
        ----------
        filepath : str
            folder to save vtt and images to
        """
        filepath_ = Path(filepath)
        for i, figure in enumerate(self.figures):
            figure_path = filepath_ / f"figure_{i}.png"
            self.vtt = self.vtt.format(**{f"figure_{i}_path": figure_path})
            self.logger.info(f"Saving figure to {figure_path}")
            figure.save(figure_path)

        for i, equation in enumerate(self.equations):
            equation_path = filepath_ / f"equation_{i}.png"
            self.vtt = self.vtt.format(**{f"equation_{i}_path": equation_path})
            self.logger.info(f"Saving equation to {equation_path}")
            equation.save(equation_path)

        with open(filepath_ / f"{filepath_.stem}.vtt", "w") as f:
            self.logger.info(f"Saving vtt to {filepath_ / f'{filepath_.stem}.vtt'}")
            f.write(self.vtt)


_installed_plugins = load_plugins("types")

for name, plugin in _installed_plugins.items():
    globals()[name] = plugin
