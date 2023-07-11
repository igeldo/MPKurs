import numpy as np
import numpy.random

from vector import Vec3d

COSZERO = 1 - 1E-12
COS90D = 1E-6
CHANCE = 0.1  # Chance of surviving the roulette
WEIGHT = 1E-4  # Critical weight for roulette

class PhotonPack:
    """
    Basic class to simulate a multitude of photons.

    Attributes
    ----------
        _pos : Vec3d
            coordinates in mm
        _dvec : Vec3d
            directional cosines of the PhotonPack
        weight : float
            "weight", more like energy
        _dead : int
            1 if the photon is terminated (absorbed or reflected)
        _exits : int
            1 if the photon leaves the model
        layer : int
            current layer where the PhotonPack resides
        _stepSize : float
            current step size in mm
        _stepSizeL : float
            step size left to current layer boundary in mm

    Methods
    -------
        get_pos() :
            Returns the x,y,z coordinates of the PhotonPackage in its current layer.
    """

    def __init__(self, pos=Vec3d(0,0,0), layer=0, stepSize=0, stepSizeL=0,
                 dvec=Vec3d(0,0,1), weight=1, dead=0, exits=0):
        self._pos = pos  # coordinates [mm]
        self._dvec = dvec  # directional cosines of photonpack
        self.weight = weight  # "weight", more like energy?
        self._dead = dead  # 1 if photon is "terminated"(absorpted or reflected)
        self._exits = exits  # 1 if the photon exits 1st layer in the top direction
        self.layer = layer  # layer in with the PhotonPack currently is
        # stepSize is handled and calculated in each layer based on its properties and the photon energy/weight
        self._stepSize = stepSize  # current step size [mm]
        self._stepSizeL = stepSizeL  # step size left, dimensionless, because it's relative to layer material stepSizeL = ()

    def __repr__(self) -> list:
        """
        Returns list of strings of attributes

        Returns
        -------
            List of strings of attributes
        """

        return [
            str(self._pos.x()),
            str(self._pos.y()),
            str(self._pos.z()),
            str(self._dvec.x()),
            str(self._dvec.y()),
            str(self._dvec.z()),
            str(self.layer),
            str(self.weight),
            str(self._dead),
            str(self._exits)
        ]

    def __str__(self) -> str:
        """
        Returns strings of attributes

        Returns
        -------
            Returns strings of attributes
        """

        return ' '.join([
            str(self._pos.x()),
            str(self._pos.y()),
            str(self._pos.z()),
            str(self._dvec.x()),
            str(self._dvec.y()),
            str(self._dvec.z()),
            str(self.layer),
            str(self.weight),
            str(self._dead),
            str(self._exits)
        ])

    def alive(self):
        """
        Returns True if the photon is alive, 0 if dead

        Returns
        -------
            Returns True if the photon is alive, 0 if dead
        """
        return not self._dead

    def roulette(self):
        """
        Draws a random number between 0 and 1 and derives a chance by which the photon can survive.
        """
        rnd = np.random.uniform()
        if self.weight == 0:
            self._dead = 1
        elif rnd < CHANCE:
            self.weight /= CHANCE
        else:
            self._dead = 1

