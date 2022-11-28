# coding=utf-8

import cv2
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join
import numpy
import math

w, h = 4, 12
mask = numpy.zeros((h, w), dtype=numpy.uint8)

hpairs = [[1,3],[8,12],]

for h0, h1 in hpairs:
    print(h0,h1+1)
    mask[h0:h1+1, :] = 1

print(mask)