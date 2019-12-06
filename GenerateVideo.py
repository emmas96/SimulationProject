import Parameters as par
import imageio
import os
import sys


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


path = os.path.join(par.save_path, par.save_path + '.gif')
if os.path.exists(path):
    print("Save path already exits, choose a new one.")
    sys.exit()
make_gif(path)

