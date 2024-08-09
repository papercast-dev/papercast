import pytest
from typing import Any, List, Union, Dict

from papercast.pipelines import Pipeline
from papercast.base import BaseProcessor, Production


class MyClass:
    pass


class MyInheritedClass(MyClass):
    pass


class AnotherClass:
    pass


class TestPipeline:
    @pytest.mark.parametrize(
        "a,b,result",
        [
            (List, Dict, False),
            (Dict, List, False),
            (int, float, False),
            (int, int, True),
            (int, Any, True),
            (Any, int, False),
            (List[int], List[int], True),
            (List[int], List[Any], True),
            (int, Union[int, float], True),
            (int, Union[float, str], False),
            (MyClass, MyInheritedClass, False),
            (MyInheritedClass, MyClass, True),
            (MyClass, MyClass, True),
            (MyInheritedClass, MyInheritedClass, True),
            (MyClass, AnotherClass, False),
        ],
    )
    def test_is_subtype(self, a, b, result):
        "Test whether `a` is a subtype (inclusive) of `b`."
        assert Pipeline.is_subtype(a, b) == result

    def test_validate_name(self):
        "Test that names are validated correctly."

        class MyProcessor(BaseProcessor):
            input_types = {
                "input1": int,
            }

            def process(self, input: Production) -> Production:
                return input

        processor = MyProcessor()

        pipeline = Pipeline("default")
        pipeline.add_processor("test", processor)

        with pytest.raises(ValueError):
            pipeline._validate_name("test")
        pipeline._validate_name("valid_name")

    def test_topological_sort(self):
        "Test that the topological sort works correctly."

        class MyProcessor(BaseProcessor):
            input_types = {
                "input1": int,
            }
            output_types = {
                "output": int,
            }

            def process(self, input: Production) -> Production:
                return input

        processor = MyProcessor()

        pipeline = Pipeline("default")
        pipeline.add_processor("test", processor)

        pipeline.add_processor("test2", processor)
        pipeline.connect("test", "output", "test2", "input1")

        pipeline.add_processor("test3", processor)
        pipeline.connect("test2", "output", "test3", "input1")

        pipeline.add_processor("test4", processor)
        pipeline.connect("test3", "output", "test4", "input1")

        sorted_processors = pipeline._topological_sort(
            processor_names=["test", "test2", "test3", "test4"]
        )

        assert sorted_processors == ["test", "test2", "test3", "test4"]
