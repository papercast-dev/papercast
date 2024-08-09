import pytest
from typing import Any, List, Union

from papercast.pipelines import Pipeline


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
        ],
    )
    def test_is_subtype(self, a, b, result):
        "Test whether `a` is a subtype (inclusive) of `b`."
        assert Pipeline.is_subtype(a, b) == result
