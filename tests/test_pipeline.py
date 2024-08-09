import pytest
from typing import Any, List, Union

from papercast.pipelines import Pipeline
from papercast.base import BaseProcessor, Production


class MyClass:
    pass


class MyInheritedClass(MyClass):
    pass


class TestPipeline:
    @pytest.mark.parametrize(
        "a,b,result",
        [
            (int, int, True),
            (int, Any, True),
            (Any, int, False),
            (List[int], List[int], True),
            (List[int], List[Any], True),
            (int, Union[int, float], True),
            (int, Union[float, str], False),
            (MyClass, MyInheritedClass, False),
            (MyInheritedClass, MyClass, True),
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
