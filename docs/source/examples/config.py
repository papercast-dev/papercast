from papercast.pipelines import Pipeline
from papercast.collectors import SemanticScholarProcessor, ArxivProcessor, PDFProcessor
from papercast.narrators import Narrator, SayNarrator, PollyNarrator
from papercast.extractors import Extractor, GROBIDExtractor
from papercast.publishers import Publisher, GithubPagesPodcastPublisher


class MyPipeline(Pipeline):
    def __init__(self):
        self.name = "default"
        self.collectors = [
            SemanticScholarProcessor(input_names={"id": "ss_id"}),
            ArxivProcessor(),
            PDFProcessor(),
        ]
        self.extractors = [GROBIDExtractor(input_names={"pdf": "pdf"})]
        self.narrators = [PollyNarrator()]
        self.filters = []
        self.publishers = [GithubPagesPodcastPublisher()]
