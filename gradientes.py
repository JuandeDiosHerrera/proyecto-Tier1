# coding=utf-8

import cv2
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join
import math
import numpy

def funcion():
	mypath='E:\\Documents\\Juan de Dios\\TFG\\Fotos gasolinera\\Zoom'
	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	images = numpy.empty(len(onlyfiles), dtype=object)
	for n in range(0, len(onlyfiles)):
		images[n] = cv2.imread( join(mypath,onlyfiles[n]) ) 
		target_gray = cv2.cvtColor(images[n], cv2.COLOR_BGR2GRAY)	
		images[n] = cv2.cvtColor(images[n], cv2.COLOR_BGR2RGB)

		#Cálculo gradientes y conversión a valores enteros positivos
		grad_x = cv2.Sobel(target_gray, cv2.CV_16S, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
		abs_grad_x = cv2.convertScaleAbs(grad_x)

		grad_y = cv2.Sobel(target_gray, cv2.CV_16S, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
		abs_grad_y = cv2.convertScaleAbs(grad_y)
		
		#Cálculo gradiente absoluto 
		gradient1 = cv2.subtract(grad_x, grad_y)
		gradient2 = cv2.convertScaleAbs(gradient1)
		#print(gradient2.max())
		#print(gradient2.min())

		#Suavizado: probar cuál funciona mejor (gaussiano)
		#blurred = cv2.blur(gradient2, (25, 25))
		blurred = cv2.GaussianBlur(gradient2,(15,15),0)
		#blurred = cv2.boxFilter(gradient2, -1, (25,25))
		#blurred = cv2.medianBlur(gradient2,5)
		#blurred = cv2.bilateralFilter(gradient2,9,75,75)

		#Plot gradientes
		# plt.subplot(221),plt.imshow(abs_grad_x,cmap = 'gray')
		# plt.title('Gradiente X'), plt.xticks([]), plt.yticks([])
		# plt.subplot(222),plt.imshow(abs_grad_y,cmap = 'gray')
		# plt.title('Gradiente Y'), plt.xticks([]), plt.yticks([])		
		# plt.subplot(223),plt.imshow(gradient1,cmap = 'gray')
		# plt.title('Resta'), plt.xticks([]), plt.yticks([])		
		# plt.subplot(224),plt.imshow(gradient2,cmap = 'gray')
		# plt.title('Valor absoluto'), plt.xticks([]), plt.yticks([])
		# plt.show()				

		#Se binariza la imagen, se hace paertura y luego se cierra para formar el rectángulo que engloba al código de barras
		umbral,binaria = cv2.threshold(blurred,75,255,cv2.THRESH_BINARY)	    #Para gasolinera
		# umbral,binaria = cv2.threshold(blurred,75,255,cv2.THRESH_BINARY)		#Para Mercadona

		# kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))   		# (Ancho, alto)
		kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 5))   		# (Ancho, alto)

		# kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 12))   		# (Ancho, alto)
		closed = cv2.morphologyEx(binaria, cv2.MORPH_CLOSE, kernel1)

		kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 75))		# (Ancho, alto) 
		# kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 3))		# (Ancho, alto) 
		opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel2)

		image_copy = images[n].copy()

		# masked = cv2.bitwise_and(images[n], images[n], mask=closed)
		
		"""
		cv2.imshow('original', img)
		cv2.imshow('binaria', opened)
		cv2.imshow('Codigo aislado', masked)
		cv2.imshow('Contornos', image_copy)
		cv2.waitKey() 
		"""
		
		plot_gradientes = 1
		if plot_gradientes == 1:
			plt.subplot(231),plt.imshow(images[n])
			plt.title('Zoom códigos'), plt.xticks([]), plt.yticks([])

			plt.subplot(232),plt.imshow(target_gray,cmap = 'gray')
			plt.title('Zoom escala de grises'), plt.xticks([]), plt.yticks([])

			plt.subplot(233),plt.imshow(blurred,cmap = 'gray')
			plt.title('Suavizado'), plt.xticks([]), plt.yticks([])

			plt.subplot(234),plt.imshow(binaria,cmap = 'gray')
			plt.title('Binaria'), plt.xticks([]), plt.yticks([])

			plt.subplot(236),plt.imshow(opened,cmap = 'gray')
			plt.title('Apertura'), plt.xticks([]), plt.yticks([])
			
			plt.subplot(235),plt.imshow(closed,cmap = 'gray')
			plt.title('Cierre'), plt.xticks([]), plt.yticks([]) 
			
			# plt.subplot(236),plt.imshow(masked,cmap = 'gray')
			# plt.title('Códigos detectados'), plt.xticks([]), plt.yticks([])
			plt.show()	
	
#############################################PROBAR cv2.ADAPTIVE_THRESH_GAUSSIAN_C#########################################################

if __name__ == "__main__":              
	funcion()