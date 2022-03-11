#!/usr/bin/env python3
"""
Testing all the functionalities of the communication package.
"""

from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.mailbox.Mailbox import Mailbox
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative
from communication.message.MessageService import MessageService


class TestAgent(CommunicatingAgent):
    """ TestAgent which inherit from CommunicatingAgent to test these functionalities.
    """
    def __init__(self, unique_id, model, name):
        super().__init__(unique_id, model, name)

    def step(self):
        super().step()

class AliceOrBob(CommunicatingAgent):
    """Alice or Bob agent that will send messages to the Charles agent"""
    def __init__(self, unique_id, model, name, v):
        super().__init__(unique_id, model, name)
        self.prefered_value = v
        self.is_happy = False
    
    def step(self):
        #New message :
        for new_message in self.get_new_messages():
            if new_message.get_performative() == MessagePerformative.INFORM_REF:
                current_value = new_message.get_content()
                self.is_happy = (current_value == self.prefered_value)

        #Sending message to Charles
        charles_id = 2
        for agent in self.model.schedule.agents:
            if agent.get_name() == "Charles":
                charles_id = agent.unique_id
        
        if not self.is_happy :
            m = Message(self.unique_id,charles_id, MessagePerformative.PROPOSE, self.prefered_value)
            self.send_message(m)

        else:
            m = Message(self.unique_id,charles_id, MessagePerformative.QUERY_REF, "What is the value ?")
            self.send_message(m)

class Charles(CommunicatingAgent):
    """Charles agent that receive messages from Alice and Bob"""
    def __init__(self, unique_id, model, name):
        super().__init__(unique_id, model, name)
        self.current_value = 0
    
    def step(self):
        for new_message in self.get_new_messages():
            if new_message.get_performative() == MessagePerformative.QUERY_REF:
                sender = new_message.get_exp()
                m = Message(self.unique_id, sender, MessagePerformative.INFORM_REF, self.current_value)
                self.send_message(m)
            elif new_message.get_performative() == MessagePerformative.PROPOSE:
                prefered_value = new_message.get_content()
                self.current_value = prefered_value
                sender = new_message.get_exp()
                m =  Message(self.unique_id, sender, MessagePerformative.INFORM_REF, self.current_value)
                self.send_message(m)

    

class TestModel(Model):
    """ TestModel which inherit from Model to test CommunicatingAgent and MessageService.
    """
    def __init__(self):
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)
        for i in range(2):
            a = TestAgent(i, self, "Agent" + str(i))
            self.schedule.add(a)
        self.running = True

    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step()

class ABCModel(Model):
    """Model for A-B-C example"""
    def __init__(self):
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)
        self.running = True
    
    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step()

if __name__ == "__main__":
    # print("*---- Testing communication package ----")
    # print("*")
    # print("* 1) Testing Mailbox receive & get methods")

    # mailbox = Mailbox()
    # m1 = Message("Agent1", "Agent2", MessagePerformative.PROPOSE, "Bonjour")
    # m2 = Message("Agent1", "Agent2", MessagePerformative.ACCEPT, "Hello")
    # m3 = Message("Agent2", "Agent1", MessagePerformative.ARGUE, "Buenos Dias")

    # mailbox.receive_messages(m1)
    # mailbox.receive_messages(m2)

    # assert(len(mailbox.get_new_messages()) == 2)
    # print("*     get_new_messages() => OK")
    # assert(len(mailbox.get_messages()) == 2)
    # print("*     get_messages() => OK")

    # mailbox.receive_messages(m3)
    # assert(len(mailbox.get_messages()) == 3)
    # assert(len(mailbox.get_messages_from_exp("Agent1")) == 2)
    # print("*     get_messages_from_exp() => OK")
    # assert(len(mailbox.get_messages_from_performative(MessagePerformative.ACCEPT)) == 1)
    # assert(len(mailbox.get_messages_from_performative(MessagePerformative.PROPOSE)) == 1)
    # assert(len(mailbox.get_messages_from_performative(MessagePerformative.ARGUE)) == 1)
    # print("*     get_messages_from_performative() => OK")

    # print("* 2) Testing CommunicatingAgent & MessageService")

    # communicating_model = TestModel()

    # assert(len(communicating_model.schedule.agents) == 2)
    # print("*     get the number of CommunicatingAgent => OK")

    # agent0 = communicating_model.schedule.agents[0]
    # agent1 = communicating_model.schedule.agents[1]

    # assert(agent0.get_name() == "Agent0")
    # assert(agent1.get_name() == "Agent1")
    # print("*     get_name() => OK")

    # agent0.send_message(Message("Agent0", "Agent1", MessagePerformative.COMMIT, "Bonjour"))
    # agent1.send_message(Message("Agent1", "Agent0", MessagePerformative.COMMIT, "Bonjour"))
    # agent0.send_message(Message("Agent0", "Agent1", MessagePerformative.COMMIT, "Comment ça va ?"))

    # assert(len(agent0.get_new_messages()) == 1)
    # assert(len(agent1.get_new_messages()) == 2)
    # assert(len(agent0.get_messages()) == 1)
    # assert(len(agent1.get_messages()) == 2)
    # print("*     send_message() & dispatch_message (instant delivery) => OK")

    # MessageService.get_instance().set_instant_delivery(False)

    # agent0.send_message(Message("Agent0", "Agent1", MessagePerformative.COMMIT, "Bonjour"))
    # agent1.send_message(Message("Agent1", "Agent0", MessagePerformative.COMMIT, "Bonjour"))
    # agent0.send_message(Message("Agent0", "Agent1", MessagePerformative.COMMIT, "Comment ça va ?"))

    # assert(len(agent0.get_messages()) == 1)
    # assert(len(agent1.get_messages()) == 2)

    # communicating_model.step()

    # assert(len(agent0.get_new_messages()) == 1)
    # assert(len(agent1.get_new_messages()) == 2)
    # assert(len(agent0.get_messages()) == 2)
    # assert(len(agent1.get_messages()) == 4)
    # print("*     send_message() & dispatch_messages => OK")


    print("Implementing Alice-Bob-Charles example")

    myModel = ABCModel()

    alice_prefered_value = 1

    bob_prefered_value = 2

    a = AliceOrBob(0,myModel,0, alice_prefered_value)
    b = AliceOrBob(1,myModel,1, bob_prefered_value)
    c = Charles(2,myModel,2)

    for agent in [a,b,c]:
        myModel.schedule.add(agent)

    for step in range(100):
        myModel.step()
        print(f"Alice happiness is {a.is_happy}")
        print(f"Bob happiness is {b.is_happy}")
        print(f"Charles value is {c.current_value}")

    