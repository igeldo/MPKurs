from daten import Daten
import operatoren as op

def const(value):
    return op.Konstante(value)


def add(left, right):
    return op.Addition(left, right)


def sub(left, right):
    return op.Subtraktion(left, right)


def mul(left, right):
    return op.Multiplikation(left, right)


def div(left, right):
    return op.Division(left, right)


def load(filename):
    return Daten.load(Daten, filename)


def read(name):
    return Daten.read(Daten, name)


def write(name, value):
    return Daten.write(Daten, name, value)


def store(filename):
    return Daten.store(Daten, filename)
