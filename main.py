import os
import csv
from model import Tissue, PhotonPack, WEIGHT
import numpy as np

from plotIO import plot

np.random.seed(42)


# random seeds of interest
# 17: casual
# 42, ab 3 Stk: photon exiting top direction


def calcCritAngles(layer_list):
    for l, layer in enumerate(layer_list[1:-2]):
        n1 = layer_list[l].n  # this layer
        n2 = layer_list[l - 1].n  # previous upwards layer
        if n1 > n2:
            layer.cos_crit0 = np.sqrt(
                1.0 - n2 * n2 / (n1 * n1))  # crit0 upwards; sqrt instead of sine because it is faster
        else:
            layer.cos_crit0 = 0

        n2 = layer_list[l + 1].n  # next layer downwards
        if n1 > n2:
            layer.cos_crit1 = np.sqrt(1.0 - n2 * n2 / (n1 * n1))  # crit1 downwards
        else:
            layer.cos_crit1 = 0


if __name__ == '__main__':

    # define IOfiles
    OUTPATH = 'out'
    FILENAME = 'test2.csv'

    # create photons
    NUM_PHOTONS = 10
    photons = list()
    for p in range(0, NUM_PHOTONS):  # number of photons to simulate
        photons.append(PhotonPack(stepSize=0.01, w=1))

    # create layers
    layer1 = Tissue(z0=0, z1=0.2, n=1, mua=1, mus=100, g=0.9)
    layer2 = Tissue(z0=0.2, z1=0.5, n=1.37, mua=1, mus=100, g=0.9)
    layer3 = Tissue(z0=0.5, z1=4, n=1.37, mua=1, mus=100, g=0.9)
    layer4 = Tissue(z0=4, z1=4.2, n=1.37, mua=1, mus=100, g=0.9)

    layers = [layer1, layer2, layer3]

    # calculate critical angles one time for given layers
    calcCritAngles(layers)

    # create output
    if not os.path.exists(os.path.join(OUTPATH)):
        os.makedirs(os.path.join(OUTPATH))
    outfile = open(os.path.join(OUTPATH, FILENAME), 'w', newline='')
    writer = csv.writer(outfile, delimiter=';')

    # write layer specifications
    writer.writerow(['#', 'd', 'n', 'mu_a', 'mu_s', 'g'])
    for layer in layers:
        writer.writerow(['#', layer.z1, layer.n, layer.mua, layer.mus, layer.g])

    # write photon header
    writer.writerow(['x', 'y', 'z', 'ux', 'uy', 'uz', 'layer', 'weight', 'dead', 'exits'])

    for p in photons:
        while p.alive():
            layers[p._layer].calcStepSize(p)
            layers[p._layer].hop(p)
            layers[p._layer].absorption(p)
            layers[p._layer].scatter(p)
            writer.writerow(p.__repr__())

            if p._w < WEIGHT:
                p.roulette()

            if layers[p._layer].hitBoundry(p):  # and hitBoundry(p)==1
                layers[p._layer].hop(p)  # swapped hop and cross or not, smart!!! es muss erst noch der restliche weg im alten layer zurück gelegt werden (bis zur grenze des layers) und dann kann der layer erhöht werden
                layers[p._layer].crossOrNot(p, layers)
            writer.writerow(p.__repr__())

    outfile.close()
    plot()
