#!/usr/bin/env python3

#TO RUN TESTS : python3 -m communication.preferences.Preferences
import random
import math
from prettytable import PrettyTable


from communication.preferences.CriterionName import CriterionName
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.Item import Item
from communication.preferences.Value import Value


class Preferences:
    """Preferences class.
    This class implements the preferences of an agent.

    attr:
        criterion_name_list: the list of criterion name (ordered by importance)
        criterion_value_list: the list of criterion value
    """

    def __init__(self):
        """Creates a new Preferences object.
        """
        self.__criterion_name_list = []
        self.__criterion_value_list = []
    
    def __str__(self):
        """
        Print preferences for the agent
        """
        order_str = ""
        x = PrettyTable()
        criterions = [str(criteria) + ': ' + str(criteria.value) for criteria in self.__criterion_name_list]
        x.field_names = ["Item", *criterions]
        items = set([x.get_item() for x in self.__criterion_value_list])
        items = list(sorted(items, key=lambda item: item.get_score(self), reverse=True))
        for item in items:
            values = [
                self.get_value(item, criterion_name)
                for criterion_name in self.__criterion_name_list
            ]
            x.add_row([str(item), *values])
        return order_str + "\n" + x.get_string()

    def get_criterion_name_list(self):
        """Returns the list of criterion name.
        """
        return self.__criterion_name_list

    def get_criterion_value_list(self):
        """Returns the list of criterion value.
        """
        return self.__criterion_value_list

    def set_criterion_name_list(self, criterion_name_list):
        """Sets the list of criterion name.
        """
        self.__criterion_name_list = criterion_name_list

    def add_criterion_value(self, criterion_value):
        """Adds a criterion value in the list.
        """
        self.__criterion_value_list.append(criterion_value)

    def get_value(self, item, criterion_name):
        """Gets the value for a given item and a given criterion name.
        """
        for value in self.__criterion_value_list:
            if value.get_item() == item and value.get_criterion_name() == criterion_name:
                return value.get_value()
        return None

    def is_preferred_criterion(self, criterion_name_1, criterion_name_2):
        """Returns if a criterion 1 is preferred to the criterion 2.
        """
        for criterion_name in self.__criterion_name_list:
            if criterion_name == criterion_name_1:
                return True
            if criterion_name == criterion_name_2:
                return False

    def is_preferred_item(self, item_1, item_2):
        """Returns if the item 1 is preferred to the item 2.
        """
        return item_1.get_score(self) > item_2.get_score(self)

    def most_preferred(self, item_list) :
        """ Returns the most preferred item from a list .
        """
        copied_item_list = item_list.copy()
        random.shuffle(copied_item_list)
        best_score = 0
        best_item = item_list[0]
        for item in copied_item_list:
            item_score = item.get_score(self)
            if item_score > best_score:
                best_item = item
                best_score = item_score
        return best_item

    def is_item_among_top_10_percent(self, item, item_list):
        """
        Return whether a given item is among the top 10 percent of the preferred items.

        :return: a boolean, True means that the item is among the favorite ones
        """
        copied_item_list = item_list.copy()
        random.shuffle(copied_item_list)

        item_and_score_list = [(item, item.get_score(self)) for item in copied_item_list]
        item_and_score_list = sorted(item_and_score_list, key = lambda x : x[1])
        
        ten_percent_best_items = []
        for i in range(1, math.ceil(len(item_and_score_list)/10+1)):
            ten_percent_best_items.append(item_and_score_list[-i][0])

        is_top_item = item in ten_percent_best_items
         
        return is_top_item


if __name__ == '__main__':
    """Testing the Preferences class.
    """
    agent_pref = Preferences()
    agent_pref.set_criterion_name_list([CriterionName.PRODUCTION_COST, CriterionName.ENVIRONMENT_IMPACT,
                                        CriterionName.CONSUMPTION, CriterionName.DURABILITY,
                                        CriterionName.NOISE])

    diesel_engine = Item("Diesel Engine", "A super cool diesel engine")
    agent_pref.add_criterion_value(CriterionValue(diesel_engine, CriterionName.PRODUCTION_COST,
                                                  Value.VERY_GOOD))
    agent_pref.add_criterion_value(CriterionValue(diesel_engine, CriterionName.CONSUMPTION,
                                                  Value.GOOD))
    agent_pref.add_criterion_value(CriterionValue(diesel_engine, CriterionName.DURABILITY,
                                                  Value.VERY_GOOD))
    agent_pref.add_criterion_value(CriterionValue(diesel_engine, CriterionName.ENVIRONMENT_IMPACT,
                                                  Value.VERY_BAD))
    agent_pref.add_criterion_value(CriterionValue(diesel_engine, CriterionName.NOISE,
                                                  Value.VERY_BAD))

    electric_engine = Item("Electric Engine", "A very quiet engine")
    agent_pref.add_criterion_value(CriterionValue(electric_engine, CriterionName.PRODUCTION_COST,
                                                  Value.BAD))
    agent_pref.add_criterion_value(CriterionValue(electric_engine, CriterionName.CONSUMPTION,
                                                  Value.VERY_BAD))
    agent_pref.add_criterion_value(CriterionValue(electric_engine, CriterionName.DURABILITY,
                                                  Value.GOOD))
    agent_pref.add_criterion_value(CriterionValue(electric_engine, CriterionName.ENVIRONMENT_IMPACT,
                                                  Value.VERY_GOOD))
    agent_pref.add_criterion_value(CriterionValue(electric_engine, CriterionName.NOISE,
                                                  Value.VERY_GOOD))

    """test list of preferences"""
    print(diesel_engine)
    print(electric_engine)
    print(diesel_engine.get_value(agent_pref, CriterionName.PRODUCTION_COST))
    print(agent_pref.is_preferred_criterion(CriterionName.CONSUMPTION, CriterionName.NOISE))

    print('Electric Engine > Diesel Engine : {}'.format(agent_pref.is_preferred_item(electric_engine, diesel_engine)))
    print('Diesel Engine > Electric Engine : {}'.format(agent_pref.is_preferred_item(diesel_engine, electric_engine)))

    print('Electric Engine (for agent 1) = {}'.format(electric_engine.get_score(agent_pref)))
    print('Diesel Engine (for agent 1) = {}'.format(diesel_engine.get_score(agent_pref)))

    print('Most preferred item is : {}'.format(agent_pref.most_preferred([diesel_engine, electric_engine]).get_name()))
    
    print('Is Electric Engine top 10% (for agent 1) ? : {}'.format(agent_pref.is_item_among_top_10_percent(electric_engine, [diesel_engine, electric_engine])))
    print('Is Diesel Engine top 10% (for agent 1) ? : {}'.format(agent_pref.is_item_among_top_10_percent(diesel_engine, [diesel_engine, electric_engine])))