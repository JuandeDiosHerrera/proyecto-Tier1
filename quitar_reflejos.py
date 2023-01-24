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
		# images[n] = cv2.imread( join(mypath,onlyfiles[n]) ) 
		# hsv = cv2.cvtColor(images[n], cv2.COLOR_BGR2HSV)
		# images[n] = cv2.cvtColor(images[n], cv2.COLOR_BGR2RGB)

		# gray = cv2.cvtColor(images[n], cv2.COLOR_RGB2GRAY)
		# height, width, channels = images[n].shape 

		# red = images[n][:,:,0] > 200 
		# green = images[n][:,:,1] > 200 
		# blue = images[n][:,:,2] > 200

		# color = red & green & blue
		# # print(color)

		# # mask = numpy.zeros((height, width),numpy.uint8)

		# mask = cv2.threshold(gray,200,255,cv2.THRESH_BINARY)[1]
		# # mask[color==False]=(0,0,0)

		# result = cv2.inpaint(src=images[n], inpaintMask=mask, inpaintRadius=5, flags=cv2.INPAINT_TELEA) 


		images[n] = cv2.imread( join(mypath,onlyfiles[n]) ) 
		images[n] = cv2.cvtColor(images[n], cv2.COLOR_BGR2RGB)

		gray = cv2.cvtColor(images[n], cv2.COLOR_RGB2GRAY)

		# Binary threshold image
		mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
		
		#First try
		img = images[n].copy()
		img[mask==255]=(180,180,180)

		#Second try
		# img = numpy.where(mask == 255,180,images[n])

		# Remove small noise
		# inp_mask = cv2.morphologyEx(mask,
		# 							cv2.MORPH_OPEN,
		# 							cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))

		# # Dilate mask
		# inp_mask = cv2.dilate(inp_mask,
		# 					cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))

		# Inpaint
		# dst = cv2.inpaint(images[n], mask, 1, cv2.INPAINT_NS)




		plt.subplot(131),plt.imshow(images[n])
		plt.title('Original Image'), plt.xticks([]), plt.yticks([])

		# plt.subplot(132),plt.imshow(mask,cmap = 'gray')
		# plt.title('Mask'), plt.xticks([]), plt.yticks([])

		plt.subplot(133),plt.imshow(img)
		plt.title('Result'), plt.xticks([]), plt.yticks([])
		plt.show()


if __name__ == "__main__":              
	funcion()