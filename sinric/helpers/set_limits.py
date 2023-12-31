from numbers import Real
from typing import Generic, TypeVar, Union

# TODO: understand python generics
_number = TypeVar('_number', bound=Union[int, float, Real])


def set_limits(value: _number, min: int = 0, max: int = 100) -> _number:
    """
    Set value to within bounds.

    Args:
        value (Generic[_number]): The number you want to set the bounds for
        min (int, optional): The lower limit. Defaults to 0.
        max (int, optional): The upper limit. Defaults to 100.

    Returns:
        _number: The value capped to the limits
    """
    if (value < min):
        # TODO cast to number type
        return min
    elif value > max:
        return max
    return value
