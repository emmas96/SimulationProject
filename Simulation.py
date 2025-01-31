import Parameters as par
from Agent import Agent
from PlotWindow import PlotWindow

import random
import time
import numpy as np
import sys
import os


class Simulation:

    def __init__(self):
        self.population = {}
        self.day = True
        self.time_step = 0
        self.population_size = 0
        self.count = {'s': 0, 'e': 0, 'i': 0, 'r': 0}
        self.plt_window = PlotWindow()

    def run_simulation(self):
        tic = time.time()
        self.initialize_population()
        self.start_plague()
        with open(par.output_path, "a") as f:
            f.write('Number of individuals initially exposed: {} \n'.format(self.count['e']))

        while True:
            if self.time_step % par.plot_step == 0:
                self.plt_window.update_simulation_plot(self.population, self.time_step, self.day)

            if par.limited_time and self.time_step >= par.T:
                s_count = self.plt_window.final_proportion_plot(self.time_step)
                toc = time.time()
                with open(par.output_path, "a") as f:
                    f.write('Simulation ended because of time out.\n')
                    f.write('{} susceptible, {} exposed, {} symptomatic, {} recovered and {} people survived in total.\n'.format(
                            self.count['s'], self.count['e'], self.count['i'], self.count['r'], self.population_size))
                    f.write('Computing time: {}\n'.format(toc - tic))
                return self.time_step, s_count

            self.get_next_simulation_step()
            self.plt_window.update_population_count(self.count)

            if self.count['e'] + self.count['i'] == 0:
                s_count = self.plt_window.final_proportion_plot(self.time_step)
                toc = time.time()
                with open(par.output_path, "a") as f:
                    f.write('Time: {}\n'.format(self.time_step))
                    f.write('Success: Virus defeated, {} people survived\n'.format(self.population_size))
                    f.write('{} susceptible, {} exposed, {} symptomatic, {} recovered and {} people survived in total.\n'.format(
                            self.count['s'], self.count['e'], self.count['i'], self.count['r'], self.population_size))
                    f.write('Computing time: {}\n'.format(toc - tic))
                return self.time_step, s_count
            elif self.population_size == 0:
                s_count = self.plt_window.final_proportion_plot(self.time_step)
                toc = time.time()
                with open(par.output_path, "a") as f:
                    f.write('Time: {}\n'.format(self.time_step))
                    f.write('Fail: Entire population has died\n')
                    f.write('Computing time: {}\n'.format(toc - tic))
                return self.time_step, s_count
            #elif self.count['e'] + self.count['i'] >= self.population_size:
            #    print('Bad sign: Entire population is infected')
            #if np.mod(self.time_step, 1000) == 0:
            #    print('Time: {}'.format(self.time_step))

    def get_next_simulation_step(self):
        self.time_step = self.time_step + 1
        self.update_day()

        self.move_population()
        self.air_transportation()
        self.disease_development()

        return self.population

    # Initialize population with N susceptible agents
    def initialize_population(self):
        for n in range(par.N):
            # Initialize at random position
            x = random.randint(0, par.dimension - 1)
            y = random.randint(0, par.dimension - 1)

            if par.not_start_at_airport:
                while [x, y] in par.airport_location:
                    x = random.randint(0, par.dimension - 1)
                    y = random.randint(0, par.dimension - 1)

            traveller_type = None
            if par.travellers:
                traveller_type = 0
                r = random.random()
                if r < par.traveller_ratio:
                    traveller_type = 1

            agent = Agent(x, y, 's', traveller_type)
            self.add_agent(agent)

        self.population_size = par.N

    # Insert agent into population
    def add_agent(self, agent):
        position = agent.get_position()
        health = agent.get_health()
        local_population = self.population.get(position, 0)

        if local_population == 0:
            new_local_population = {'s': [], 'e': [], 'i': [], 'r': [], 'count': 0}
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

        self.count['e'] = self.count['e'] + len(local_population['s'])
        self.count['s'] = self.count['s'] - len(local_population['s'])

        for agent in local_population['s']:
            agent.infect(self.time_step)

        if local_population['e']:
            local_population['e'].extend(local_population['s'])
        else:
            local_population['e'] = local_population['s']
        local_population['s'] = []

        self.population.update({position: local_population})

    def infect_agent(self, agent):
        position = agent.get_position()
        local_population = self.population.get(position)
        local_population['s'].pop(local_population['s'].index(agent))
        local_population['e'].append(agent)
        self.count['s'] = self.count['s'] - 1
        self.count['e'] = self.count['e'] + 1

    # Recover a single agent
    def recover_agent(self, agent):
        position = agent.get_position()
        health = agent.get_health()
        local_population = self.population.get(position)
        local_population[health].pop(local_population[health].index(agent))
        local_population['r'].append(agent)
        agent.recover()

        self.count[health] = self.count[health] - 1
        self.count['r'] = self.count['r'] + 1

    # Recover a single agent
    def make_agent_symptomatic(self, agent):
        position = agent.get_position()
        local_population = self.population.get(position)
        local_population['e'].pop(local_population['e'].index(agent))
        local_population['i'].append(agent)

        self.count['e'] = self.count['e'] - 1
        self.count['i'] = self.count['i'] + 1

    def kill_agent(self, agent):
        self.remove_agent(agent)
        self.population_size = self.population_size - 1
        self.plt_window.add_dead([agent.x, agent.y])

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
        if self.day:
            population_copy = self.population.copy()
            for position in population_copy.keys():
                local_population = self.population.get(position)
                agents = Simulation.get_agents_from_location(local_population)

                sym_ratio = len(local_population['i']) / len(local_population)

                for agent in agents:
                    d = par.d

                    health = agent.get_health()
                    if health == 'e':
                        d = par.d_exposed
                        if agent.becomes_symptomatic(self.time_step):
                            self.make_agent_symptomatic(agent)
                            d = par.d_symptomatic
                    elif health == 'i':
                        d = par.d_symptomatic

                    r = random.random()
                    if r < d and agent.traveller_type == 1:
                        self.move_agent(agent)
                    elif r < d and agent.traveller_type == 0 and sym_ratio > par.panic_threshold:
                        self.move_agent(agent)

    def move_agent(self, agent):
        self.remove_agent(agent)
        if par.boundary == 0:
            agent.move_without_boundary()
        else:
            agent.move()
        self.add_agent(agent)

    def disease_development(self):
        population_copy = self.population.copy()
        for position in population_copy.keys():
            local_population = self.population.get(position)

            if local_population['e'] or local_population['i']:
                if par.infect_all:
                    number_of_infected = len(local_population['e']) + len(local_population['i'])
                    probability_of_infection = (1 - par.beta) ** number_of_infected
                    r = random.random()
                    if r < probability_of_infection:
                        self.infect_location(position)
                else:
                    number_of_exposed = len(local_population['e'])
                    number_of_ill = len(local_population['i'])
                    #probability_of_infection = 1 - (1 - par.beta_exposed) * number_of_exposed * (1 - par.beta_ill) * number_of_ill
                    probability_of_infection = 1 - (1 - par.beta_exposed) ** number_of_exposed * (1 - par.beta_ill) ** number_of_ill
                    for agent in local_population['s']:
                        r = random.random()
                        if r < probability_of_infection:
                            agent.infect(self.time_step)
                            self.infect_agent(agent)

                infected = local_population['i'].copy()
                for agent in infected:
                    r = random.random()
                    q = random.random()
                    if r < par.delta:
                        self.kill_agent(agent)
                    elif q < par.gamma:
                        self.recover_agent(agent)

    @staticmethod
    def get_agents_from_location(local_population):
        agents = []
        if local_population['s']:
            agents.extend(local_population['s'])
        if local_population['e']:
            agents.extend(local_population['e'])
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
                airport_population = {'s': [], 'e': [], 'i': [], 'r': [], 'count': 0}

            agents = Simulation.get_agents_from_location(airport_population)
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

    def update_day(self):
        total_time = par.day_time + par.night_time
        check_time = self.time_step % total_time
        self.day = check_time < par.day_time

