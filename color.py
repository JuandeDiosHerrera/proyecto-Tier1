# coding=utf-8

import cv2
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join
import numpy
import math

def funcion():
	#mypath='C:\\Users\\joseh\\Documents\\Juan de Dios\\TFG\\Fotos'
	#mypath='E:\\Documents\\Juan de Dios\\TFG\\Fotos folio'
	mypath='E:\\Documents\\Juan de Dios\\TFG\\Fotos gasolinera'
	#mypath='E:\\Documents\\Juan de Dios\\TFG\\Fotos productos'
	#mypath='E:\\Documents\\Juan de Dios\\TFG\\Fotos Mercadona'
	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	images = numpy.empty(len(onlyfiles), dtype=object)
	for n in range(0, len(onlyfiles)):
		images[n] = cv2.imread( join(mypath,onlyfiles[n]) ) 
		hsv = cv2.cvtColor(images[n], cv2.COLOR_BGR2HSV)
		images[n] = cv2.cvtColor(images[n], cv2.COLOR_BGR2RGB)

		gray = cv2.cvtColor(images[n], cv2.COLOR_RGB2GRAY)

		height, width = gray.shape 
		# print('altura:',height)
		# print('ancho:',width)

		## mask of green (36,0,0) ~ (70, 255,255)
		# mask1 = cv2.inRange(hsv, (36, 0, 0), (70, 255,255))
		mask1 = cv2.inRange(hsv, (30, 50, 50), (50, 255,255))

		# kernel1 = numpy.ones((25,25),numpy.uint8)
		# print(kernel1)
		kernel_banda1 = cv2.getStructuringElement(cv2.MORPH_RECT, (100, 100))		# (Ancho, alto) 
		opened_banda = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, kernel_banda1)

		kernel_banda2 = cv2.getStructuringElement(cv2.MORPH_RECT, (4000, 1))		# (Ancho, alto) 
		closed_banda = cv2.morphologyEx(opened_banda, cv2.MORPH_CLOSE, kernel_banda2)

		# ## mask o yellow (15,0,0) ~ (36, 255, 255)
		# mask2 = cv2.inRange(hsv, (15,0,0), (36, 255, 255))

		# ## final mask and masked
		# mask = cv2.bitwise_or(mask1, mask2)
		target = cv2.bitwise_and(images[n],images[n], mask=closed_banda)

		plt.subplot(241),plt.imshow(images[n])
		plt.title('Original Image'), plt.xticks([]), plt.yticks([])

		plt.subplot(242),plt.imshow(mask1, cmap='gray')
		plt.title('Máscara color'), plt.xticks([]), plt.yticks([])

		plt.subplot(243),plt.imshow(opened_banda, cmap='gray')
		plt.title('Apertura'), plt.xticks([]), plt.yticks([])

		plt.subplot(244),plt.imshow(closed_banda, cmap='gray')
		plt.title('Cierre'), plt.xticks([]), plt.yticks([])

		plt.subplot(245),plt.imshow(target)
		plt.title('Color detection'), plt.xticks([]), plt.yticks([])
		
		
		
		# plt.subplot(224),plt.imshow(img_copy2)
		# plt.title('Líneas definitivas'), plt.xticks([]), plt.yticks([])		
		plt.show()

if __name__ == "__main__":              
	funcion()