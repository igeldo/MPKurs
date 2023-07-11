import math


class Vec3d:
    def __init__(self, x=0, y=0, z=0):
        self._x = x
        self._y = y
        self._z = z

    def __add__(self, other):
        if isinstance(other, Vec3d):
            return Vec3d(self._x + other._x, self._y + other._y, self._z + other._z)

    def __sub__(self, other):
        if isinstance(other, Vec3d):
            return Vec3d(self._x - other._x, self._y - other._y, self._z - other._z)

    def __mul__(self, other):
        if isinstance(other, Vec3d):
            return self._x * other._x + self._y * other._y + self._z * other._z
        elif isinstance(other, (float, int)):
            return Vec3d(self._x * other, self._y * other, self._z * other)
    def __abs__(self):
        return math.sqrt(self._x ** 2 + self._y ** 2 + self._z ** 2)

    def __repr__(self):
        return "({},{},{})".format(self._x, self._y, self._z)

    def x(self):
        return self._x

    def y(self):
        return self._y

    def z(self):
        return self._z
