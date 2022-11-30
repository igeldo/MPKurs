from header import Layer, PhotonPack

if __name__ == '__main__':
    photon1 = PhotonPack(stepSize=1)

    print(photon1.x, photon1.y, photon1.z)
    for i in range(0,10):
        photon1.hop()
    print(photon1.x, photon1.y, photon1.z)
