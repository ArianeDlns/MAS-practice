from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Sheep:
        portrayal = {"Shape": "prey_predator/icons/sheep_icon.png",
                 "scale": 0.9,
                 "Layer": 1}

    elif type(agent) is Wolf:
        portrayal = {"Shape": "prey_predator/icons/wolf_icon.png",
                 "scale" : 0.9,
                 "Layer": 2}

    elif type(agent) is GrassPatch:
        if agent.grown:
            portrayal = {"Shape": "rect",
                    "Color": "#00aa00",
                    "Filled": "true",
                    "Layer": 0,
                    "w": 1,
                    "h": 1}
        else:
            portrayal = {"Shape": "rect",
                    "Color": "#55ff55",
                    "Filled": "true",
                    "Layer": 0,
                    "w": 1,
                    "h": 1}

    return portrayal






height = 20
width = 20
initial_sheep = UserSettableParameter('slider', 'Initial sheep', value=50, min_value=10, max_value=200, step=1)
initial_wolves = UserSettableParameter('slider', 'Initial wolves', value=20, min_value=1, max_value=100, step=1)
sheep_reproduce =  UserSettableParameter('slider', 'Sheep reproduce', value=0.06, min_value=0, max_value=1, step=0.01)
wolf_reproduce =  UserSettableParameter('slider', 'Wolf reproduce', value=0.05, min_value=0, max_value=1, step=0.01)
wolf_gain_from_food = UserSettableParameter('slider', 'Wolf gains from food', value=10, min_value=0, max_value=100, step=1)
grass = UserSettableParameter('checkbox', 'Grass', value=True)
grass_regrowth_time = UserSettableParameter('slider', 'Grass regrowth time', value=30, min_value=1, max_value=100, step=1)
sheep_gain_from_food = UserSettableParameter('slider', 'Sheep gains from food', value=10, min_value=0, max_value=100, step=1)

canvas_element = CanvasGrid(wolf_sheep_portrayal, height, width, 500, 500)
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": "#AA0000"}, {"Label": "Sheep", "Color": "#666666"}]
)

model_params = {
    "height":height,
    "width":width,
    "initial_sheep":initial_sheep,
    "initial_wolves":initial_wolves,
    "sheep_reproduce":sheep_reproduce,
    "wolf_reproduce":wolf_reproduce,
    "wolf_gain_from_food":wolf_gain_from_food,
    "grass":True,
    "grass_regrowth_time":grass_regrowth_time,
    "sheep_gain_from_food":sheep_gain_from_food,

}

server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8521
