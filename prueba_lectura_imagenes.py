# coding=utf-8

import cv2
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join
import math
import numpy

def funcion():
	mypath='E:\\Documents\\Juan de Dios\\TFG\\Fotos Mercadona\\Misma altura'
	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	images = numpy.empty(len(onlyfiles), dtype=object)
	for n in range(0, len(onlyfiles)):
		images[n] = cv2.imread( join(mypath,onlyfiles[n]) ) 
		images[n] = cv2.cvtColor(images[n], cv2.COLOR_BGR2RGB)

		plt.subplot(111),plt.imshow(images[n])	#Pinto las líneas definitivas
		plt.title('Foto'), plt.xticks([]), plt.yticks([])
		plt.show()




if __name__ == "__main__":              
	funcion()