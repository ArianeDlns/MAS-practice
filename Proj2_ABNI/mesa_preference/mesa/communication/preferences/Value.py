#!/usr/bin/env python3

from enum import Enum


class Value(Enum):
    """Value enum class.
    Enumeration containing the possible Value.
    """
    VERY_BAD = 0
    BAD = 1
    AVERAGE = 2
    GOOD = 3
    VERY_GOOD = 4

    def matchvalue(value):
        dictionnary_value = dict(VERY_BAD=0,
                                BAD=1,
                                AVERAGE=2,
                                GOOD=3,
                                VERY_GOOD=4)
        word_value = list(dictionnary_value.keys())[value]
        return Value[word_value]

    def __str__(self):
        dictionnary_value = dict(VERY_BAD="Very bad",
                                BAD="Bad",
                                AVERAGE="Average",
                                GOOD="Good",
                                VERY_GOOD="Very good")
        word_value = list(dictionnary_value.keys())[self.value]
        return dictionnary_value[word_value]