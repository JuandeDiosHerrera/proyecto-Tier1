# coding=utf-8

import cv2
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join
import numpy

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

		height, width, channels = images[n].shape 
		#print('alto:', height)
		#print('ancho:', width)

		gray = cv2.cvtColor(images[n], cv2.COLOR_RGB2GRAY)

		# Aislamos por el color las bandas horizontales
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
		target = cv2.bitwise_and(gray,gray, mask=closed_banda)
		
		"""
		gaus = cv2.GaussianBlur(gray,(5,5),0)
		"""
		# Cálculo gradientes y conversión a valores enteros positivos
		grad_x = cv2.Sobel(target, cv2.CV_16S, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
		abs_grad_x = cv2.convertScaleAbs(grad_x)

		grad_y = cv2.Sobel(target, cv2.CV_16S, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
		abs_grad_y = cv2.convertScaleAbs(grad_y)
		"""
		grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

		cv2.imshow('gray', grad)
		cv2.waitKey() 
		"""
		"""
		#######################################################################Forma 1##################################################################################3
		median = cv2.medianBlur(gray, 5)
		#print("Tipo de median", type(median))
		#print("Tipo de grad_x", type(grad_x))

		umbral,binaria1 = cv2.threshold(abs_grad_x,200,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		#print(umbral)
		#cv2.imshow('original', img)
		#cv2.imshow('gradiente X abs', abs_grad_x)
		#cv2.imshow('gradiente Y abs', abs_grad_y)
		#cv2.imshow('binaria1', binaria1)
		#cv2.imshow('binaria1', binaria1)
		"""
		#######################################################################Forma 2##################################################################################3
		# Cálculo gradiente absoluto 
		gradient1 = cv2.subtract(grad_x, grad_y)
		gradient2 = cv2.convertScaleAbs(gradient1)
		#print(gradient2.max())
		#print(gradient2.min())

		# Suavizado: probar cuál funciona mejor
		#blurred = cv2.blur(gradient2, (25, 25))
		blurred = cv2.GaussianBlur(gradient2,(25,25),0)
		#blurred = cv2.boxFilter(gradient2, -1, (25,25))

		#blurred = cv2.medianBlur(gradient2,5)
		#blurred = cv2.bilateralFilter(gradient2,9,75,75)


		#print(blurred.max())
		#print(blurred.min())
		# Se binariza la imagen y se cierra para formar el rectángulo que engloba al código de barras
		umbral,binaria = cv2.threshold(blurred,150,255,cv2.THRESH_BINARY)
		#cv2.imshow('binaria', binaria)
		#print(binaria.max())
		kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))   
		#print(kernel1)
		opened = cv2.morphologyEx(binaria, cv2.MORPH_OPEN, kernel1)
		#cv2.imshow('cierre', closed)

		kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 3))		# (Ancho, alto) 
		closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel2)
		#opened = cv2.erode(closed, kernel2, iterations = 1)
		#opened = cv2.dilate(closed, kernel2, iterations = 4)
		
		binaria1 = cv2.adaptiveThreshold(gradient2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,251,0)
		#binaria2 = cv2.adaptiveThreshold(gradient,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,251,0)

		"""
		plt.subplot(231),plt.imshow(images[n])
		plt.title('Original Image'), plt.xticks([]), plt.yticks([])

		plt.subplot(232),plt.imshow(grad_x,cmap = 'gray')
		plt.title('gradiente x'), plt.xticks([]), plt.yticks([])

		plt.subplot(233),plt.imshow(grad_y,cmap = 'gray')
		plt.title('gradiente y'), plt.xticks([]), plt.yticks([])

		plt.subplot(234),plt.imshow(gradient1,cmap = 'gray')
		plt.title('gradiente restado'), plt.xticks([]), plt.yticks([])

		plt.subplot(235),plt.imshow(gradient2,cmap = 'gray')
		plt.title('gradiente restado y valor absoluto'), plt.xticks([]), plt.yticks([])
		plt.show()
		"""

		"""
		print('Maximo binaria:',binaria.max())
		print('\n')
		print('Minimo binaria:',binaria.min())
		print('\n')
		print('Maximo binaria1:',binaria1.max())
		print('\n')
		print('Maximo binaria1:',binaria1.min())
		#cv2.imshow('apertura', opened)
		"""
		
		# Se buscan los contornos del rectángulo y se pintan
		opened_copy = opened.copy()
		contours, hierarchy = cv2.findContours(opened_copy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		image_copy = images[n].copy()

		"""
		# Para sacar solo las esquinas del contorno no el contorno entero	
		for i in range(len(contours[0])):
			x = contours[0][i][0][0]
			y = contours[0][i][0][1]
			#print(x,y)
			cv2.circle(image_copy, (x,y), 20, (0,0,255), -1)
			#cv2.drawContours(image_copy, [contours[i], [], (0,0,255), 6)
			#cv2.drawContours(image_copy, [contours[i], 1, (0,0,255), 6)
		"""
		
		for i in contours:
			M = cv2.moments(i)
			#if M['m00'] != 0:
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])
			#cv2.drawContours(image_copy, [i], -1, (0, 255, 0), 6)
			cv2.circle(image_copy, (cx, cy), 20, (131, 255, 0), -1)
		

		masked = cv2.bitwise_and(images[n], images[n], mask=opened)
		
		"""
		cv2.imshow('original', img)
		cv2.imshow('binaria', opened)
		cv2.imshow('Codigo aislado', masked)
		cv2.imshow('Contornos', image_copy)
		cv2.waitKey() 
		"""

		plt.subplot(231),plt.imshow(images[n])
		plt.title('Original Image'), plt.xticks([]), plt.yticks([])

		plt.subplot(232),plt.imshow(gradient2,cmap = 'gray')
		plt.title('Resta y valor abs'), plt.xticks([]), plt.yticks([])

		plt.subplot(233),plt.imshow(blurred,cmap = 'gray')
		plt.title('Suavizado'), plt.xticks([]), plt.yticks([])

		plt.subplot(234),plt.imshow(binaria,cmap = 'gray')
		plt.title('Binaria'), plt.xticks([]), plt.yticks([])
		
		plt.subplot(235),plt.imshow(opened,cmap = 'gray')
		plt.title('Apertura'), plt.xticks([]), plt.yticks([])
		
		plt.subplot(236),plt.imshow(closed,cmap = 'gray')
		plt.title('Cierre'), plt.xticks([]), plt.yticks([])
		plt.show()

		"""
		plt.subplot(231),plt.imshow(images[n])
		plt.title('Original Image'), plt.xticks([]), plt.yticks([])

		plt.subplot(232),plt.imshow(binaria,cmap = 'gray')
		plt.title('Binaria Global'), plt.xticks([]), plt.yticks([])

		plt.subplot(233),plt.imshow(opened,cmap = 'gray')
		plt.title('Morphologic Image'), plt.xticks([]), plt.yticks([])

		plt.subplot(234),plt.imshow(binaria1,cmap = 'gray')
		plt.title('Binaria Adaptativa'), plt.xticks([]), plt.yticks([])
		
		plt.subplot(235),plt.imshow(image_copy,cmap = 'gray')
		plt.title('Centros de masa'), plt.xticks([]), plt.yticks([])
		
		plt.subplot(236),plt.imshow(masked)
		plt.title('Barcode detection'), plt.xticks([]), plt.yticks([])
		plt.show()
		"""
	#############################################PROBAR cv2.ADAPTIVE_THRESH_GAUSSIAN_C#########################################################

if __name__ == "__main__":              
	funcion()






