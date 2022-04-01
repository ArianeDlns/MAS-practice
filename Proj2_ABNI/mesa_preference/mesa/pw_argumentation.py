from mesa import Model
from mesa.time import RandomActivation
from spacy import prefer_gpu

from communication.preferences.Preferences import Preferences
from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative
from communication.message.MessageService import MessageService
from communication.preferences.CriterionName import CriterionName
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.Value import Value
from communication.preferences.Item import Item
from communication.arguments.Argument import Argument

import pandas as pd
from random import randint

list_criterion = [CriterionName.PRODUCTION_COST, CriterionName.ENVIRONMENT_IMPACT,
                  CriterionName.CONSUMPTION, CriterionName.DURABILITY,
                  CriterionName.NOISE]


class ArgumentAgent(CommunicatingAgent):
    """ TestAgent which inherit from CommunicatingAgent.
    """

    def __init__(self, unique_id, model, name, list_items):
        super().__init__(unique_id, model, name)
        self.preference = None
        self._list_items = list_items
        self._committed = False

    def step(self):
        super().step()
        list_messages = self.get_new_messages()
        for message in list_messages:
            print(message)
            if message.get_performative() == MessagePerformative.PROPOSE:
                message_to_send_back = self.handle_PROPOSE_message(message)
                self.send_message(message_to_send_back)

            if message.get_performative() == MessagePerformative.ACCEPT or message.get_performative() == MessagePerformative.COMMIT:
                if not self._committed:
                    message_to_send_back = self.handle_ACCEPT_or_COMMIT_message(
                        message)
                    self.send_message(message_to_send_back)

            if message.get_performative() == MessagePerformative.ASK_WHY:
                self.send_message(Message(from_agent=self.get_name(), to_agent=message.get_exp(
                ), message_performative=MessagePerformative.ARGUE, content=None))
                self._committed = True

            if message.get_performative() == MessagePerformative.ARGUE:
                self._committed = True

    def get_preference(self):
        return self.preference

    def handle_PROPOSE_message(self, message):
        """Handle an item proposal"""
        o_i = message.get_content()
        preferences = self.get_preference()
        if preferences.is_item_among_top_10_percent(o_i, self._list_items):
            o_j = preferences.most_preferred(self._list_items)
            if o_i == o_j:
                return Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.ACCEPT, content=o_i)
            else:
                return Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.PROPOSE, content=o_j)
        else:
            return Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.ASK_WHY, content=o_i)

    def handle_ACCEPT_or_COMMIT_message(self, message):
        self._committed = True
        return Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.COMMIT, content=message.get_content())

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
                    print(
                        pref.iloc[idx].Item, pref.iloc[idx].CriterionValue, pref.iloc[idx].CriterionName)
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

    def support_proposal(self, item):
        """
        Used when the agent receives "ASK_WHY" after having proposed an item :param item: str - name of the item which was proposed
        :return: string - the strongest supportive argument
        """
        arg = Argument(boolean_decision=False, item=item)
        possible_proposals = arg.List_supporting_proposal(
            item, self.preference)
        if len(possible_proposals) == 0:
            return 'No arguments in favor of this item'
        for proposal in possible_proposals:
            if proposal.get_value().name == 'VERY_GOOD':
                return proposal
            else:
                temp_proposal = proposal
        return temp_proposal


class ArgumentModel(Model):
    """ ArgumentModel which inherit from Model.
    """

    def __init__(self):
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)
        self.running = True

    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step()


if __name__ == "__main__":
    argument_model = ArgumentModel()

    diesel_engine = Item("Diesel Engine", "A super cool diesel engine")
    electric_engine = Item("Electric Engine", "A very quiet engine")
    list_items = [diesel_engine, electric_engine]

    # Agent 1
    agent_one = ArgumentAgent(0, argument_model, "agent_one", list_items)
    agent_one.generate_preferences(list_items, csv=True)
    argument_model.schedule.add(agent_one)

    # Agent 2
    agent_two = ArgumentAgent(1, argument_model, "agent_two", list_items)
    agent_two.generate_preferences(list_items, csv=True)
    argument_model.schedule.add(agent_two)

    agent_one.send_message(Message(agent_one.get_name(), agent_two.get_name(), MessagePerformative.PROPOSE, "Diesel Engine"))

    step = 0
    while step < 10:
        argument_model.step()
        step += 1
