import matplotlib.pyplot as plt
import os
import numpy as np


def PercentPerGeneration(best, worst, average):
    if not os.path.isfile("log.txt"):
        newFile = open("log.txt", "w")
        newFile.write(" ".join(best) + "\n")
        newFile.write(" ".join(worst) + "\n")
        newFile.write(" ".join(average) + "\n")
    save_graph("best",best)
    save_graph("worst",worst)
    save_graph("average",average)


def save_graph(name, array):
    fig, ax = plt.subplots()
    x_values = list(range(len(array)))
    ax.set_xlabel("genertion")
    ax.set_ylabel(name + " score")
    ax.plot(x_values, array)

    plt.ylim(0, 100)
    plt.yticks(range(0, int(max(array)), 50))
    plt.xlim(0, len(array))
    plt.xticks(range(0, len(array), 50))

    plt.savefig(name + ".png")
    plt.clf()
    plt.close()

