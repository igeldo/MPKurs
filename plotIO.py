import os
import csv
import pandas as pd

import matplotlib.pyplot as plt


if __name__ == '__main__':

    OUTPATH = 'out'
    FILENAME = 'test2.csv'
    SAVE = False

    # read layers
    layers = []
    with open(os.path.join(OUTPATH, FILENAME), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if '#' in row[0]:
                layers.append((row[1:]))

    # read photon data
    df = pd.read_csv(
        os.path.join(OUTPATH, FILENAME), sep=';', header=0, skip_blank_lines=True, comment='#'
    )
    
    # https://stackoverflow.com/questions/58342419/show-direction-arrows-in-a-scatterplot

    runaways = df.where(df['exits'] == 1).dropna()

    fig, ax = plt.subplots(dpi=200)
    df.plot.scatter(x='x', y='z', s=2, c='weight', colormap='viridis', ax=ax)
    ax.quiver(0,0,0,1, angles="xy", pivot="tip", color='black', alpha=1)
    if not runaways.empty:
        ax.quiver(runaways['x'].values, runaways['z'].values, runaways['ux'].values, runaways['uz'].values,
                  angles="xy", pivot="tail", color='black', alpha=1
                  )
    ylims = ax.get_ylim()
    plt.xlabel('x in mm')
    plt.ylabel('z in mm')

    borders = []
    for layer in layers[1:-1]:
        borders.append(float(layer[0]))
    borders.append(round(float(ylims[1]), 2))

    last_border = 0
    colors = ['b', 'r', 'g', 'y']
    for layer, c in zip(borders, colors):
        plt.axhspan(last_border, layer, color=c, alpha=.1)
        last_border = layer

    plt.gca().invert_yaxis()

    # for l, layer in enumerate(layers_df):
    #     plt.axhline(
    #         layers_df.loc[l, 'd'],
    #         xmin=ax.get_xlim()[0],
    #         xmax=ax.get_xlim()[1],
    #         linestyle='--', alpha=.5)

    if SAVE:
        plt.savefig(os.path.join(OUTPATH, FILENAME))
    else:
        plt.show()

# TODO: - "heatmap" anzahl photon/tiefe, "heatmap" bzgl eindringtiefe
#
