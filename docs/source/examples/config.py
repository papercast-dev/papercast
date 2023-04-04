from papercast.pipelines import Pipeline
from papercast.collectors import SemanticScholarCollector, ArxivCollector, PDFCollector
from papercast.narrators import Narrator, SayNarrator, PollyNarrator
from papercast.extractors import Extractor, GROBIDExtractor
from papercast.publishers import Publisher, GithubPagesPodcastPublisher


class MyPipeline(Pipeline):
    def __init__(self):
        self.name = "default"
        self.collectors = [
            SemanticScholarCollector(input_names={"id": "ss_id"}),
            ArxivCollector(),
            PDFCollector(),
        ]
        self.extractors = [GROBIDExtractor(input_names={"pdf": "pdf"})]
        self.narrators = [PollyNarrator()]
        self.filters = []
        self.publishers = [GithubPagesPodcastPublisher()]
