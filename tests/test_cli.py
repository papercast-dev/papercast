import pytest
from unittest.mock import Mock
from papercast.scripts.papercast import call_api, parse_arguments, main
import sys


def test_call_api(mocker):
    mock_post = mocker.patch("requests.post")
    mock_response = Mock()
    mock_response.json.return_value = {"result": "success"}
    mock_post.return_value = mock_response

    result = call_api("test_endpoint", {"param1": "value1"})

    mock_post.assert_called_once_with(
        "http://localhost:8000/test_endpoint", json={"param1": "value1"}
    )
    assert result == {"result": "success"}


def test_parse_arguments(mocker):
    mocker.patch.object(
        sys,
        "argv",
        ["script.py", "endpoint", "--param1", "value1", "--param2", "value2", "value3"],
    )

    endpoint, params = parse_arguments()

    assert endpoint == "endpoint"
    assert params == {"param1": "value1", "param2": ["value2", "value3"]}


def test_not_enough_arguments(mocker):
    mocker.patch.object(sys, "argv", ["script.py"])

    with pytest.raises(SystemExit):
        parse_arguments()


def test_unexpected_parameter(mocker):
    mocker.patch.object(sys, "argv", ["script.py", "endpoint", "value1", "--param2"])

    with pytest.raises(SystemExit):
        parse_arguments()


def test_main(mocker):
    mock_parse_arguments = mocker.patch("papercast.scripts.papercast.parse_arguments")
    mock_parse_arguments.return_value = ("test_endpoint", {"param1": "value1"})

    mock_call_api = mocker.patch("papercast.scripts.papercast.call_api")
    mock_call_api.return_value = {"result": "success"}

    mock_print = mocker.patch("builtins.print")

    main()

    mock_parse_arguments.assert_called_once()
    mock_call_api.assert_called_once_with("test_endpoint", {"param1": "value1"})
    mock_print.assert_called_once_with('{"result": "success"}')
