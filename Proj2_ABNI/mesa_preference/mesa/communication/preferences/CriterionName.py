#!/usr/bin/env python3

from enum import Enum


class CriterionName(Enum):
    """CriterionName enum class.
    Enumeration containing the possible CriterionName.
    """
    PRODUCTION_COST = 0
    CONSUMPTION = 1
    DURABILITY = 2
    ENVIRONMENT_IMPACT = 3
    NOISE = 4

    def matchvalue(self, value):
        dictionnary_value = dict(PRODUCTION_COST=0,
                                 CONSUMPTION=1,
                                 DURABILITY=2,
                                 ENVIRONMENT_IMPACT=3,
                                 NOISE=4)
        word_value = list(dictionnary_value.keys())[value]
        return CriterionName[word_value]

    def __str__(self):
        dictionnary_value = dict(PRODUCTION_COST="Production cost",
                                 CONSUMPTION="Consumption",
                                 DURABILITY="Durability",
                                 ENVIRONMENT_IMPACT="Environment impact",
                                 NOISE="Noise")
        word_value = list(dictionnary_value.keys())[self.value]
        return dictionnary_value[word_value]