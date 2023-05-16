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
    with open(os.path.join(OUTPATH,FILENAME), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if '#' in row[0]:
                layers.append((row[1:]))

    # read photon data
    df = pd.read_csv(
        os.path.join(OUTPATH, FILENAME), sep=';', header=0, skip_blank_lines=True, comment='#'
    )
    
    # https://stackoverflow.com/questions/58342419/show-direction-arrows-in-a-scatterplot
    
    x = df['x'].values
    y = df['y'].values
    z = df['z'].values
    w = df['weight'].values

    ux = df['ux'].values
    uy = df['uy'].values
    uz = df['uz'].values

    fig, ax = plt.subplots(dpi=200)
    df.plot.scatter(x='x', y='z', s=2, c='weight', colormap='viridis', ax=ax)
    #ax.quiver(x, z, ux, uz, angles="xy", pivot="mid", color='black', alpha=0.3)
    ylims = ax.get_ylim()
    plt.xlabel('x in mm')
    plt.ylabel('z in mm')

    #layers_df.apply(lambda row: layers_df.loc[row.name,'d'], axis=1)
    #plt.axhline(layers_df['z'], linestyle = '--', alpha = .5)

    borders = []
    for layer in layers[1:-1]:
        borders.append(float(layer[0]))
    borders.append(round(float(ylims[1]), 2))

    last_border=0
    colors=['b','r','g']
    for layer, c in zip(borders, colors):
        plt.axhspan(last_border, layer, color=c, alpha=.1)
        last_border = layer



    # plt.axhspan(0, 0.2, color='b', alpha=.5)
    # plt.axhspan(0.2, 0.5, color='r', alpha=.5)
    # plt.axhspan(0.5, ylims[1], color='g', alpha=.5)

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
