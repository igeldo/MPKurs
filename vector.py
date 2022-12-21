import math


class Vec3d:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        if isinstance(other, Vec3d):
            return Vec3d(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        if isinstance(other, Vec3d):
            return Vec3d(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, Vec3d):
            return Vec3d(self.x * other.x + self.y * other.y + self.z * other.z)
        elif isinstance(other, (float, int)):
            return Vec3d(self.x * other, self.y * other, self.z * other)
    def __abs__(self):
        return math.sqrt(self.x**2+self.y**2+self.z**2)

    def __repr__(self):
        return "({},{},{})".format(self.x, self.y, self.z)

