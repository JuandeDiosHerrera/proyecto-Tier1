# coding=utf-8

import cv2
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join
import numpy

def funcion():

	mypath='E:\\Documents\\Juan de Dios\\TFG\\Fotos'
	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	images = numpy.empty(len(onlyfiles), dtype=object)
	for n in range(0, len(onlyfiles)):
		images[n] = cv2.imread( join(mypath,onlyfiles[n]) ) 
		height, width, channels = images[n].shape 

		gray = cv2.cvtColor(images[n], cv2.COLOR_BGR2GRAY)
		#print('alto:', height)
		#print('ancho:', width)
		"""
		gaus = cv2.GaussianBlur(gray,(5,5),0)
		"""
		# Cálculo gradientes y conversión a valores enteros positivos
		grad_x = cv2.Sobel(gray, cv2.CV_16S, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
		abs_grad_x = cv2.convertScaleAbs(grad_x)

		grad_y = cv2.Sobel(gray, cv2.CV_16S, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
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
		gradient = cv2.subtract(grad_x, grad_y)
		gradient = cv2.convertScaleAbs(gradient)
		#blurred = cv2.blur(gradient, (9, 9))

		# Se binariza la imagen y se cierra para formar el rectángulo que engloba al código de barras
		umbral,binaria = cv2.threshold(gradient,200,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		#cv2.imshow('binaria', binaria)
		kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (75, 7))
		closed = cv2.morphologyEx(binaria, cv2.MORPH_CLOSE, kernel1)
		#cv2.imshow('cierre', closed)

		kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 75))
		opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel2)
		#opened = cv2.erode(closed, kernel2, iterations = 4)
		#opened = cv2.dilate(closed, kernel2, iterations = 4)
		
		binaria1 = cv2.adaptiveThreshold(gradient,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,251,0)
		#binaria2 = cv2.adaptiveThreshold(gradient,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,251,0)
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

		# Para sacar solo las esquinas del contorno no el contorno entero	
		for i in range(len(contours[0])):
			x = contours[0][i][0][0]
			y = contours[0][i][0][1]
			#print(x,y)
			cv2.circle(image_copy, (x,y), 7, (0,0,255), -1)
			#cv2.drawContours(image_copy, [contours[i], [], (0,0,255), 6)
			#cv2.drawContours(image_copy, [contours[i], 1, (0,0,255), 6)


		for i in contours:
			M = cv2.moments(i)
			if M['m00'] != 0:
				cx = int(M['m10']/M['m00'])
				cy = int(M['m01']/M['m00'])
				#cv2.drawContours(image_copy, [i], -1, (0, 255, 0), 6)
				cv2.circle(image_copy, (cx, cy), 7, (255, 0, 0), -1)

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

		plt.subplot(232),plt.imshow(binaria,cmap = 'gray')
		plt.title('Binaria Global'), plt.xticks([]), plt.yticks([])

		plt.subplot(233),plt.imshow(opened,cmap = 'gray')
		plt.title('Morphologic Image'), plt.xticks([]), plt.yticks([])

		plt.subplot(234),plt.imshow(binaria1,cmap = 'gray')
		plt.title('Binaria Adaptativa'), plt.xticks([]), plt.yticks([])
		"""
		plt.subplot(235),plt.imshow(binaria2,cmap = 'gray')
		plt.title('Binaria Adaptativa flag inverso'), plt.xticks([]), plt.yticks([])
		"""
		plt.subplot(236),plt.imshow(masked)
		plt.title('Barcode detection'), plt.xticks([]), plt.yticks([])
		plt.show()

	#############################################PROBAR cv2.ADAPTIVE_THRESH_GAUSSIAN_C#########################################################

if __name__ == "__main__":              
	funcion()






