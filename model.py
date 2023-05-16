import numpy as np
import numpy.random

from vector import Vec3d

COSZERO = 1-1E-12
COS90D = 1E-6
CHANCE = 0.1 # Chance of surviving the roulette
WEIGHT = 1E-4 # Critical weight for roulette

# TODO: for testing -> set random seed for uniform variable, calculate the algorithm "by hand" for that variable, then test for algorithm

class PhotonPack:
    """
    Basic class to simulate photon packages.

    ...

    Attributes
    ----------
        _x,_y,_z :
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

    def __init__(self, pos=Vec3d(0,0,0), layer=0, stepSize=0, stepSizeL=0,
                 dvec=Vec3d(0,0,1), w=1, dead=0, exits=0):
        self._pos = pos  # coordinates [mm]
        self._dvec = dvec  # directional cosines of photonpack
        self._w = w  # "weight", more like energy?
        self._dead = dead  # 1 if photon is "terminated"(absorpted or reflected)
        self._layer = layer  # layer in with the PhotonPack currently is
        # stepSize is handled and calculated in each layer based on its properties and the photon energy/weight
        self._stepSize = stepSize  # current step size [mm]
        self._stepSizeL = stepSizeL  # step size left, dimensionless, because it's relative to layer material stepSizeL = ()
        self._exits = exits  # 1 if the photon exits 1st layer in the top direction

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
            str(self._dead),
            str(self._exits)
        ]

    def alive(self):
        return not self._dead

    def roulette(self):
        rnd = np.random.uniform()
        if self._w == 0:
            self._dead = 1
        elif rnd < CHANCE:
            self._w /= CHANCE
        else:
            self._dead = 1

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

    def __init__(self, z0, z1, mua, mus, g, n=1):
        self.z0, self.z1 = z0, z1  # z coordinates of the upper (z0) and lower (z1) boundary of the respective layer [mm]
        self.n = n  # refractive index (Brechungsindex) of the respective layer
        self.mua, self.mus = mua, mus  # absorption and scattering coefficient [1/mm]
        self.g = g  # anisotropy of the layer material
        self.cos_crit0, self.cos_crit1 = 0, 0  # critical angles under which total reflection occurs(?) so there is nothing to compute in this layer

    def hop(self, photonPack):
        photonPack._pos += photonPack._dvec * photonPack._stepSize

    def calcStepSize(self, photonPack):
        photonPack._stepSize = -np.log(np.random.uniform()) / (self.mua + self.mus)

    def hitBoundry(self, photonPack):
        dl_b = 0
        hit = 0
        if photonPack._dvec.z() > 0.0:
            dl_b = (self.z1 - photonPack._pos.z()) / photonPack._dvec.z()
        elif photonPack._dvec.z() < 0.0:
            dl_b = (self.z0 - photonPack._pos.z()) / photonPack._dvec.z()

        if photonPack._dvec.z() != 0.0 and photonPack._stepSize > dl_b:
            mut = self.mua + self.mus

            photonPack._stepSizeL = (photonPack._stepSize - dl_b) * mut
            photonPack._stepSize = dl_b
            hit = 1
        else:
            hit = 0

        return hit

    def crossOrNot(self, photonPack, layers):
        if photonPack._dvec.z() < 0.0:
            self._crossUp(photonPack, layers)
        else:
            self._crossDown(photonPack, layers)

    def _crossDown(self, photonPack, layers):
        n1 = self.n  # this layer
        n2 = layers[photonPack._layer+1].n  # next layer


        if photonPack._dvec.z() <= self.cos_crit1:
            r = 1 # total reflection!
            out_uz = 0
        elif photonPack._layer == len(layers)-1:
            photonPack._dead = 1
            r = 0
            out_uz = 0
        else:
            r, out_uz = self._RFresnel(n1, n2, photonPack._dvec.z())
        # NO PARTIAL REFLECTION IMPLEMENTED RIGHT NOW

        if np.random.uniform() > r:
            if photonPack._layer == len(layers)-1:  # letzter Layer
                photonPack._dvec._z = out_uz
                photonPack._dead = 1  # RIP
            else:
                photonPack._dvec = Vec3d(
                    photonPack._dvec._x * (n1 / n2),
                    photonPack._dvec._y * (n1 / n2),
                    out_uz
                )  # NICHT Skalarprodukt, deswegen Komponenten einzeln berechnet
                photonPack._layer += 1
        else:
            photonPack._dvec._z = -photonPack._dvec._z


    def _crossUp(self, photonPack, layers):
        n1 = self.n  # this layer
        n2 = layers[photonPack._layer - 1].n  # next layer

        if -photonPack._dvec.z() <= self.cos_crit0:
            r = 1
            out_uz = 0
        elif photonPack._layer == 0:
            photonPack._dead = 1
            r = 0
            out_uz = 0
        else:
            r, out_uz = self._RFresnel(n1, n2, -photonPack._dvec.z())
        # NO PARTIAL REFLECTION IMPLEMENTED RIGHT NOW

        if np.random.uniform() > r:  # chance for photon to be reflected
            if photonPack._layer == 0:  # erster Layer # REMINDER: in MCML steht hier eine 1, also nicht "erster" layer?
                photonPack._dvec._z = -out_uz
                photonPack._dead = 1  # RIP
                photonPack._exits = 1
            else:
                photonPack._dvec = Vec3d(
                    photonPack._dvec._x * (n1 / n2),
                    photonPack._dvec._y * (n1 / n2),
                    -out_uz
                )
                photonPack._layer -= 1
        else:
            photonPack._dvec._z = -photonPack._dvec._z

    def _RFresnel(self, ni, nt, cosi):
        r = 0  # reflectance

        # ....
        if (ni == nt):  # matched boundary case
            cost = cosi
            r = 0
        elif (cosi > COSZERO):  # normal incident, "nearly" orthogonal angle to boundary border
            cost = cosi
            r = (nt - ni) / (nt + ni)  # MCman p.18, eq. 3.25
            r *= r
        elif (cosi < COS90D): # very slant, "nearly" horizontal to boundary border
            cost = 0
            r = 1
        else:
            sini = np.sqrt(1 - cosi*cosi) # sqrt instead of sine cuz it is faster
            sint = ni * sini / nt
            if (sint >= 1.0):  # TODO: why double check? rundungsfehler?
                cost = 0
                r = 1
            else:
                cost = np.sqrt(1 - sint*sint)

                cosp = cosi*cost - sini*sint
                cosm = cosi*cost + sini*sint
                sinp = sini*cost + cosi*sint
                sinm = sini*cost - cosi*sint

                r = 0.5 * sinm**2 * (cosm**2 + cosp**2)/(sinp**2 * cosm**2)

        return r, cost

class Glas(Medium):

    #def hop(self, photonPack):
        # """
    #     if (photonPack.__dvec.z == 0):  # 3rd dimension is uz
    #         photonPack.__dead = 1
    #     else:
    #         StepSize.inGlass()
    #         self.hop(photonPack)
        # """

    def stepSize(self, photonPack, layer):
        if(photonPack._dvec.z() > 0.0): # TODO z falsch?
            stepsToBoundry = (layer.z1)


