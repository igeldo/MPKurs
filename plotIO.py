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

    # convert strings into floats
    for layer in layers[1:]:
        for i in layer:
            layer[layer.index(i)] = float(i)

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

    last_border = 0
    colors = ['b', 'r', 'g', 'y']
    for layer, c in zip(layers[1:], colors):
        plt.axhspan(last_border, layer[0], color=c, alpha=.1)
        last_border = layer[0]

    plt.ylim(ylims)
    plt.gca().invert_yaxis()

    if SAVE:
        plt.savefig(os.path.join(OUTPATH, FILENAME))
    else:
        plt.show()

# TODO: - "heatmap" anzahl photon/tiefe, "heatmap" bzgl eindringtiefe
#
