import Parameters as par
from Agent import Agent

import random
import time
import numpy as np
import sys


class Simulation:

    def __init__(self):
        self.population = {}

        self.day = True
        self.time_step = 0

        self.population_size = 0

        self.count = {'s': 0, 'i': 0, 'r': 0}

    def run_simulation(self):
        tic = time.time()
        self.initialize_population()
        self.start_plague()
        print('Number of individuals initially infected: {}'.format(self.count['i']))

        done = False
        while not done:
            self.time_step = self.time_step + 1
            self.move_population()
            self.air_transportation()
            self.disease_development()

            if self.count['i'] == 0:
                done = True
                print('Time: {}'.format(self.time_step))
                print('Success: Virus defeated, {} people survived'.format(self.population_size))
                print(self.population)
                print(self.get_population_size())
                toc = time.time()
                print('Computing time: ' + str(toc - tic))
            elif self.population_size == 0:
                done = True
                print('Time: {}'.format(self.time_step))
                print('Fail: Entire population has died')
                print(self.population)
                print(self.get_population_size())
                toc = time.time()
                print('Computing time: ' + str(toc - tic))
            elif self.count['i'] == self.population_size:
                print('Bad sign: Entire population is infected')
            elif np.mod(self.time_step, 1000) == 0:
                print('Time: {}'.format(self.time_step))

    # Initialize population with N susceptible agents
    def initialize_population(self):
        for n in range(par.N):
            # Initialize at random position
            x = random.randint(0, par.dimension - 1)
            y = random.randint(0, par.dimension - 1)
            agent = Agent(x, y, 's')
            self.add_agent(agent)

        self.population_size = par.N


    # Insert agent into population
    def add_agent(self, agent):
        position = agent.get_position()
        health = agent.get_health()
        local_population = self.population.get(position, 0)

        if local_population == 0:
            new_local_population = {'s': [], 'i': [], 'r': [], 'count': 0}
            new_local_population[health].append(agent)
        else:
            local_population[health].append(agent)
            new_local_population = local_population

        new_local_population['count'] = new_local_population['count'] + 1
        self.count[health] = self.count[health] + 1

        self.population.update({position: new_local_population})

    # Remove agent from population
    def remove_agent(self, agent):
        position = agent.get_position()
        health = agent.get_health()

        local_population = self.population.get(position)
        local_population[health].pop(local_population[health].index(agent))

        local_population['count'] = local_population['count'] - 1
        self.count[health] = self.count[health] - 1

        self.population.update({position: local_population})

    # Only for debugging!
    def get_population_size(self):
        count = 0
        for position in self.population.keys():
            local_count = self.population.get(position).get('count')
            count = count + local_count
        return count

    # Start plague at most dense location
    def start_plague(self):
        init_position = self.get_most_dense_area()
        self.infect_location(init_position)

    # Infect all agents at a certain location
    def infect_location(self, position):
        local_population = self.population.get(position)

        self.count['i'] = self.count['i'] + len(local_population['s'])
        self.count['s'] = self.count['s'] - len(local_population['s'])

        for agent in local_population['s']:
            agent.infect(self.time_step)

        if local_population['i']:
            local_population['i'].extend(local_population['s'])
        else:
            local_population['i'] = local_population['s']
        local_population['s'] = []

        self.population.update({position: local_population})

    # Recover a single agent
    def recover_agent(self, agent):
        position = agent.get_position()
        local_population = self.population.get(position)
        local_population['i'].pop(local_population['i'].index(agent))
        local_population['r'].append(agent)
        agent.recover()

        self.count['i'] = self.count['i'] - 1

    def kill_agent(self, agent):
        position = agent.get_position()
        health = agent.get_health()

        local_population = self.population.get(position)
        local_population[health].pop(local_population[health].index(agent))

        self.population_size = self.population_size - 1

    def get_most_dense_area(self):
        most_dense_position = None
        highest_density = 0
        for position in self.population.keys():
            local_density = self.population.get(position)['count']
            if local_density > highest_density:
                most_dense_position = position
                highest_density = local_density

        return most_dense_position

    # Move all agents according to probability gamma
    def move_population(self):
        population_copy = self.population.copy()
        for position in population_copy.keys():
            local_population = self.population.get(position)
            agents = self.get_agents_from_location(local_population)

            for agent in agents:
                d = par.d

                # Change movement depending on sickness, 'zombie virus'
                if agent.get_health() == 'i':
                    if agent.is_symptomatic(self.time_step):
                        d = par.d_dying
                    else:
                        d = par.d_zombie

                r = random.random()
                if r < d:
                    self.remove_agent(agent)
                    agent.move()
                    self.add_agent(agent)

    def disease_development(self):
        population_copy = self.population.copy()
        for position in population_copy.keys():
            local_population = self.population.get(position)

            if local_population['i']:
                number_of_infected = len(local_population['i'])
                propability_of_infection = (1 - par.beta) ** number_of_infected

                r = random.random()
                if r < propability_of_infection:
                    self.infect_location(position)

                infected = local_population['i'].copy()
                for agent in infected:
                    r = random.random()
                    q = random.random()
                    if r < par.delta:
                        self.kill_agent(agent)
                    elif q < par.gamma:
                        self.recover_agent(agent)

    def get_agents_from_location(self, local_population):
        agents = []
        if local_population['s']:
            agents.extend(local_population['s'])
        if local_population['i']:
            agents.extend(local_population['i'])
        if local_population['r']:
            agents.extend(local_population['r'])
        return agents

    def air_transportation(self):
        all_travelling_agents = []
        for iAirport in range(par.n_airport):
            position = tuple(par.airport_location[iAirport])
            airport_population = self.population.get(position)

            if airport_population is None:
                airport_population = {'s': [], 'i': [], 'r': [], 'count': 0}

            agents = self.get_agents_from_location(airport_population)
            all_travelling_agents.extend(agents)

            roulette = par.airport_flow[iAirport]
            for agent in agents:
                r = random.random()
                for i in range(par.n_airport):
                    if r < roulette[i]:
                        self.remove_agent(agent)
                        agent.x = par.airport_location[i][0]
                        agent.y = par.airport_location[i][1]
                        break

        for agent in all_travelling_agents:
            self.add_agent(agent)

