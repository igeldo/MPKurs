import os
import numpy as np
from vector import Vec3d


class PhotonPack(Vec3d):
    """
    Basic class to simulate photon packages.

    ...

    Attributes
    ----------
        __x,__y,__z :
            coordinates in [mm]
        __ux,__uy,__uz :
            directional cosines of the PhotonPack
        w :
            "weight", more like energy(?)
        __dead :
            1 if the photon is terminated (absorbed or reflected)
        __layer :
            current layer where the PhotonPack resides
        stepSize :
            current step size in [mm]
        stepSizeL :
            step size left, dimensionless, because it's relative to layer material

    Methods
    -------
        get_pos() :
            Returns the x,y,z coordinates of the PhotonPackage in its current layer.
    """

    def __init__(self, pos=Vec3d(0,0,0), layer=1, stepSize=0, stepSizeL=0,
                 dvec=Vec3d(0,0,1), w=1, dead=0):
        self.__pos = pos  # coordinates [mm]
        self.__dvec = dvec  # directional cosines of photonpack
        self.__w = w  # "weight", more like energy?
        self.__dead = dead  # 1 if photon is "terminated"(absorpted or reflected)
        self.__layer = layer  # layer in with the PhotonPack currently is
        self.__stepSize = stepSize  # current step size [mm]
        self.__stepSizeL = stepSizeL  # step size left, dimensionless, because it's relative to layer material stepSizeL = ()

    def __repr__(self):
        """
        Returns the x,y,z coordinates of the PhotonPackage in its current layer.

        Parameters
        ----------
            None

        Returns
        -------
            Tuple(x,y,z) :
                Coordinates of the PhotonPack in the layer it resides in [mm]
            layer :
                Index of the layer where the PhotonPack resides
        """
        return "{}, {}, {}, {}, {}".format(
                self.__pos, self.__dvec, self.__layer, self.__w, self.__dead)


class Layer:
    """
    Basic class to simulate a layer.
    
    ...
    
    Attributes
    ----------
    z0,z1 :
        z-coordinates of the upper (z0) and lower (z1) boundary of the layer in [mm]
    n : 
        refractive index of the layer
    mua, mus : 
        absorption and scattering coefficient in [1/mm]
    g : 
        anisotropy of the material
    cos_crit0, cos_crit1 : 
        critical angles under which the total reflection occurs

    Methods
    -------
    """

    def __init__(self, z0, z1, mua, mus, g, n=1):
        self.z0, self.z1 = z0, z1  # z coordinates of the upper (z0) and lower (z1) boundary of the respective layer [mm]
        self.n = n  # refractive index (Brechungsindex) of the respective layer
        self.mua, self.mus = mua, mus  # absorption and scattering coefficient [1/mm]
        self.g = g  # anisotropy of the layer material
        self.cos_crit0, self.cos_crit1  # critical angles under which total reflection occurs(?) so there is nothing to compute in this layer

class Medium:
    def __init__(self, layer1, layer2, layer3): # zukünftig mit 'args?
        # for l in len(args):
        #   layer_l = args(l)
        self.layer1 = layer1
        self.layer2 = layer2
        self.layer3 = layer3

        # fehlt hier noch eigentschaften gedönns? z.B. dz,dr,da
        # und ist grid üeberhaupt nötig? -> mit vincent mal besprechen
