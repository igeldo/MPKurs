import os
import csv
import matplotlib.pyplot as plt

def output(path, filename, delimiter=';'):
    file = open(os.path.join(path, filename), "w", newline='')
    writer = csv.writer(file, delimiter=delimiter)
    writer.writerow(['x', 'y', 'z', 'ux', 'uy', 'uz', 'stepSizeL'])
    writer.writerow([x,y,z,ux,uy,uz,stepSizeL]) #  TODO: mäke gedänken drüber
