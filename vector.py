import math


class Vec3d:
    def __init__(self, x=0, y=0, z=0):
        self.__x = x
        self.__y = y
        self.__z = z

    def __add__(self, other):
        if isinstance(other, Vec3d):
            return Vec3d(self.__x + other.__x, self.__y + other.__y, self.__z + other.__z)

    def __sub__(self, other):
        if isinstance(other, Vec3d):
            return Vec3d(self.__x - other.__x, self.__y - other.__y, self.__z - other.__z)

    def __mul__(self, other):
        if isinstance(other, Vec3d):
            return Vec3d(self.__x * other.__x + self.__y * other.__y + self.__z * other.__z)
        elif isinstance(other, (float, int)):
            return Vec3d(self.__x * other, self.__y * other, self.__z * other)
    def __abs__(self):
        return math.sqrt(self.__x**2+self.__y**2+self.__z**2)

    def __repr__(self):
        return "({},{},{})".format(self.__x, self.__y, self.__z)

    def x(self):
        return self.__x

    def y(self):
        return self.__y

    def z(self):
        return self.__z
