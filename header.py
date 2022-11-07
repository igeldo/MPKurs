import os
import numpy as np

class PhotonPack:
    def __init__(self, x , y, z, layer=1, stepSize=0, stepSizeL=0,
                 ux=0, uy=0, uz=1, w=1, dead=0):
        self.x, self.y, self.z = x, y, z  # coordinates [mm]
        self.ux, self.uy, self.uz = ux, uy, uz  # directional cosines of photonpack
        self.w = w  # "weight"
        self.dead = dead  # 1 if photon is "terminated"(absorpted or reflected)
        self.layer = layer  # layer in with the PhotonPack currently is
        self.stepSize = stepSize  # current step size [mm]
        self.stepSizeL = stepSizeL  # step size left, dimensionless (why?)

class Layer:
    def __init__(self, z0, z1, mua, mus, g, n=1):
        self.z0, self.z1 = z0, z1  # z coordinates of the upper (z0) and lower (z1) boundary of the respective layer [mm]
        self.n = n  # refractive index (Brechungsindex) of the respective layer
        self.mua, self.mus = mua, mus  # absorption and scattering coefficient [1/mm]
        self.g = g  # anisotropy of the layer material

        self. cos_crit0, self.cos_crit1  # critical angles under which total reflection occurs(?) so there is nothing to compute in this layer





