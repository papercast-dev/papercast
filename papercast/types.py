from typing import Union
import os
from typing import List, Any
from pathlib import Path
from dataclasses import dataclass
import logging


# _installed_plugins = load_plugins("types")

# for name, plugin in _installed_plugins.items():
#     globals()[name] = plugin


PathLike = Union[str, Path]


@dataclass
class PNGFile:
    path: PathLike


@dataclass
class JPGFile:
    path: PathLike


@dataclass
class JPEGFile:
    path: PathLike


@dataclass
class WEBPFile:
    path: PathLike


@dataclass
class M4BFile:
    path: PathLike


@dataclass
class MP3File:
    path: PathLike


@dataclass
class M4AFile:
    path: PathLike


@dataclass
class FLACFile:
    path: PathLike


@dataclass
class OPUSFile:
    path: PathLike


@dataclass
class OGGFile:
    path: PathLike


@dataclass
class OGAFile:
    path: PathLike


@dataclass
class MP4File:
    path: PathLike


@dataclass
class AACFile:
    path: PathLike


@dataclass
class WMAFile:
    path: PathLike


@dataclass
class AIFFFile:
    path: PathLike


@dataclass
class WAVFile:
    path: PathLike


@dataclass
class WEBMFile:
    path: PathLike


@dataclass
class WEBMAFile:
    path: PathLike


@dataclass
class EPUBFile:
    path: PathLike


@dataclass
class PDFFile:
    path: PathLike


@dataclass
class MOBIFile:
    path: PathLike


@dataclass
class AZW3File:
    path: PathLike


@dataclass
class CBRFile:
    path: PathLike


@dataclass
class CBZFile:
    path: PathLike


@dataclass
class NFOFile:
    path: PathLike


@dataclass
class TXTFile:
    path: PathLike


@dataclass
class OPFFile:
    path: PathLike


@dataclass
class ABSFile:
    path: PathLike


@dataclass
class TxtFile:
    path: PathLike


@dataclass
class SRTFile:
    path: PathLike


@dataclass
class M4BFile:
    path: PathLike


@dataclass
class M4AFile:
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
class CoordinateLocatedMixin:
    """
    Mixin for objects that have a coordinate location in a document.
    Useful for documents with fixed layouts, such as PDFs.
    """

    page: int
    x0: float
    y0: float
    x1: float
    y1: float


@dataclass
class Author:
    name: str = None
    first_name: str = None
    last_name: str = None
    affiliation: str = None
    email: str = None


@dataclass
class Title:
    title: str = None
    subtitle: str = None


@dataclass
class Abstract:
    abstract: str = None
    keywords: str = None


@dataclass
class Figure:
    image: Any
    caption: str = None


@dataclass
class Table:
    table: Any
    image: Any
    caption: str = None


@dataclass
class SectionHeading:
    heading: str = None
    level: int = None


@dataclass
class Equation:
    equation: Any
    caption: str = None


@dataclass
class RichVTT:
    vtt: str
    images: List[Any]
    equations: List[Any]
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
        filepath = Path(filepath)
        for i, figure in enumerate(self.figures):
            figure_path = filepath / f"figure_{i}.png"
            self.vtt = self.vtt.format(**{f"figure_{i}_path": figure_path})
            self.logger.info(f"Saving figure to {figure_path}")
            figure.save(figure_path)

        for i, equation in enumerate(self.equations):
            equation_path = filepath / f"equation_{i}.png"
            self.vtt = self.vtt.format(**{f"equation_{i}_path": equation_path})
            self.logger.info(f"Saving equation to {equation_path}")
            equation.save(equation_path)

        with open(filepath / filepath.stem + ".vtt", "w") as f:
            self.logger.info(f"Saving vtt to {filepath / filepath.stem + '.vtt'}")
            f.write(self.vtt)
