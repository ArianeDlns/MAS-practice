#!/usr/bin/env python3


class CoupleValue:
    """CoupleValue class.
    This class implements a couple value used in argument object.

    attr:
        criterion_name: str - the name of the criterion
        value: str - the value of the criterion
    """

    def __init__(self, criterion_name, value):
        """Creates a new couple value.
        """
        self.__criterion_name = criterion_name
        self.__value = value

    def __str__(self) -> str:
        """Returns a string representation of the couple value.
        """
        return f"Criterion '{self.__criterion_name}' with value '{self.__value}'"