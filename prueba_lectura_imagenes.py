# coding=utf-8

import cv2
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join
import math
import numpy
from natsort import natsorted

def funcion():
	#Primer bucle para leer las fotos normales
	mypath1='E:\\Documents\\Juan de Dios\\TFG\\Fotos Mercadona\\Misma altura'
	onlyfiles1 = [ f for f in listdir(mypath1) if isfile(join(mypath1,f)) ]
	onlyfiles1 = natsorted(onlyfiles1)
	print(onlyfiles1)
	images1 = numpy.empty(len(onlyfiles1), dtype=object)
	for n in range(0, len(onlyfiles1)):
		images1[n] = cv2.imread( join(mypath1,onlyfiles1[n]) ) 
		images1[n] = cv2.cvtColor(images1[n], cv2.COLOR_BGR2RGB)

		plt.subplot(111),plt.imshow(images1[n])	#Pinto las líneas definitivas
		plt.title('Foto'), plt.xticks([]), plt.yticks([])
		plt.show()

		#Segundo bucle para leer las fotos con zoom de las bandas identificadas
		mypath2='E:\\Documents\\Juan de Dios\\TFG\\Fotos Mercadona\\2B'
		onlyfiles2 = [ f for f in listdir(mypath2) if isfile(join(mypath2,f)) ]
		onlyfiles2 = natsorted(onlyfiles2)
		print(onlyfiles2)
		images2 = numpy.empty(len(onlyfiles2), dtype=object)
		for m in range(0, len(onlyfiles2)):
			images2[m] = cv2.imread( join(mypath2,onlyfiles2[m]) ) 
			images2[m] = cv2.cvtColor(images2[m], cv2.COLOR_BGR2RGB)

			plt.subplot(111),plt.imshow(images2[m])	#Pinto las líneas definitivas
			plt.title('Foto'), plt.xticks([]), plt.yticks([])
			plt.show()

if __name__ == "__main__":              
	funcion()


# cv_img = []
# for img in path:
#     n = cv.imread(img)
#     cv_img.append(n)