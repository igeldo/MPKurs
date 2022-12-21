from model import Layer, PhotonPack
from run import Hop
if __name__ == '__main__':

    photon1 = PhotonPack(stepSize=1)
    hop = Hop

    print(photon1)
    for i in range(0,10):
        hop.hop(photon1)
        print(photon1)

