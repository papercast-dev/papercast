
import os

from dotenv import load_dotenv
from papercast.pipelines import Pipeline
from papercast.processors import (
    GROBIDProcessor,
    EdgeTTSProcessor,
    PDFProcessor,
)
from papercast.server import Server

load_dotenv()

grobid_kwargs = dict(
    remove_non_printable_chars=True, grobid_url="http://localhost:8070/", serve_grobid_script="~/forks/scipdf_parser/serve_grobid.sh"
)


def make_default_pipeline():
    pipeline = Pipeline(name="default")
    pipeline.add_processors(
        {
            "pdf": PDFProcessor(pdf_dir="data/pdfs"),
            "grobid": GROBIDProcessor(**grobid_kwargs),
            "edge_tts": EdgeTTSProcessor(mp3_dir="data/mp3s", txt_dir="data/txts"),
        },
    )

    pipeline.connect("pdf", "pdf", "grobid", "pdf")
    pipeline.connect("grobid", "text", "edge_tts", "text")

    return pipeline


default_pipeline = make_default_pipeline()

server = Server(pipelines={"default": default_pipeline})

if __name__ == "__main__":
    server.run()
