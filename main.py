import os
import csv
from model import Tissue, PhotonPack, calcCritAngles, WEIGHT
import numpy as np

from plotIO import plot

np.random.seed(42)

if __name__ == '__main__':

    # define IOfiles
    OUTPATH = 'out'


    # create photons
    NUM_PHOTONS = 1
    photons = list()
    for photon in range(0, NUM_PHOTONS):  # number of photons to simulate
        photons.append(PhotonPack())

    # create layers
    layer1 = Tissue(z0=0, z1=0.2, n=0.1, mua=1, mus=25, anisotropy=0.9)
    layer2 = Tissue(z0=0.2, z1=0.5, n=1.2, mua=1, mus=25, anisotropy=0.9)
    layer3 = Tissue(z0=0.5, z1=4, n=1, mua=1, mus=100, anisotropy=0.9)
    layer4 = Tissue(z0=4, z1=4.2, n=1.37, mua=1, mus=100, anisotropy=0.9)

    layers = [layer1, layer2]

    FILENAME = f'{NUM_PHOTONS}p_{len(layers)}l6.csv'

    # calculate critical angles one time for given layers
    calcCritAngles(layers)

    # create output
    if not os.path.exists(os.path.join(OUTPATH)):
        os.makedirs(os.path.join(OUTPATH))
    outfile = open(os.path.join(OUTPATH, FILENAME), 'w', newline='')
    writer = csv.writer(outfile, delimiter=';')

    # write layer specifications
    writer.writerow(['#', 'd', 'n', 'mu_a', 'mu_s', 'anisotropy'])
    for layer in layers:
        writer.writerow(['#', layer.z1, layer.n, layer.mua, layer.mus, layer.anisotropy])

    # write photon header
    writer.writerow(['x', 'y', 'z', 'ux', 'uy', 'uz', 'layer', 'weight', 'dead', 'exits'])

    for photon in photons:
        while photon.alive():
            layers[photon.layer].calcStepSize(photon)
            layers[photon.layer].hop(photon)
            layers[photon.layer].absorption(photon)
            layers[photon.layer].scatter(photon)
            writer.writerow(photon.__repr__())

            if photon.weight < WEIGHT:
                photon.roulette()

            if layers[photon.layer].hitBoundary(photon) and photon.alive():  # and hitBoundary(photon)==1
                layers[photon.layer].hop(photon)  # swapped hop and cross or not, smart!!! es muss erst noch der restliche weg im alten layer zurück gelegt werden (bis zur grenze des layers) und dann kann der layer erhöht werden
                layers[photon.layer].crossOrNot(photon, layers)
            writer.writerow(photon.__repr__())

    outfile.close()
    plot(FILENAME, trace=True, save=True)
