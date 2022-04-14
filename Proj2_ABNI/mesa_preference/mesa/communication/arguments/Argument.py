#!/usr/bin/env python3

from communication.arguments.Comparison import Comparison
from communication.arguments.CoupleValue import CoupleValue
from communication.preferences.Preferences import Preferences
from communication.preferences.Item import Item
from communication.preferences.Value import Value


class Argument:
    """Argument class.
    This class implements an argument used in the negotiation.

    attr:
        decision: bool - the decision of the argument
        item: str - the name of the item
        comparison_list: list of Comparison - the list of comparisons
        couple_values_list: list of CoupleValue - the list of couple values
    """

    def __init__(self, boolean_decision, item: Item):
        """Creates a new Argument.
        """
        self.__decision = boolean_decision
        self.__item = item.get_name()
        self.__comparison_list: list[Comparison] = []
        self.__couple_values_list: list[CoupleValue] = []

    def __str__(self) -> str:
        return f"{'not'*(not self.__decision)} {self.__item} <= {'|'.join(list(map(str, self.__couple_values_list)))}, {'|'.join(list(map(str, self.__comparison_list)))}"

    def add_premiss_comparison(self, criterion_name_1, criterion_name_2):
        """Adds a premiss comparison in the comparison list.
        """
        self.__comparison_list.append(Comparison(criterion_name_1, criterion_name_2))

    def add_premiss_couple_values(self, criterion_name, value):
        """Add a premiss couple values in the couple values list.
        """
        self.__couple_values_list.append(CoupleValue(criterion_name, value))

    def list_supporting_proposal(self, item: Item, preferences: Preferences):
        """Generate a list of premisses which can be used to support an item
        :param item: Item - name of the item
        :param preferences: Preferences - preferences of the agent
        :return: list of all premisses PRO an item (sorted by order of importance based on agent's preferences)
        """
        supporting_proposal = []
        for criterion_name in preferences.get_criterion_name_list():
            if (preferences.get_value(item, criterion_name) in [Value.GOOD, Value.VERY_GOOD]):
                supporting_proposal.append(criterion_name)
        return supporting_proposal

    def list_attacking_proposal(self, item: Item, preferences: Preferences):
        """Generate a list of premisses which can be used to attack an item
        :param item: Item - name of the item
        :param preferences: Preferences - preferences of the agent
        :return: list of all premisses CON an item (sorted by order of importance based on preferences)
        """
        attacking_proposal = []
        for criterion_name in preferences.get_criterion_name_list():
            if preferences.get_value(item, criterion_name) in [Value.BAD, Value.VERY_BAD]:
                attacking_proposal.append(criterion_name)
        return attacking_proposal

    def get_decision(self):
        """Returns the decision of the argument.
        """
        return self.__decision

    def get_item(self):
        """Returns the item of the argument.
        """
        return self.__item

    def argument_parsing(self):
        """ returns ....
        :param argument: :return: 
        """
        criterion_used = [couple.get_criterion_name() for couple in self.__couple_values_list]
        return criterion_used


if __name__ == "__main__":
    pass
