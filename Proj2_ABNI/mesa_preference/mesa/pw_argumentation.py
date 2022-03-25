from mesa import Model
from mesa.time import RandomActivation
from spacy import prefer_gpu

from communication.preferences.Preferences import Preferences
from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessageService import MessageService
from communication.preferences.CriterionName import CriterionName
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.Value import Value
from communication.preferences.Item import Item

import pandas as pd
from random import randint

list_criterion = [CriterionName.PRODUCTION_COST, CriterionName.ENVIRONMENT_IMPACT,
                  CriterionName.CONSUMPTION, CriterionName.DURABILITY,
                  CriterionName.NOISE]


class ArgumentAgent(CommunicatingAgent):
    """ TestAgent which inherit from CommunicatingAgent.
    """

    def __init__(self, unique_id, model, name):
        super().__init__(unique_id, model, name)
        self.preference = None

    def step(self):
        super().step()

    def get_preference(self):
        return self.preference

    def generate_preferences(self, list_items, verbose=False, csv=False) -> None:
        preferences = Preferences()
        if csv:
            dict_item = {
                "diesel_engine": list_items[0], "electric_engine": list_items[1]}
            pref = pd.read_csv('preferences.csv', sep=';')
            # Filter on agent number
            pref = pref[pref['agent'] == self.unique_id]
            for idx in range(len(pref)):
                if verbose:
                    print(pref.iloc[idx].Item, pref.iloc[idx].CriterionValue, pref.iloc[idx].CriterionName)
                preferences.add_criterion_value(CriterionValue(dict_item[pref.iloc[idx].Item],
                                                               CriterionName[pref.iloc[idx].CriterionName],
                                                               Value[pref.iloc[idx].CriterionValue]))
        else:
            preferences.set_criterion_name_list(list_criterion)
            for item in list_items:
                for criterion in list_criterion:
                    random = randint(0, 4)
                    preferences.add_criterion_value(CriterionValue(
                        item, criterion, Value.matchvalue(random)))
                    if verbose:
                        print(item, criterion, Value.matchvalue(random))

        self.preference = preferences


class ArgumentModel(Model):
    """ ArgumentModel which inherit from Model.
    """

    def __init__(self):
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)

        diesel_engine = Item("Diesel Engine", "A super cool diesel engine")
        electric_engine = Item("Electric Engine", "A very quiet engine")

        list_items = [diesel_engine, electric_engine]

        agent_one = ArgumentAgent(0, self, "agent_one")
        agent_two = ArgumentAgent(1, self, "agent_two")

        agent_one.generate_preferences(list_items, csv=True)
        agent_two.generate_preferences(list_items, csv=True)

        self.schedule.add(agent_one)
        self.schedule.add(agent_two)

        self.running = True

    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step()


if __name__ == "__main__":
    argument_model = ArgumentModel()
