from papercast.pipelines import Pipeline
from papercast.collectors.arxiv import ArxivCollector
from papercast.collectors.pdf import PDFCollector
from papercast.processors.say import SayProcessor
from papercast.processors import GROBIDProcessor
from papercast.publishers.github_pages import GitHubPagesPodcastPublisher
from papercast.server import Server

# Create a pipeline
pipeline = Pipeline(name="default")

# Add processors to the pipeline
pipeline.add_processor(
    "arxiv", ArxivCollector(pdf_dir="data/pdfs", json_dir="data/json")
)

pipeline.add_processor("pdf", PDFCollector(pdf_dir="data/pdfs"))

pipeline.add_processor(
    "grobid",
    GROBIDProcessor(
        remove_non_printable_chars=True, grobid_url="http://localhost:8070/"
    ),
)

pipeline.add_processor("say", SayProcessor(mp3_dir="data/mp3s", txt_dir="data/txts"))

pipeline.add_processor(
    "github_pages",
    GitHubPagesPodcastPublisher(
        title="<your-podcast-title>",
        base_url="<your-github-pages-url>",
        language="en-us",
        subtitle="",
        copyright="",
        author="<your-name>",
        email="<your-email>",
        description="",
        cover_path="<your-github-pages-url>/cover.jpg",
        categories=["Mathematics", "Tech News", "Courses"],
        keywords=[
            "Machine Learning",
            "Natural Language Processing",
            "Artificial Intelligence",
        ],
        xml_path="./feed.xml",
    ),
)

# Connect the pipeline components together
pipeline.connect("arxiv", "pdf", "grobid", "pdf")
pipeline.connect("pdf", "pdf", "grobid", "pdf")
pipeline.connect("grobid", "text", "say", "text")
pipeline.connect("say", "mp3_path", "github_pages", "mp3_path")
pipeline.connect("grobid", "abstract", "github_pages", "description")
pipeline.connect("grobid", "title", "github_pages", "title")


# Create a server
server = Server(pipelines={"default": pipeline})


# Run the server
if __name__ == "__main__":
    server.run()
