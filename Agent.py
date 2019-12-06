import Parameters as par

import random
import numpy as np


class Agent:

    def __init__(self, x0, y0, health):
        self.x = x0
        self.y = y0
        self.health = health
        self.time_to_symptomatic = None

    # Random move
    def move(self):
        done = False

        while not done:
            direction = random.randint(1, 4)

            if direction == 1 and not self.x == 0: # and par.cross_wall_coordinate - self.x > 0 and par.cross_wall_coordinate - self.x < - 0.5:
                self.x = self.x - 1
                done = True
            elif direction == 2 and not self.y == 0: # and par.cross_wall_coordinate - self.y > 0 and par.cross_wall_coordinate - self.y < - 0.5:
                self.y = self.y - 1
                done = True
            elif direction == 3 and not self.x == par.dimension - 1: # and par.cross_wall_coordinate - self.x > 0.5 and par.cross_wall_coordinate - self.x < 0:
                self.x = self.x + 1
                done = True
            elif direction == 4 and not self.y == par.dimension - 1: # and par.cross_wall_coordinate - self.y > 0.5 and par.cross_wall_coordinate - self.y < 0:
                self.y = self.y + 1
                done = True

    # TODO
    # initialize discrete
    # put in dict based on discrete x and y
    # in move
    # get dx and dy
    # update x and y
    # implement periodic boundries based on with area you're in
    #

    def get_position(self):
        return tuple([self.x, self.y])

    def get_health(self):
        return self.health

    def recover(self):
        self.health = 'r'

    def infect(self, time_step):
        self.health = 'e'
        incubation_time = par.mean_incubation_time + 10 * np.random.normal() + 1
        if incubation_time < 1:
            incubation_time = 1
        self.time_to_symptomatic = time_step + incubation_time

    def becomes_symptomatic(self, time_step):
        if self.time_to_symptomatic <= time_step:
            self.health = 'i'
            return True
        return False
