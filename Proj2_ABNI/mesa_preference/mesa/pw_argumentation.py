from turtle import pos
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
import random
from random import randint

list_criterion = [CriterionName.PRODUCTION_COST, CriterionName.ENVIRONMENT_IMPACT,
                  CriterionName.CONSUMPTION, CriterionName.DURABILITY,
                  CriterionName.NOISE]

NULL_ARG = 'No arguments to support this item'


class ArgumentAgent(CommunicatingAgent):
    """ 
    ArgumentAgent which inherit from CommunicatingAgent.
    """

    def __init__(self, unique_id, model, name, list_items):
        super().__init__(unique_id, model, name)
        self.preference = None
        self._list_items = list_items
        self._list_items_left = list_items.copy()
        self._committed = False
        self._arguments = []

    def step(self):
        super().step()
        list_messages = self.get_new_messages()
        for message in list_messages:

            # Print the message
            print(message)

            # Handle the PROPOSE message
            if message.get_performative() == MessagePerformative.PROPOSE:
                message_to_send_back = self.handle_PROPOSE_message(message)
                self.send_message(message_to_send_back)

            # Handle the ACCEPT or COMMIT message
            if message.get_performative() == MessagePerformative.ACCEPT or message.get_performative() == MessagePerformative.COMMIT:
                if not self._committed:
                    message_to_send_back = self.handle_ACCEPT_or_COMMIT_message(
                        message)
                    self.send_message(message_to_send_back)

            # Handle the ASK_WHY message
            if message.get_performative() == MessagePerformative.ASK_WHY:
                message_to_send_back = self.handle_ASK_WHY_message(message)
                self.send_message(message_to_send_back)

            # Handle the ARGUE message
            if message.get_performative() == MessagePerformative.ARGUE:
                message_to_send_back = self.handle_ARGUE_message(message)
                self.send_message(message_to_send_back)

    def get_preference(self):
        return self.preference

    def handle_PROPOSE_message(self, message):
        """Handle an item proposal
        :param message: Message - the message received
        :return: Message - the message to send back
        """
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
        """     
        Handle an item proposal acceptance or commit
        :param message: Message - the message received
        :return: Message - the message to send back
        """
        self._committed = True
        return Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.COMMIT, content=message.get_content())

    def handle_ASK_WHY_message(self, message):
        """
        Used when the agent receives "ASK_WHY" after having proposed an item 
        :param message: Message - the message received
        :return: string - the strongest supportive argument
        """
        # TODO: replace (o_i,reasons) by argument 
        o_i = message.get_content()
        reasons = self.support_proposal(o_i)
        if reasons == NULL_ARG:  # No more argument pro o_i
            # Remove o_i from the list of items
            self._list_items_left.remove(o_i)
            o_j = random.choice(self._list_items_left)
            return Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.PROPOSE, content=o_j)
        else:
            # Log the sent argument
            self._arguments.append((self,o_i,reasons))
            return Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.ARGUE, content= (o_i,reasons))
    
    def handle_ARGUE_message(self, message):
        """
        Used when the agent receives "ARGUE" 
        :param message: Message - the message received
        :return: string - argue back 
        """
        o_i,reasons = message.get_content()
        # Log the received argument
        self._arguments.append((message.get_exp(),self,o_i,reasons))
        self_reasons = self.counter_proposal(o_i)
        # Check if the argument is supported by the other agent
        # TODO: to be implemented
        if len(self.counter_proposal(o_i)) > 0 :
            o_i = o_i
            reasons = self.counter_proposal(o_i)
            return Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.ARGUE, content= (o_i,reasons))
        # If the argument is supported by the other agent, then the agent accepts the argument
        else: 
            return Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.ACCEPT, content=o_i)

    def generate_preferences(self, list_items, verbose=False, csv=False) -> None:
        """
        Generate the preferences of the agent
        :param list_items: list of items
        :param verbose: boolean - if True, print the preferences
        :param csv: boolean - if True, get the preferences from a csv file
        """
        preferences = Preferences()

        # If the agent has not generated the preferences yet and if it is reading from a csv file
        if csv:
            preferences.set_criterion_name_list(list_criterion)
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

        # Generating preferences without csv file using random values
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
        Used when the agent receives "ASK_WHY" after having proposed an item 
        :param item: str - name of the item which was proposed
        :return arg: Argument - the strongest supportive argument
        """
        arg = Argument(boolean_decision=True, item=item)
        possible_proposals = arg.list_supporting_proposal(
            item, self.preference)
        if len(possible_proposals) == 0:
            return NULL_ARG
        for proposal in possible_proposals:
            # Return a criterion that has the maximum value 
            # TODO: Can be improved taking into account the importance of the criterion
            if self.preference.get_value(item, proposal) == Value.VERY_GOOD:
                return proposal
            else:
                temp_proposal = proposal
        return temp_proposal
    
    def counter_proposal(self, item):
        """
        Used when the agent receives "ARGUE" after having proposed an item 
        :param item: str - name of the item which was proposed
        :return arg: Argument - the strongest supportive argument
        """
        # TODO: implement the counter-argumentation mechanism
        return []
    
    def argument_parsing(self, argument):
        """ returns ....
        :param argument: Argument - the argument to parse
        :return message: string - the strongest supportive argument
        """
        #proposal = self.support_proposal(item)
        #message = item.get_name() + " because " + proposal.name + " is " + self.preference.get_value(item, proposal)
        message = ''
        return message

class ArgumentModel(Model):
    """ 
    ArgumentModel which inherit from Model.
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
    electric_engine = Item("Electric Engine", "A very quiet and ecofriendly engine")
    list_items = [diesel_engine, electric_engine]

    # Agent 1
    agent_one = ArgumentAgent(0, argument_model, "agent_one", list_items)
    agent_one.generate_preferences(list_items, csv=True)
    argument_model.schedule.add(agent_one)

    # Agent 2
    agent_two = ArgumentAgent(1, argument_model, "agent_two", list_items)
    agent_two.generate_preferences(list_items, csv=True)
    argument_model.schedule.add(agent_two)

    # Send the proposal message
    most_preferred_item = agent_two.preference.most_preferred(list_items)
    agent_two.send_message(Message(agent_two.get_name(
    ), agent_one.get_name(), MessagePerformative.PROPOSE, most_preferred_item))

    # Run the model on 10 steps
    step = 0
    while step < 10:
        argument_model.step()
        step += 1
