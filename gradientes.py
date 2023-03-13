# coding=utf-8

import cv2
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join
import math
import numpy
from lineas import *
# from lineas import Hough
# from lineas import pintar_lineas
# from lineas import seleccion_lineas_definitivas
# from lineas import ordena_alturas
# from lineas import creacion_mascara

def calcula_banda_central(image, height, width):
	#Se supone que partimos de la imagen con las bandas identificadas, luego vamos a calcular Hough para adaptar la imagen a que solo tenga las 
	#bandas y los productos con píxeles negros
	edges, lines = Hough(image, 7) 
	# print(lines)
	# print('')

	vector_alturas_unidas = []
	vector_angulos_unidos = []
	for i in range(len(lines)):
		#print(i)
		vector_alturas_unidas.append(lines[i][0][0])
		vector_angulos_unidos.append(lines[i][0][1])

	print('rho:', vector_alturas_unidas)
	print('theta:', vector_angulos_unidos)

	img_copy = pintar_lineas(image, height, width, lines, None, None)	#Para pintar todas las líneas detectadas

	#Saco las dos líneas que delimitan la banda
	vector_alturas, vector_angulos = seleccion_lineas_definitivas(vector_alturas_unidas, vector_angulos_unidos, separacion = 300)

	#Ordenamos alturas para formar máscara
	tam_vector, alturas_ordenadas, angulos_ordenados = ordena_alturas(vector_alturas, vector_angulos)

	#Formamos "vector_mascara" y creamos la máscara
	vector_mascara = []
	# for i in range(len(alturas_ordenadas)):
	# 	if alturas_ordenadas[i] >

	alturas_ordenadas = [x for x in alturas_ordenadas if x > 850 and x < 2250]

	print('alturas_ordenadas filtradas:',alturas_ordenadas)

	vector_mascara.append([alturas_ordenadas[0], alturas_ordenadas[1]])
	mascara = creacion_mascara(height, width, vector_mascara, flag = 1)	

	#Aplicamos la máscara
	target = cv2.bitwise_and(image,image, mask=mascara)

	target_gray = cv2.cvtColor(target, cv2.COLOR_RGB2GRAY)	

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

	masked = cv2.bitwise_and(image, image, mask=opened)

	return target_gray, binaria, closed, opened, masked

def funcion():
	mypath='E:\\Documents\\Juan de Dios\\TFG\\Fotos gasolinera\\Zoom'
	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	print(onlyfiles)
	images = numpy.empty(len(onlyfiles), dtype=object)
	for n in range(0, len(onlyfiles)):
		images[n] = cv2.imread( join(mypath,onlyfiles[n]) ) 
		images[n] = cv2.cvtColor(images[n], cv2.COLOR_BGR2RGB)

		height, width, channels = images[n].shape 

		target_gray, binaria, closed, opened, masked = calcula_banda_central(images[n], height, width)
		
		"""
		cv2.imshow('original', img)
		cv2.imshow('binaria', opened)
		cv2.imshow('Codigo aislado', masked)
		cv2.imshow('Contornos', image_copy)
		cv2.waitKey() 
		"""

		# Se buscan los contornos de los códigos de barras (rectángulos) y se pintan
		opened_copy = opened.copy()
		contours, hierarchy = cv2.findContours(opened_copy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		image_copy = images[n].copy()

		"""
		# Obtención de los rectángulos que circunscriben a los códigos de barras
		minRect = [None]*len(contours)
		#print(range(len(contours[0])))
		#print(contours)
		for i in range(len(contours[0])):
			c = contours[0][i][0]
			print(type(c))
			minRect[i] = cv2.minAreaRect(c)
		
		# Para sacar solo las esquinas del contorno no el contorno entero	
		for i in range(len(contours[0])):
			x = contours[0][i][0][0]
			y = contours[0][i][0][1]
			#print(x,y)
			cv2.circle(image_copy, (x,y), 7, (0,0,255), -1)
			#cv2.drawContours(image_copy, [contours[i], [], (0,0,255), 6)
			#cv2.drawContours(image_copy, [contours[i], 1, (0,0,255), 6)
		"""

		#Obtención del píxel central de los códigos de barras identificados
		for i in contours:
			M = cv2.moments(i)
			if M['m00'] != 0:
				cx = int(M['m10']/M['m00'])
				cy = int(M['m01']/M['m00'])
				cv2.drawContours(masked, [i], -1, (0, 255, 0), 6)
				cv2.circle(masked, (cx, cy), 40, (255, 0, 0), -1)
		
		plot_gradientes = 1
		if plot_gradientes == 1:
			plt.subplot(231),plt.imshow(images[n])
			plt.title('Zoom códigos'), plt.xticks([]), plt.yticks([])

			plt.subplot(232),plt.imshow(target_gray,cmap = 'gray')
			plt.title('Zoom escala de grises'), plt.xticks([]), plt.yticks([])

			# plt.subplot(233),plt.imshow(blurred,cmap = 'gray')
			# plt.title('Suavizado'), plt.xticks([]), plt.yticks([])

			plt.subplot(233),plt.imshow(binaria,cmap = 'gray')
			plt.title('Binaria'), plt.xticks([]), plt.yticks([])			
			
			plt.subplot(234),plt.imshow(closed,cmap = 'gray')
			plt.title('Cierre'), plt.xticks([]), plt.yticks([]) 

			plt.subplot(235),plt.imshow(opened,cmap = 'gray')
			plt.title('Apertura'), plt.xticks([]), plt.yticks([])

			plt.subplot(236),plt.imshow(masked)
			plt.title('Códigos detectados'), plt.xticks([]), plt.yticks([])
			plt.show()	
	
#############################################PROBAR cv2.ADAPTIVE_THRESH_GAUSSIAN_C#########################################################

if __name__ == "__main__":              
	funcion()