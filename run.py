class StepSize:
    def __init__(self):
        self.inGlass()
        self.inTissue()

    def inGlass(self, photonPack, layer):
        if(photonPack.__dvec(3) > 0.0):
            stepsToBoundry = (layer.z1)

class Hop:
    def __init__(self):
        self.__hop()
        self.inGlass()
        self.inTissue()

    def __hop(self, photonPack):
        photonPack.__pos += photonPack.__dvec * photonPack.__stepSize
        #self.__y += self.stepSize * self.__uy
        #self.__z += self.stepSize * self.__uz

    def inGlass(self, photonPack):
        if(photonPack.__dvec(3) == 0): # 3rd dimension is uz
            photonPack.__dead = 1
        else:
            StepSize.inGlass()
            self.hop(photonPack)

