import os
import csv
from model import Tissue, PhotonPack, WEIGHT
import numpy as np

np.random.seed(42)
# random seeds of interest
# 17: casual
# 42: photon exiting top direction

if __name__ == '__main__':

    # define IOfiles
    OUTPATH = 'out'
    FILENAME = 'test2.csv'

    # define params
    photon1 = PhotonPack(stepSize=1, w=1)
    photon2 = PhotonPack(stepSize=1, w=1)

    layer1 = Tissue(z0=0, z1=0.3, mua=1, mus=100, g=0.9, cos_crit0=0, cos_crit1=0)
    layer2 = Tissue(z0=0.3, z1=1.4, mua=1, mus=100, g=0.9, cos_crit0=0, cos_crit1=0)

    #
    layers = [layer1]
    photons = [photon1]

    # create output
    if not os.path.exists(os.path.join(OUTPATH)):
        os.makedirs(os.path.join(OUTPATH))
    outfile = open(os.path.join(OUTPATH, FILENAME), 'w', newline='')
    writer = csv.writer(outfile, delimiter=';')
    writer.writerow(['x', 'y', 'z', 'ux', 'uy', 'uz', 'layer', 'weight', 'dead'])

    # start sim
    #print(p.__repr__()) # TODO: check repr

    for p in photons:
        while not layers[p._layer].hitBoundry(p) and p.alive() == 0:
            layers[p._layer].hop(p)
            layers[p._layer].absorption(p)
            layers[p._layer].scatter(p)
            writer.writerow(p.__repr__())
            if p._w < WEIGHT and p.alive() == 0:
                p.roulette()

        if p.alive() == 0:
            layers[p._layer].hop(p) # swapped hop and cross or not, smart?
            layers[p._layer].crossOrNot(p, layers)
            writer.writerow(p.__repr__())

    # for i in range(0, 100):
    #     layer1.hop(photon1)
    #     layer1.absorption(photon1)
    #     layer1.scatter(photon1)
    #     writer.writerow(photon1.__repr__())
    #     #print(photon1)

    outfile.close()
