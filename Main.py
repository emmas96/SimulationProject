from Simulation import Simulation
import Parameters as par
import sys
import os


def get_dir():
    if not os.path.exists(par.save_path):
        os.system("mkdir " + par.save_path)
    else:
        print("Directory already exits, choose a new one.")
        sys.exit()


get_dir()
sim = Simulation()
sim.run_simulation()
