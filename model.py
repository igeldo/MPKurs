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
        self._pos = pos  # coordinates [mm]
        self._dvec = dvec  # directional cosines of photonpack
        self._w = w  # "weight", more like energy?
        self._dead = dead  # 1 if photon is "terminated"(absorpted or reflected)
        self._layer = layer  # layer in with the PhotonPack currently is
        # stepSize is handled and calculated in each layer based on its properties and the photon energy/weight
        self._stepSize = stepSize  # current step size [mm]
        #self.__stepSizeL = stepSizeL  # step size left, dimensionless, because it's relative to layer material stepSizeL = ()

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
        #return "{}, {}, {}, {}, {}".format(
         #       self._pos, self._dvec, self._layer, self._w, self._dead)
        return [
            str(self._pos.x()),
            str(self._pos.y()),
            str(self._pos.z()),
            str(self._dvec.x()),
            str(self._dvec.y()),
            str(self._dvec.z()),
            str(self._layer),
            str(self._w),
            str(self._dead)
        ]

class Medium:
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
        absorption and scattering coefficient in [1/mm] TODO: typischerweise in cm -> umrechnen *1/10
    g : 
        anisotropy of the material
    cos_crit0, cos_crit1 : 
        critical angles under which the total reflection occurs

    Methods
    -------
    """

    def __init__(self, z0, z1, mua, mus, g, cos_crit0, cos_crit1, n=1):
        self.z0, self.z1 = z0, z1  # z coordinates of the upper (z0) and lower (z1) boundary of the respective layer [mm]
        self.n = n  # refractive index (Brechungsindex) of the respective layer
        self.mua, self.mus = mua, mus  # absorption and scattering coefficient [1/mm]
        self.g = g  # anisotropy of the layer material
        self.cos_crit0, self.cos_crit1 = cos_crit0, cos_crit1  # critical angles under which total reflection occurs(?) so there is nothing to compute in this layer

    def _hop(self, photonPack):
        s = -np.log(np.random.uniform())/(self.mua+self.mus)
        #print(s)
        photonPack._pos += photonPack._dvec * s

class Glas(Medium):


    #def hop(self):
        # """
        # def inGlass(self, photonPack):
        #     if (photonPack.__dvec.z == 0):  # 3rd dimension is uz
        #         photonPack.__dead = 1
        #     else:
        #         StepSize.inGlass()
        #         self.hop(photonPack)
        # """

    def stepSize(self, photonPack, layer):
        if(photonPack._dvec.z > 0.0): # TODO z falsch?
            stepsToBoundry = (layer.z1)


class Tissue(Medium):

    def __int__(self):
        super().__init__() #TODO: siehe TODO hop

    def _hop(self, photonPack):
        super()._hop(photonPack) # TODO: Warum hier mit Argument, aber nicht bei __init()__? @vincent @alex

    #def stepSize(self):
        """
        p.14 & p.19 eq. 2.7 "total interaction coefficient µt, which is the sum of the
absorption coefficient µa and the scattering coefficient µs"
        Returns
        -------

        """

    def _absorption(self, photonPack):
        dw = photonPack._w * self.mua / (self.mua + self.mus)
        photonPack._w = dw


# class Luft(Medium):
#     def __int__(self):
#         super.__init__()
#
#     def stepSize(self):
