import pytest

from knowmydevs.core.utils import str_utils


def test_snake_to_pascal_should_convert_snake_case_to_pascal():
    snake = "my_super_test"
    target = "MySuperTest"

    result = str_utils.snake_to_pascal(snake)

    assert result == target


def test_snake_to_pascal_should_raise_value_error_for_invalid_inputs():
    with pytest.raises(ValueError):
        str_utils.snake_to_pascal(None)

    with pytest.raises(ValueError):
        str_utils.snake_to_pascal(True)

    with pytest.raises(ValueError):
        str_utils.snake_to_pascal({"testing": 1234})