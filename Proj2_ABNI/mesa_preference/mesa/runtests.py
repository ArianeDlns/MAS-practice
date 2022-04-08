from pw_argumentation import *

if __name__ == "__main__":
    # Run the tests
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
    agent_two.send_message(Message(agent_two.get_name(
    ), agent_one.get_name(), MessagePerformative.PROPOSE, electric_engine))

    # Run the model on 10 steps
    step = 0
    while step < 10:
        argument_model.step()
        step += 1

