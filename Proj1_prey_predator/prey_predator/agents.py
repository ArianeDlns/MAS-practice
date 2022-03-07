from mesa import Agent
from prey_predator.random_walk import RandomWalker
import random


class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.unique_id = unique_id
        self.pos = pos
        self.model = model
        self.moore = moore
        self.energy = energy

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        #moving
        self.random_move()
        self.energy -= 1
        #eating
        if self.model.grass: #allow sheep to eat grass or not
            same_cell_agents = self.model.grid.get_cell_list_contents([self.pos])
            for agent in same_cell_agents :
                if type(agent) == GrassPatch :
                    if agent.grown:
                        agent.grown = False
                        self.energy += self.model.sheep_gain_from_food
        #reproduce 
        p = random.random()
        if p < self.model.sheep_reproduce:
            self.energy = self.energy//2 #divide energy by 2 if reproducing
            sheep_agent = Sheep(self.model.unique_id, self.pos, self.model, True, energy = self.energy)
            self.model.unique_id += 1
            self.model.schedule.add(sheep_agent)
            self.model.grid.place_agent(sheep_agent, self.pos)
        #die if no energy
        if self.energy < 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)

        self.unique_id = unique_id
        self.pos = pos
        self.model = model
        self.moore = moore
        self.energy = energy

    def step(self):
        #moving
        self.random_move()
        self.energy -= 1
        #eating
        same_cell_agents = self.model.grid.get_cell_list_contents([self.pos])
        for a in same_cell_agents : 
            if type(a) == Sheep:
                self.model.grid.remove_agent(a)
                self.model.schedule.remove(a)
                self.energy += self.model.wolf_gain_from_food
                break #Only eat one sheep
        #reproduce 
        p = random.random()
        if p < self.model.wolf_reproduce:
            self.energy = self.energy//2
            wolf_agent = Wolf(self.model.unique_id, self.pos, self.model, True, energy = self.energy)
            self.model.unique_id += 1
            self.model.schedule.add(wolf_agent)
            self.model.grid.place_agent(wolf_agent, self.pos)
        #die if no energy
        if self.energy < 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)


class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.pos = pos
        self.model = model
        self.grown = fully_grown
        self.countdown = countdown
        self.count = 0

    def step(self):
        if not self.grown:
            self.count = (self.count + 1) % self.countdown
            if self.count == 0 :
                self.grown = True
