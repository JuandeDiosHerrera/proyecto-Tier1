# coding=utf-8

import cv2
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join
import math
import numpy

def funcion():
	#mypath='C:\\Users\\joseh\\Documents\\Juan de Dios\\TFG\\Fotos'
	#mypath='E:\\Documents\\Juan de Dios\\TFG\\Fotos folio'
	# mypath='E:\\Documents\\Juan de Dios\\TFG\\Fotos gasolinera'
	#mypath='E:\\Documents\\Juan de Dios\\TFG\\Fotos productos'
	mypath='E:\\Documents\\Juan de Dios\\TFG\\Fotos Mercadona\\4B'
	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	images = numpy.empty(len(onlyfiles), dtype=object)
	for n in range(0, len(onlyfiles)):
		images[n] = cv2.imread( join(mypath,onlyfiles[n]) ) 
		hsv = cv2.cvtColor(images[n], cv2.COLOR_BGR2HSV)
		images[n] = cv2.cvtColor(images[n], cv2.COLOR_BGR2RGB)

		gray = cv2.cvtColor(images[n], cv2.COLOR_RGB2GRAY)
		height, width, channels = images[n].shape 

		red = images[n][:,:,0] > 200 
		green = images[n][:,:,1] > 200 
		blue = images[n][:,:,2] > 200
	
		# mask = numpy.zeros((height, width),numpy.uint8)
		mask = red & green & blue	
		print(type(mask))
		mask = mask.astype(numpy.uint8)
		
		plt.subplot(121),plt.imshow(images[n],cmap = 'gray')
		plt.title('Original Image'), plt.xticks([]), plt.yticks([])

		plt.subplot(122),plt.imshow(mask,cmap = 'gray')
		plt.title('Mask'), plt.xticks([]), plt.yticks([])
		plt.show()

		# gray = cv2.cvtColor(images[n], cv2.COLOR_BGR2GRAY)
		# mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)


		result = cv2.inpaint(images[n], mask, 21, cv2.INPAINT_TELEA) 

		plt.subplot(311),plt.imshow(images[n],cmap = 'gray')
		plt.title('Original Image'), plt.xticks([]), plt.yticks([])

		plt.subplot(312),plt.imshow(mask,cmap = 'gray')
		plt.title('Mask'), plt.xticks([]), plt.yticks([])

		plt.subplot(313),plt.imshow(result,cmap = 'gray')
		plt.title('Result'), plt.xticks([]), plt.yticks([])
		plt.show()


if __name__ == "__main__":              
	funcion()