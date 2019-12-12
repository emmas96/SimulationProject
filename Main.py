from Simulation import Simulation
import Parameters as par
import math
import imageio
import sys
import os
import numpy as np
import matplotlib.pyplot as plt


def get_dir():
    if not os.path.exists(par.save_path):
        os.system("mkdir " + par.save_path)
        os.system("touch " + par.output_path)
    else:
        print("Directory already exits, choose a new one.")
        sys.exit()


def set_new_path(path):
    par.save_path = path
    print(par.save_path)
    par.output_path = par.save_path + '_output.txt'


def make_gif(path):
    n_frames = len(os.listdir(par.save_path))
    frames = list()
    t = 0
    while len(frames) < n_frames:
        frames.append('t' + str(t) + '.png')
        t = t + par.plot_step

    images = []
    for frame in frames:
        frame_path = os.path.join(par.save_path, frame)
        images.append(imageio.imread(frame_path))
    imageio.mimsave(path, images)


def generate_gif():
    path = os.path.join(par.save_path, par.save_path + '.gif')
    if os.path.exists(path):
        print("Save path already exits, choose a new one.")
        sys.exit()
    make_gif(path)


def set_par_baseline():
    par.dimension = 100
    par.N = 1000

    par.d = 0.8
    par.d_exposed = par.d
    par.d_symptomatic = par.d

    par.night_time = 0

    par.mean_incubation_time = 0

    par.beta = 0.6
    par.gamma = 0.01
    par.delta = 0

    par.n_airport = 0

    par.boundary = 0

    par.infect_all = True


def run_simulation():
    get_dir()
    sim = Simulation()
    time, count = sim.run_simulation()
    if par.plot_grid:
        generate_gif()
    return time, count


def test_ratios():
    n_iterations = 10
    ratios = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
    susceptible_count = []
    for ratio in ratios:
        count = 0
        for i in range(n_iterations):
            set_new_path('ratio_{}'.format(int(ratio * 100)))
            par.traveller_ratio = ratio
            sim = Simulation()
            time, s0 = sim.run_simulation()
            count = count + s0
            if time < par.T:
                print('Earlier stop')
            print('Done with ratio = {}'.format(ratio))
        susceptible_count.append(count/n_iterations)

    plt.plot(ratios, susceptible_count)
    plt.xlabel('Ratio of travellers')
    plt.ylabel('Hours')
    plt.title('Time until every individual has been exposed')
    path = par.save_path + '_final_susceptible_0_vs_ratio'
    plt.savefig(path)
    plt.close()

#test_ratios()
run_simulation()


