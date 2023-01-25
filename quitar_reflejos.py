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
		_,mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

		red = numpy.array(images[n][:,:,0]) 
		green = numpy.array(images[n][:,:,1])
		blue = numpy.array(images[n][:,:,2])
		
		mascara_red = red > 200 
		mascara_green = green > 200 
		mascara_blue = blue > 200

		mascara = mascara_red & mascara_green & mascara_blue
		# r = red > 200
		# g = green > 200
		# b = blue > 200

		media_red = int(sum(red[mascara])/len(red[mascara]))
		media_green = int(sum(green[mascara])/len(green[mascara]))		#Mirar si meterle pesos para que la media dé más parecida al color de la etiqueta
		media_blue = int(sum(blue[mascara])/len(blue[mascara]))

		# print(len(red[mascara]),len(green[mascara]),len(blue[mascara]))
		print(media_red,media_green,media_blue)
		
		#First try
		img = images[n].copy()
		img[mask==255]=(media_red,media_green,media_blue)

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
		# dst = cv2.inpaint(images[n], mask, 15, cv2.INPAINT_NS)

		

		plt.subplot(131),plt.imshow(images[n])
		plt.title('Original Image'), plt.xticks([]), plt.yticks([])

		plt.subplot(132),plt.imshow(mask,cmap = 'gray')
		plt.title('Mask'), plt.xticks([]), plt.yticks([])

		plt.subplot(133),plt.imshow(img)
		plt.title('Result'), plt.xticks([]), plt.yticks([])
		plt.show()


if __name__ == "__main__":              
	funcion()