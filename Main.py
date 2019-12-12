from Simulation import Simulation
import Parameters as par
import math
import imageio
import sys
import os


def get_dir():
    if not os.path.exists(par.save_path):
        os.system("mkdir " + par.save_path)
        os.system("touch " + par.output_path)
    else:
        print("Directory already exits, choose a new one.")
        sys.exit()


def set_new_path(path):
    par.save_path = path
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
    sim.run_simulation()
    generate_gif()
    #os.system("python3 GenerateVideo.py")

run_simulation()
