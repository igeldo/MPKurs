import os
import csv

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


if __name__ == '__main__':

    OUTPATH = 'out'
    FILENAME = 'test.csv'
    SAVE = False

    df = pd.read_csv(
        os.path.join(OUTPATH, FILENAME), sep=';', header=0
    )
    
    x = df['x'].values
    y = df['y'].values
    u = df['ux'].values
    v = df['uy'].values
    w = df['weight'].values
    
    # u = np.diff(x)
    # v = np.diff(y)
    
    # pos_x = x[:-1] + u/2
    # pos_y = y[:-1] + v/2
    # norm = np.sqrt(u**2+v**2) 
    
    fig, ax = plt.subplots(dpi=200)
    ax.plot(x,y, marker="o")
    ax.quiver(x, y, u, v, angles="xy", zorder=5, pivot="mid")
    plt.show()
    
    # print(df['z'].head())
    # fig, ax = plt.subplots(dpi=200)
    # df.plot.scatter(x = 'y', y = 'z', s=0.1, c = 'weight', colormap='viridis', ax=ax)
    # plt.xlabel('y [mm]')
    # plt.ylabel('z [mm]')
    # if SAVE:
    #     plt.savefig(os.path.join(OUTPATH, FILENAME))
    # else:
    #     plt.show()