class Medium:
    """
    Basic class to simulate a layer.

    Attributes
    ----------
    z0,z1 :
        z-coordinates of the upper (z0) and lower (z1) boundary of the layer in mm
    n :
        Refractive index of the layer
    mua, mus :
        Absorption and scattering coefficient in 1/mm. Typically these are given in 1/cm.
    anisotropy :
        Anisotropy of the material
    cos_crit0, cos_crit1 :
        Critical angles under which the total reflection occurs
    """

    def __init__(self, z0, z1, mua, mus, anisotropy, n=1):
        self.z0, self.z1 = z0, z1  # z coordinates of the upper (z0) and lower (z1) boundary of the respective layer [mm]
        self.n = n  # refractive index (Brechungsindex) of the respective layer
        self.mua, self.mus = mua, mus  # absorption and scattering coefficient [1/mm]
        self.anisotropy = anisotropy  # anisotropy of the layer material
        self.cos_crit0, self.cos_crit1 = 0, 0  # critical angles under which total reflection occurs(?) so there is nothing to compute in this layer

    def hop(self, photonPack):
        """
        Calculates new photon position by multiplying the directional vector and the step size.

        Parameters
        ----------
        photonPack

        """

        photonPack._pos += photonPack._dvec * photonPack._stepSize

    def calcStepSize(self, photonPack):
        """
        Calculate the step size by dividing a random number between 0 and 1 by the sum of the absorption and scattering coefficient.

        Parameters
        ----------
        photonPack

        """
        photonPack._stepSize = -np.log(np.random.uniform()) / (self.mua + self.mus)

    def hitBoundary(self, photonPack):
        """
        Checks if the photon is able to hit the current layer boundaries (upper and lower) with the current direction and step size.
        Also calculates the remaining step size to the boundary if the photon hits the boundary and overrides the current with the remaining step size.

        Parameters
        ----------
        photonPack

        Returns
        -------
        hit : int
        """
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
        """
        Differentiates between upper and lower boundary crossing.

        Parameters
        ----------
        photonPack
        layers
        """
        if photonPack._dvec.z() < 0.0:
            self._crossUp(photonPack, layers)
        else:
            self._crossDown(photonPack, layers)

    def _crossDown(self, photonPack, layers):
        """
        Checks if the incoming angle of the photon is below the critical angle value. If so total reflection occurs.
        If no total reflection is happening the photons layer is set to the next downward one.

        Parameters
        ----------
        photonPack
        layers
        """
        out_uz = 0

        if photonPack._dvec.z() <= self.cos_crit1:
            r = 1  # total reflection!

        elif photonPack.layer == len(layers)-1:
            photonPack._dead = 1
            r = 0
            out_uz = photonPack._dvec.z()  # Pfeil in richtige "exit"-Richtung

        else:
            n1 = self.n  # this layer
            n2 = layers[photonPack.layer + 1].n  # next layer
            r, out_uz = self._RFresnel(n1, n2, photonPack._dvec.z())
        # NO PARTIAL REFLECTION IMPLEMENTED RIGHT NOW

        if np.random.uniform() > r:
            if photonPack.layer == len(layers)-1:  # letzter Layer
                photonPack._dvec._z = out_uz
                photonPack._dead = 1  # RIP
                photonPack._exits = 1

            else:
                photonPack._dvec = Vec3d(
                    photonPack._dvec._x * (n1 / n2),
                    photonPack._dvec._y * (n1 / n2),
                    out_uz
                )  # NICHT Skalarprodukt, deswegen Komponenten einzeln berechnet
                photonPack.layer += 1

        else:
            photonPack._dvec._z = -photonPack._dvec._z


    def _crossUp(self, photonPack, layers):
        """
        Checks if the incoming angle of the photon is below the critical angle value. If so total reflection occurs.
        If no total reflection is happening the photons layer is set to the next upward one.

        Parameters
        ----------
        photonPack
        layers
        """
        out_uz = 0

        if -photonPack._dvec.z() <= self.cos_crit0:
            r = 1
        elif photonPack.layer == 0:
            photonPack._dead = 1
            r = 0
            out_uz = -photonPack._dvec.z()  # Pfeil in richtiger "exit"-Richtung

        else:
            n1 = self.n  # this layer
            n2 = layers[photonPack.layer - 1].n  # next layer
            r, out_uz = self._RFresnel(n1, n2, -photonPack._dvec.z())
        # NO PARTIAL REFLECTION IMPLEMENTED RIGHT NOW

        if np.random.uniform() > r:  # chance for photon to be reflected
            if photonPack.layer == 0:  # erster Layer # REMINDER: in MCML steht hier eine 1, also nicht "erster" layer?
                photonPack._dvec._z = -out_uz
                photonPack._dead = 1  # RIP
                photonPack._exits = 1
            else:
                photonPack._dvec = Vec3d(
                    photonPack._dvec._x * (n1 / n2),
                    photonPack._dvec._y * (n1 / n2),
                    -out_uz
                )
                photonPack.layer -= 1

        else:
            photonPack._dvec._z = -photonPack._dvec._z

    def _RFresnel(self, ni, nt, cosi):
        """
        Compute the Fresnel reflectance.

        Parameters
        ----------
        ni : current layers refractive index
        nt : next layers refractive index
        cosi : cosine of incoming angle

        Returns
        -------
        r : reflectance
        cost : cosine of incoming angle
        """

        r = 0  # reflectance
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
            if (sint >= 1.0):
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

class Tissue(Medium):
    """
    Basic class to simulate a layer.

    Attributes
    ----------
    z0,z1 :
        z-coordinates of the upper (z0) and lower (z1) boundary of the layer in mm
    n :
        Refractive index of the layer
    mua, mus :
        Absorption and scattering coefficient in 1/mm. Typically these are given in 1/cm.
    anisotropy :
        Anisotropy of the material
    cos_crit0, cos_crit1 :
        Critical angles under which the total reflection occurs
    """

    def __int__(self, z0, z1, mua, mus, anisotropy, cos_crit0, cos_crit1, n=1):
        super().__init__(z0, z1, mua, mus, anisotropy, cos_crit0, cos_crit1, n=1)

    def absorption(self, photonPack):
        """
        Reduce photon weight based on absorption and scattering coefficient.

        Parameters
        ----------
        photonPack
        """
        dw = photonPack.weight * self.mua / (self.mua + self.mus)
        photonPack.weight -= dw

    def scatter(self, photonPack):
        """
        Calculate new directional vector and scattering angle.

        Parameters
        ----------
        photonPack
        """
        # calculate random direction for polar angle theta
        if (self.anisotropy==0):
            cos_t = 2*np.random.uniform() - 1
            # 2*rand-1 because value should be between [-1,1]
        else:
            temp = (1-self.anisotropy*self.anisotropy) / (1-self.anisotropy+2*np.random.uniform())
            cos_t = (1+self.anisotropy*self.anisotropy - temp*temp) / (2*self.anisotropy)
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
        else:
            temp = np.sqrt(1 - uz*uz)
            photonPack._dvec = Vec3d(
                (sin_t * (ux * uz * cos_p - uy * sin_p) / temp) + ux * cos_t,
                (sin_t * (uy * uz * cos_p + ux * sin_p) / temp) + uy * cos_t,
                -sin_t * cos_p * temp + uz * cos_t
            )
