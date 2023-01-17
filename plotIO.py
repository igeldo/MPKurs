import os
import csv

import pandas as pd

import matplotlib.pyplot as plt


if __name__ == '__main__':

    OUTPATH = 'out'
    FILENAME = 'test.csv'
    SAVE = False

    df = pd.read_csv(
        os.path.join(OUTPATH, FILENAME), sep=';', header=0
    )
    print(df['z'].head())
    fig, ax = plt.subplots(dpi=200)
    df.plot.scatter(x = 'y', y = 'z', s=0.1, c = 'weight', colormap='viridis', ax=ax)
    plt.xlabel('y [mm]')
    plt.ylabel('z [mm]')
    if SAVE:
        plt.savefig(os.path.join(OUTPATH, FILENAME))
    else:
        plt.show()

