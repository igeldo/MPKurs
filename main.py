import os
import csv
from model import Tissue, PhotonPack, WEIGHT
import numpy as np

np.random.seed(42)
# random seeds of interest
# 17: casual
# 42: photon exiting top direction

def calcCritAngles(layer_list):
    for l, layer in enumerate(layer_list[1:-2]):
        n1 = layer_list[l].n # this layer
        n2 = layer_list[l-1].n # previous upwards layer
        if n1>n2:
            layer.cos_crit0 = np.sqrt(1.0 - n2*n2/(n1*n1)) # crit0 upwards
        else:
            layer.cos_crit0 = 0

        n2 = layer_list[l+1].n # next layer downwards
        if n1>n2:
            layer.cos_crit1 = np.sqrt(1.0 - n2 * n2 / (n1 * n1))  # crit1 downwards
        else:
            layer.cos_crit1 = 0


if __name__ == '__main__':

    # define IOfiles
    OUTPATH = 'out'
    FILENAME = 'test2.csv'

    # define params
    photons = list()
    for p in range(0, 100):
        photons.append(PhotonPack(stepSize=0.01, w=1))

    #photon2 = PhotonPack(stepSize=0.01, w=1)

    layer1 = Tissue(z0=0, z1=0.2, n=1, mua=1, mus=100, g=0.9)
    layer2 = Tissue(z0=0.2, z1=0.5, n=1.37, mua=1, mus=100, g=0.9)
    layer3 = Tissue(z0=0.5, z1=4, n=1.37, mua=1, mus=100, g=0.9)


    #
    layers = [layer1, layer2, layer3]
    #photons = [photon1, photon2]

    # create output
    if not os.path.exists(os.path.join(OUTPATH)):
        os.makedirs(os.path.join(OUTPATH))
    outfile = open(os.path.join(OUTPATH, FILENAME), 'w', newline='')
    writer = csv.writer(outfile, delimiter=';')
    writer.writerow(['x', 'y', 'z', 'ux', 'uy', 'uz', 'layer', 'weight', 'dead'])

    # start sim
    #print(p.__repr__()) # TODO: check repr

    # calculate critical angles one time for given layers
    calcCritAngles(layers)

    for p in photons:
        #print(layers[p._layer].hitBoundry(p)) #
        while not layers[p._layer].hitBoundry(p) and p.alive() == 1:
            layers[p._layer].hop(p)
            layers[p._layer].absorption(p)
            layers[p._layer].scatter(p)
            writer.writerow(p.__repr__())
            if p._w < WEIGHT and p.alive() == 1:
                p.roulette()
            if layers[p._layer].hitBoundry(p) and p.alive() == 1: # and hitBoundry(p)==1

                layers[p._layer].hop(p) # swapped hop and cross or not, smart!!! es muss erst noch der restliche weg im alten layer zurück gelegt werden (bis zur grenze des layers) und dann kann der layer erhöht werden
                layers[p._layer].crossOrNot(p, layers)
                writer.writerow(p.__repr__())
                #writer.writerow(50*'-') #  TODO: sinnvoller print mit layer nr?

    # for i in range(0, 100):
    #     layer1.hop(photon1)
    #     layer1.absorption(photon1)
    #     layer1.scatter(photon1)
    #     writer.writerow(photon1.__repr__())
    #     #print(photon1)

    outfile.close()
