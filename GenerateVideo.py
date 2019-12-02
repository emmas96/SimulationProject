import Parameters as par
import imageio
import os


def make_gif():
    n_frames = len(os.listdir(par.save_path))
    frames = list()
    t = par.plot_step
    while len(frames) < n_frames:
        frames.append('t' + str(t) + '.png')
        t = t + par.plot_step

    images = []
    for frame in frames:
        path = os.path.join(par.save_path, frame)
        images.append(imageio.imread(path))
    path = os.path.join(par.save_path, par.save_path + '.gif')
    imageio.mimsave(path, images)


make_gif()

