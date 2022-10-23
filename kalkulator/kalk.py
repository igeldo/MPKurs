from daten import Daten
from operatoren import Konstante
import matplotlib.mathtext as mt

def const(value):
    return Konstante(value)


def load(filename):
    return Daten.load(Daten, filename)


def read(name):
    return Daten.read(Daten, name)


def write(name, wert):
    latex = wert.latex() + r"=" + wert.latexVector(wert.value())
    mt.math_to_image(r"$" + latex + r"$", f"data/{name}.png", dpi=600)
    return Daten.write(Daten, name, wert)


def store(filename):
    return Daten.store(Daten, filename)
