import os

import pandas as pd

import matplotlib.pyplot as plt


if __name__ == '__main__':

    OUTPATH = 'out'
    FILENAME = 'test2.csv'
    SAVE = False

    df = pd.read_csv(
        os.path.join(OUTPATH, FILENAME), sep=';', header=0
    )
    
    # https://stackoverflow.com/questions/58342419/show-direction-arrows-in-a-scatterplot
    
    x = df['x'].values
    y = df['y'].values
    z = df['z'].values
    w = df['weight'].values

    # u = np.diff(x)
    # v = np.diff(y)
    # pos_x = x[:-1] + u/2
    # pos_y = y[:-1] + v/2
    # norm = np.sqrt(u**2+v**2)
    #
    # fig, ax = plt.subplots(dpi=200)
    # ax.scatter(x,y, marker="o", s=0.1)
    # ax.quiver(pos_x, pos_y, u/norm, v/norm, angles="xy", zorder=5, pivot="mid")
    # plt.xlabel("x [mm]")
    # plt.ylabel("y [mm]")
    # plt.show()

    ux = df['ux'].values
    uy = df['uy'].values
    uz = df['uz'].values

    # fig, ax = plt.subplots(dpi=200)
    # ax.scatter(x,z, marker="o", s=0.1)
    # ax.quiver(x, z, ux, uz, angles="xy", zorder=5, pivot="mid")
    # plt.gca().invert_yaxis()
    # plt.xlabel("x [mm]")
    # plt.ylabel("z [mm]")
    # plt.show()

    fig, ax = plt.subplots(dpi=200)
    df.plot.scatter(x='x', y='z', s=2, c='weight', colormap='viridis', ax=ax)
    ax.quiver(x, z, ux, uz, angles="xy", pivot="mid", color='black', alpha=0.3)
    plt.gca().invert_yaxis()
    plt.xlabel('x [mm]')
    plt.ylabel('z [mm]')
    if SAVE:
        plt.savefig(os.path.join(OUTPATH, FILENAME))
    else:
        plt.show()
