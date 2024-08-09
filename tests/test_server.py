import pytest
from papercast.server import Server
from papercast.pipelines import Pipeline
from papercast.base import BaseProcessor, Production
from fastapi import HTTPException
from typing import List


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

    @pytest.mark.asyncio
    async def test_add_valid_input_to_default(self):
        class MyProcessor(BaseProcessor):
            input_types = {
                "input1": int,
            }

            def process(self, input: Production) -> Production:
                return input

        processor = MyProcessor()

        pipeline = Pipeline("test")

        pipeline.add_processor("test", processor)

        server = Server(
            pipelines={"default": pipeline},
        )
        result = await server._add({"input1": 5})
        assert result is not None
        assert result == {"message": "Document(s) added to pipeline"}

    @pytest.mark.asyncio
    @pytest.mark.xfail
    async def test_add_invalid_input_to_default(self):
        # TODO This test should at least warn the user that the input is invalid
        # Currently it runs without issue
        # Though I think the responsiblity of checking
        # the input should be on the pipeline or the processor
        class MyProcessor(BaseProcessor):
            input_types = {
                "input1": int,
            }

            def process(self, input: Production) -> Production:
                return input

        processor = MyProcessor()

        pipeline = Pipeline("test")

        pipeline.add_processor("test", processor)

        server = Server(
            pipelines={"default": pipeline},
        )
        with pytest.raises(HTTPException) as exc_info:
            result = await server._add({"incorrect_input_key": 5})

    @pytest.mark.asyncio
    async def test_add_valid_input_to_non_default_pipeline(self):
        class MyProcessor(BaseProcessor):
            input_types = {
                "input1": int,
            }

            def process(self, input: Production) -> Production:
                return input

        processor = MyProcessor()

        pipeline = Pipeline("non_default")
        pipeline.add_processor("test", processor)

        server = Server(
            pipelines={"default": Pipeline("default"), "non_default": pipeline},
        )
        result = await server._add({"pipeline": "non_default", "input1": 5})
        assert result is not None
        assert result == {"message": "Document(s) added to pipeline"}

    @pytest.mark.asyncio
    @pytest.mark.xfail
    async def test_add_invalid_input_to_non_default_pipeline(self):
        # TODO This test should at least warn the user that the input is invalid
        # Currently it runs without issue
        # Though I think the responsiblity of checking
        # the input should be on the pipeline or the processor
        class MyProcessor(BaseProcessor):
            input_types = {
                "input1": int,
            }

            def process(self, input: Production) -> Production:
                return input

        processor = MyProcessor()

        pipeline = Pipeline("non_default")
        pipeline.add_processor("test", processor)

        server = Server(
            pipelines={"default": Pipeline("default"), "non_default": pipeline},
        )

        with pytest.raises(HTTPException) as exc_info:
            await server._add({"pipeline": "non_default", "incorrect_input_key": 5})

    @pytest.mark.asyncio
    async def test_add_input_to_missing_pipeline(self):
        server = Server(
            pipelines={},
        )
        with pytest.raises(HTTPException) as exc_info:
            await server._add({"pipeline": "missing"})

    @pytest.mark.asyncio
    async def test_pipeline_not_specified_and_no_default_pipeline(self):
        server = Server(
            pipelines={},
        )

        with pytest.raises(HTTPException) as exc_info:
            await server._add({})

    def test_serialize_empty_pipelines(self):
        server = Server(
            pipelines={"default": Pipeline("default")},
        )
        print(server.serialize_pipelines())
        assert server.serialize_pipelines() == {
            "pipelines": {"default": {"subscribers": [], "processors": []}}
        }

    def test_serialize_pipelines(self):
        class MyProcessor(BaseProcessor):
            input_types = {
                "input1": int,
            }

            output_types = {
                "output1": int,
            }

            def process(self, input: Production) -> Production:
                return input

        processor = MyProcessor()

        pipeline = Pipeline("test")

        pipeline.add_processor("test", processor)

        server = Server(
            pipelines={"default": pipeline},
        )
        print(server.serialize_pipelines())

        assert server.serialize_pipelines() == {
            "pipelines": {
                "default": {
                    "subscribers": [],
                    "processors": [
                        {
                            "input_types": {"input1": "int"},
                            "output_types": {"output1": "int"},
                        }
                    ],
                }
            }
        }

    def test_serialize_pipelines_with_typing_types(self):
        class MyProcessor(BaseProcessor):
            input_types = {
                "input1": List[int],
            }

            output_types = {
                "output1": List[int],
            }

            def process(self, input: Production) -> Production:
                return input

        processor = MyProcessor()

        pipeline = Pipeline("test")

        pipeline.add_processor("test", processor)

        server = Server(
            pipelines={"default": pipeline},
        )
        print(server.serialize_pipelines())

        assert server.serialize_pipelines() == {
            "pipelines": {
                "default": {
                    "subscribers": [],
                    "processors": [
                        {
                            "input_types": {"input1": "typing.List[int]"},
                            "output_types": {"output1": "typing.List[int]"},
                        }
                    ],
                }
            }
        }
