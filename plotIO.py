import os
import csv
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


#if __name__ == '__main__':
def plot(filename, save=True, runaways=True, trace=False):
    OUTPATH = 'out'
    FILENAME = filename
    SAVE = save
    PLOT_RUNAWAYS = runaways
    TRACE = trace

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
    if TRACE:
        df.plot.line(x='x', y='z', ax=ax, color='k', linewidth=0.2, linestyle='dashed')
    df.plot.scatter(x='x', y='z', s=2, c='weight', colormap='viridis', ax=ax)  # plot photon paths
    if not runaways.empty and PLOT_RUNAWAYS:
        ax.quiver(runaways['x'].values, runaways['z'].values, runaways['ux'].values, runaways['uz'].values,
                  angles="xy", pivot="tail", color='black', alpha=1
                  )  # plot runaways
    ax.quiver(0, 0, 0, 1, angles="xy", pivot="tip", color='red', alpha=1)  # plot entry point

    ylims = ax.get_ylim()
    xlims = ax.get_xlim()
    plt.xlabel('x in mm')
    plt.ylabel('z in mm')

    last_border = 0
    colors = ['b', 'r', 'g', 'y']
    legend_elements = []
    for layer, c in zip(layers[1:], colors):
        plt.axhspan(last_border, layer[0], color=c, alpha=.1)   # plot layer backgrounds
        legend_elements.append(
            Line2D([0], [0], color=c, lw=4, alpha=.3,
                   label="$n$: {:.2f}, $g$: {:.2f},\n$\mu_a$: {:.2f}, $\mu_s$: {:.2f}".format(layer[1], layer[4], layer[2], layer[3]))
        )  # create layer legend elements
        last_border = layer[0]

    plt.ylim(-0.2, ylims[1])
    plt.gca().invert_yaxis()
    ax.legend(handles=legend_elements, loc='upper center',
              bbox_to_anchor=(0.5, -0.15), ncol=2,
              fancybox=True, shadow=True)
    plt.tight_layout()

    if SAVE:
        plt.savefig(os.path.splitext(os.path.join(OUTPATH, FILENAME))[0], dpi=300)
        plt.show(dpi=300)
    else:
        plt.show(dpi=300)