class Tissue(Medium):

    def __int__(self, z0, z1, mua, mus, g, cos_crit0, cos_crit1, n=1):
        super().__init__(z0, z1, mua, mus, g, cos_crit0, cos_crit1, n=1) #TODO: siehe TODO hop

    # def hop(self, photonPack):
    #     super().hop(photonPack)  # TODO: Warum hier mit Argument, aber nicht bei __init()__? @vincent @alex
    #
    # def hitBoundry(self, photonPack):
    #     super().hitBoundry(photonPack)

    def absorption(self, photonPack):
        dw = photonPack._w * self.mua / (self.mua + self.mus)
        photonPack._w -= dw

    def scatter(self, photonPack):
        # calculate random direction for polar angle theta
        if (self.g==0):
            cos_t = 2*np.random.uniform() - 1
            # 2*rand-1 because value should be between [-1,1]
        else:
            temp = (1-self.g*self.g) / (1-self.g+2*np.random.uniform())
            cos_t = (1+self.g*self.g - temp*temp) / (2*self.g)
            if (cos_t < -1):
                cos_t = -1
            elif (cos_t > 1):
                cos_t = 1
        sin_t = np.sqrt(1 - cos_t*cos_t)

        # calculate random direction of azimuthal angle phi
        phi = 2*np.pi*np.random.uniform()
        cos_p = np.cos(phi)
        sin_p = np.sin(phi)

        # calculate new direction vector
        ux = photonPack._dvec.x()
        uy = photonPack._dvec.y()
        uz = photonPack._dvec.z()

        if (np.abs(uz) > COSZERO):
            photonPack._dvec = Vec3d(
                sin_t * cos_p,
                sin_t * sin_p,
                cos_t * np.sign(uz)
            )
            # photonPack._dvec._x = sin_t * cos_p
            # photonPack._dvec._y = sin_t * sin_p
            # photonPack._dvec._z = cos_t * np.sign(uz)
        else:
            temp = np.sqrt(1 - uz*uz)
            photonPack._dvec = Vec3d(
                (sin_t * (ux * uz * cos_p - uy * sin_p) / temp) + ux * cos_t,
                (sin_t * (uy * uz * cos_p + ux * sin_p) / temp) + uy * cos_t,
                -sin_t * cos_p * temp + uz * cos_t
            )
            # photonPack._dvec._x = (sin_t * (ux * uz * cos_p - uy * sin_p) / temp) + ux * cos_t
            # photonPack._dvec._y = (sin_t * (uy * uz * cos_p + ux * sin_p) / temp) + uy * cos_t
            # photonPack._dvec._z = -sin_t * cos_p * temp + uz * cos_t


# class Luft(Medium):
#     def __int__(self):
#         super.__init__()
#
#     def stepSize(self):

# TODO: - siehe plot
#       - remove starting point of layer, when enough time
