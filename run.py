class Material:
    def __init__(self):

    def __hop(self, photonPack):
        photonPack.__pos += photonPack.__dvec * photonPack.__stepSize
        #self.__y += self.stepSize * self.__uy
        #self.__z += self.stepSize * self.__uz


class Glas(Material):
    def __init__(self):
        super.__init__()

    def hop(self):
    ''''
    def inGlass(self, photonPack):
        if (photonPack.__dvec(3) == 0):  # 3rd dimension is uz
            photonPack.__dead = 1
        else:
            StepSize.inGlass()
            self.hop(photonPack)
    '''

    def stepSize(self, photonPack, layer):
        if(photonPack.__dvec(3) > 0.0):
            stepsToBoundry = (layer.z1)


class Tissue(Material):
    def __init__(self):
        super.__init__()

    def stepSize(self):
