import os
import csv
from model import Tissue, PhotonPack

if __name__ == '__main__':

    # define iofiles
    OUTPATH = 'out'
    FILENAME = 'test.csv'

    # define params
    photon1 = PhotonPack(stepSize=1, w=100)
    layer1 = Tissue(z0=0, z1=1000, mua=1, mus=1, g=0, cos_crit0=0,cos_crit1=0)

    # create output
    if not os.path.exists(os.path.join(OUTPATH)):
        os.makedirs(os.path.join(OUTPATH))
    outfile = open(os.path.join(OUTPATH, FILENAME), 'w', newline='')
    writer = csv.writer(outfile, delimiter=';')
    writer.writerow(['x', 'y', 'z', 'ux', 'uy', 'uz', 'layer', 'weight', 'dead'])

    # start sim
    print(photon1.__repr__()) # TODO: check repr
    for i in range(0, 100):
        layer1._hop(photon1)
        layer1._absorption(photon1)
        writer.writerow(photon1.__repr__())
        #print(photon1)

    outfile.close()
