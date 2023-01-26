import os
import csv
from model import Tissue, PhotonPack

if __name__ == '__main__':

    # define iofiles
    OUTPATH = 'out'
    FILENAME = 'test.csv'

    # define params
    photon1 = PhotonPack(stepSize=1, w=100)
    layer1 = Tissue(z0=0, z1=1000, mua=1, mus=100, g=0.9, cos_crit0=0,cos_crit1=0)

    layers = list(layer1)
    photons = list(photon1)

    # create output
    if not os.path.exists(os.path.join(OUTPATH)):
        os.makedirs(os.path.join(OUTPATH))
    outfile = open(os.path.join(OUTPATH, FILENAME), 'w', newline='')
    writer = csv.writer(outfile, delimiter=';')
    writer.writerow(['x', 'y', 'z', 'ux', 'uy', 'uz', 'layer', 'weight', 'dead'])

    # start sim
    print(photon1.__repr__()) # TODO: check repr

    for p in photons:
        if p.alive == 0:
            while(not layers[p._layer].hitBoundry):
                        layers[p._layer].hop(p)
                        layers[p._layer].absorption(p)
                        layers[p._layer].scatter(p)
                        writer.writerow(p.__rep)
            layers[p._layer].hop(p)
            layers[p._layer].crossOrNot(p, layers)


    # for i in range(0, 100):
    #     layer1.hop(photon1)
    #     layer1.absorption(photon1)
    #     layer1.scatter(photon1)
    #     writer.writerow(photon1.__repr__())
    #     #print(photon1)

    outfile.close()
