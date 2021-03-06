from asyncio.windows_events import NULL
from mesa import Model
from mesa.time import RandomActivation

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
                self._arguments = [] #Changing to another item so reset the arguments
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

    def handle_PROPOSE_message(self, message):
        """Handle an item proposal
        :param message: Message - the message received
        :return: Message - the message to send back
        """
        o_i = message.get_content()
        preferences = self.get_preference()
        if preferences.is_item_among_top_10_percent(o_i, self._list_items):
            o_j = preferences.most_preferred(self._list_items_left)
            if o_i == o_j:
                return Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.ACCEPT, content=o_i)
            else:
                self._arguments = [] #Changing to another item so reset the arguments
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

    def handle_ARGUE_message(self, message):
        """
        Used when the agent receives "ARGUE" 
        :param message: Message - the message received
        :return: string - argue back 
        """
        args = message.get_content()

        chosen_item = [item for item in self._list_items if item.get_name()==args.get_item()][0]
        decision = args.get_decision()
        # Log the received argument
        if args != NULL_ARG: #Don't add null argument to the argument list
            self._arguments.append((message.get_exp(),args))
        # Check if the argument is supported by the other agent
        counter_arg, counter_score = self.counter_proposal(chosen_item,args)
        send_arg, pro_score = self.support_proposal(chosen_item)
        # Print scores
        # print("Counter proposal: ", counter_score, "- Support proposal: ", pro_score)
        
        # No more argument 
        if decision: 
            if counter_score > args.get_score():
                # Log the argument
                self._arguments.append((self,counter_arg))
                return Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.ARGUE, content= counter_arg)
            else:
                return Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.ACCEPT, content= chosen_item)
        else: 
            if pro_score > args.get_score():
             # Log the argument
                self._arguments.append((self,counter_arg))
                return Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.ARGUE, content= send_arg)
            else:
                self._list_items_left.remove(chosen_item)
                o_j = self.get_preference().most_preferred(self._list_items_left) # Propose the most preferred item
                self._arguments = [] #Changing to another item so reset the arguments
                return Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.PROPOSE, content=o_j)

    def handle_ASK_WHY_message(self, message):
        """
        Used when the agent receives "ASK_WHY" after having proposed an item 
        :param message: Message - the message received
        :return: string - the strongest supportive argument
        """
        item_chosen = message.get_content()
        if type(item_chosen) == Item:
            send_arg, _ = self.support_proposal(item_chosen)
            if send_arg == NULL_ARG:  # No more argument pro o_i
                self._list_items_left.remove(item_chosen)
                other_item = random.choice(self._list_items_left)
                self._arguments = [] #Changing to another item so reset the arguments
                return Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.PROPOSE, content=other_item)
            else:
                # Log the send argument 
                self._arguments.append((self,send_arg))
                return Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.ARGUE, content = send_arg)

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

    def get_preference(self):
        return self.preference

    def support_proposal(self, item):
        """
        Used when the agent receives "ASK_WHY" after having proposed an item 
        :param item: str - name of the item which was proposed
        :return arg: Argument - the strongest supportive argument
        """
        prev_arg = [a[1].argument_parsing()[0] for a in self._arguments if a != NULL_ARG] 
        arg = Argument(boolean_decision=True, item=item)
        possible_proposals = arg.list_supporting_proposal(
            item, self.preference)
        possible_proposals = [proposal for proposal in possible_proposals if proposal not in prev_arg]
        if len(possible_proposals) == 0:
            return NULL_ARG, 0
        # TODO: Can be improved taking into account the importance of the criterion
        else:       
            values = [(5-proposal.value) + self.preference.get_value(item, proposal).value/10 for proposal in possible_proposals]
            index_max_value = values.index(max(values))
            proposal = possible_proposals[index_max_value]
        final_arg = Argument(boolean_decision=True, item=item, score = max(values))
        value = self.preference.get_value(item, proposal)
        final_arg.add_premiss_couple_values(proposal,value)
        return final_arg, max(values)
    
    def counter_proposal(self, item, prev_arg):
        """
        Used when the agent receives "ARGUE" after having proposed an item 
        :param item: str - name of the item which was proposed
        :param prev_arg: Argument - the previous argument
        :return arg: Argument - the strongest supportive argument
        """
        prev_arg_criteria = prev_arg.argument_parsing()[0]
        arg = Argument(boolean_decision=True, item=item)
        possible_proposals = arg.list_attacking_proposal(
            item, self.preference)
        # Remove used criterion already used 
        prev_arg = [a[1].argument_parsing()[0] for a in self._arguments if a != NULL_ARG] 
        possible_proposals = [proposal for proposal in possible_proposals if proposal not in prev_arg]
        if len(possible_proposals) == 0:
            return NULL_ARG, 0
        # TODO: Can be improved taking into account the importance of the criterion
        else:       
            values = [(5 - proposal.value) + (5  - self.preference.get_value(item, proposal).value)/10 for proposal in possible_proposals]
            index_max_value = values.index(max(values))
            proposal = possible_proposals[index_max_value]
        if proposal.value > prev_arg_criteria.value: # The proposal has not a higher rank than the previous one
            return NULL_ARG, 0
        final_arg = Argument(boolean_decision=False, item=item, score = max(values))
        value = self.preference.get_value(item, proposal)
        final_arg.add_premiss_couple_values(proposal,value)
        final_arg.add_premiss_comparison(proposal, prev_arg_criteria)
        return final_arg, max(values)

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
    CRED = '\x1b[0;30;41m'
    CGREEN = '\x1b[6;30;42m'
    CEND = '\x1b[0m'

    cRED = '\033[91m'
    cGREEN = '\033[92m'
    cYELLOW = '\033[93m'
    cPURPLE = '\033[95m'
    cEND = '\033[0m'


    argument_model = ArgumentModel()

    diesel_engine = Item(cRED+"Diesel Engine"+cEND, "A super cool diesel engine")
    electric_engine = Item(cGREEN+"Electric Engine"+cEND, "A very quiet and ecofriendly engine")
    mixed_engine = Item(cPURPLE+"Mixed Engine"+cEND, "Engine")
    mixed_engine_1 = Item("Mixed Engine 1", "Engine")
    mixed_engine_2 = Item("Mixed Engine 2", "Engine")
    mixed_engine_3 = Item("Mixed Engine 3", "Engine")
    mixed_engine_4 = Item("Mixed Engine 4", "Engine")
    mixed_engine_5 = Item("Mixed Engine 5", "Engine")
    mixed_engine_6 = Item("Mixed Engine 6", "Engine")
    list_items = [diesel_engine, electric_engine, mixed_engine]

    # Agent 1
    agent_one = ArgumentAgent(0, argument_model, CRED + "agent_one" + CEND, list_items)
    agent_one.generate_preferences(list_items, csv=False)
    print("Preferences for Agent One:")
    print(agent_one.preference)
    argument_model.schedule.add(agent_one)

    # Agent 2
    agent_two = ArgumentAgent(1, argument_model, CGREEN + "agent_two" + CEND, list_items)
    agent_two.generate_preferences(list_items, csv=False)
    print("\nPreferences for Agent Two:")
    print(agent_two.preference)
    argument_model.schedule.add(agent_two)

    # Send the proposal message
    most_preferred_item = agent_two.preference.most_preferred(list_items)
    agent_two.send_message(Message(agent_two.get_name(
    ), agent_one.get_name(), MessagePerformative.PROPOSE, most_preferred_item))

    # Run the model on 100 steps
    step = 0
    while step < 100:
        argument_model.step()
        step += 1
