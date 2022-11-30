import os
import numpy as np

class PhotonPack:
    """
    Basic class to simulate photon packages.

    ...

    Attributes
    ----------
        x,y,z :
            coordinates in [mm]
        ux,uy.uz :
            directional cosines of the PhotonPack
        w :
            "weight", more like energy(?)
        dead :
            1 if the photon is terminated (absorbed or reflected)
        layer :
            current layer where the PhotonPack resides
        stepSize :
            current step size in [mm]
        stepSizeL :
            step size left, dimensionless, because it's relative to layer material

    Methods
    -------
        get_coords() :
            Returns the x,y,z coordinates of the PhotonPackage in its current layer.
    """
    def __init__(self, x=0, y=0, z=0, layer=1, stepSize=0, stepSizeL=0,
                 ux=0, uy=0, uz=1, w=1, dead=0):
        self.x, self.y, self.z = x, y, z  # coordinates [mm]
        self.ux, self.uy, self.uz = ux, uy, uz  # directional cosines of photonpack
        self.w = w  # "weight", more like energy?
        self.dead = dead  # 1 if photon is "terminated"(absorpted or reflected)
        self.layer = layer  # layer in with the PhotonPack currently is
        self.stepSize = stepSize  # current step size [mm]
        self.stepSizeL = stepSizeL  # step size left, dimensionless, because it's relative to layer material stepSizeL = ()

    def get_coords(self):
        '''
        Returns the x,y,z coordinates of the PhotonPackage in its current layer.

        Parameters
        ----------
            none
        
        Returns
        -------
            Tuple(x,y,z) :
                Coordinates of the PhotonPack in the layer it resides in [mm]
            layer :
                Index of the layer where the PhotonPack resides
        '''
        return (self.x, self.y, self.z), self.layer

    def hop(self):
        self.x += self.stepSize*self.ux
        self.y += self.stepSize*self.uy
        self.z += self.stepSize*self.uz

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

        self. cos_crit0, self.cos_crit1  # critical angles under which total reflection occurs(?) so there is nothing to compute in this layer





