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

    def generate_preferences(self, list_items, verbose=0) -> None:
        preferences = Preferences()
        preferences.set_criterion_name_list(list_criterion)
        for item in list_items: 
            for criterion in list_criterion: 
                random = randint(0,4)
                preferences.add_criterion_value(CriterionValue(item,criterion,Value.matchvalue(random))) 
                if verbose:
                    print(item,criterion,Value.matchvalue(random))
        self.preference = preferences

class ArgumentModel(Model):
    """ ArgumentModel which inherit from Model.
    """
    def __init__(self):
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)

        # To be completed
        # list_items = [...]
        #
        # a = TestAgent(id, self, "agent_name")
        # a.generate_preferences(list_items)
        # self.schedule.add(a)
        # ...

        self.running = True

    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step()


if __name__ == "__main__":
    argument_model = ArgumentModel()

    diesel_engine = Item("Diesel Engine", "A super cool diesel engine")
    electric_engine = Item("Electric Engine", "A very quiet engine")

    seller = ArgumentAgent(0, argument_model, "Seller")
    seller.generate_preferences([electric_engine,diesel_engine])