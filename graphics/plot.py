import matplotlib.pyplot as plt
import numpy as np
import os


def plot():
    data = [66, 68, 76, 74]
    # plt.hist(data, bins=[0.001, 0.01, 0.1, 0.15]))

    # fig = plt.figure()
    fig, ax = plt.subplots()

    # manually plug these numbers in. These numbers come from results documented at
    # https://docs.google.com/spreadsheets/d/1VHnBQxjCSiNHenB_PuUABOYHCSfrxBhYpFQ7wKoQWDc/edit?usp=sharing
    # (must have a Harvard gmail account to access)
    density = ['0.001', '0.01', '0.1', '0.15']
    data = [66, 68, 76, 74]
    ax.bar(density, data)
    ax.set_ylabel('Casualties aided')
    ax.set_xlabel('Point generation density (points/unit^2)')
    ax.set_title('PSM Density vs. Casualties')

    # save
    plt.savefig(os.getcwd() + "/plot_casualties.png")


    fig, ax = plt.subplots()
    density = ['0.001', '0.01', '0.1', '0.15']
    runtimes = [6.98, 13.94, 146.66, 585.36]
    ax.bar(density, runtimes)
    ax.set_ylabel('Runtime (seconds)')
    ax.set_xlabel('Point generation density (points/unit^2)')
    ax.set_title('PSM Density vs. Runtime')

    # save
    plt.savefig(os.getcwd() + "/plot_runtime.png")


    fig, ax = plt.subplots()
    data = [[58, 75],
            [80, 81],
            [82, 82]]
    X = np.arange(2)





    # ax = fig.add_axes([0,0,1,1])

    plt.axis([-0.5, 2, 50, 90])


    ax.bar(X + 0.00, data[0], color = 'b', width = 0.25)
    ax.bar(X + 0.25, data[1], color = 'g', width = 0.25)
    ax.bar(X + 0.50, data[2], color = 'r', width = 0.25)

    ax.set_xticks(X, ('0.01', '0.1'))
    ax.legend(labels=['PSM', 'Standard', 'Control'])


    ax.set_ylabel('Casualties collected')
    ax.set_xlabel('Point generation density (points/unit^2)')
    ax.set_title('Casualties collected by algorithm, different PSM densities')

    # save
    plt.savefig(os.getcwd() + "/plot_runtime.png")

plot()
