import Parameters as par

import random
import numpy as np


class Agent:

    def __init__(self, x0, y0, health):
        self.x = x0
        self.y = y0
        self.health = health
        self.time_to_symptomatic = None

    def move(self):
        direction = random.randint(1, 4)
        x_area, y_area = self.get_area_code()

        if direction == 1:
            self.x = np.mod(self.x - x_area * par.boundary - 1, par.boundary) + x_area * par.boundary
        elif direction == 2:
            self.y = np.mod(self.y - y_area * par.boundary - 1, par.boundary) + y_area * par.boundary
        elif direction == 3:
            self.x = np.mod(self.x - x_area * par.boundary + 1, par.boundary) + x_area * par.boundary
        elif direction == 4:
            self.y = np.mod(self.y - y_area * par.boundary + 1, par.boundary) + y_area * par.boundary

    def move_without_boundary(self):
        done = False

        while not done:
            direction = random.randint(1, 4)

            if direction == 1 and not self.x == 0:
                self.x = self.x - 1
                done = True
            elif direction == 2 and not self.y == 0:
                self.y = self.y - 1
                done = True
            elif direction == 3 and not self.x == par.dimension - 1:
                self.x = self.x + 1
                done = True
            elif direction == 4 and not self.y == par.dimension - 1:
                self.y = self.y + 1
                done = True

    def get_area_code(self):
        if self.x < par.boundary:
            x_area = 0
        else:
            x_area = 1
        if self.y < par.boundary:
            y_area = 0
        else:
            y_area = 1
        return x_area, y_area

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
        if par.mean_incubation_time == 0:
            self.time_to_symptomatic = time_step

    def becomes_symptomatic(self, time_step):
        if self.time_to_symptomatic <= time_step:
            self.health = 'i'
            return True
        return False
