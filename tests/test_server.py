import pytest
from papercast.server import Server
from papercast.pipelines import Pipeline
from papercast.base import BaseProcessor


class TestServer:
    def test_init(self):
        server = Server(
            pipelines={},
        )
        assert server is not None

    def test_root(self):
        server = Server(
            pipelines={},
        )
        assert server._root() == {"message": "Papercast Server"}

    def test_missing_pipeline(self):
        server = Server(
            pipelines={},
        )
        with pytest.raises(Exception):
            server._get_pipeline("missing")

    def test_get_pipeline(self):
        server = Server(
            pipelines={"test": Pipeline("test")},
        )
        assert server._get_pipeline("test") is not None
