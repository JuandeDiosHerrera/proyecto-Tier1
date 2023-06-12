# coding=utf-8

import cv2
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join
import math
import numpy
from lineas import *

#Función de la etapa 3. Busca líneas horizontales en la mitad de la imagen, ya que la imagen es solo la banda de la que estamos haciendo el barrido.
def calcula_banda(image, height, width):
	plot_banda = 0
	plot_gradientes = 0
	plot_morfologia = 1
	edges, lines = Hough(image, 7) 

	vector_alturas_unidas = []
	vector_angulos_unidos = []
	for i in range(len(lines)):
		vector_alturas_unidas.append(lines[i][0][0])
		vector_angulos_unidos.append(lines[i][0][1])

	print('rho:', vector_alturas_unidas)
	print('theta:', vector_angulos_unidos)

	img_copy = pintar_lineas(image, height, width, lines, None, None)	
	filename = 'Lineas detectadas foto zoom.jpg'
	target = cv2.cvtColor(img_copy, cv2.COLOR_RGB2BGR)
	cv2.imwrite(filename, target)

	#Miro la altura de las líneas y desecho las que representan la misma línea horizontal para quedarme solo con una
	vector_alturas, vector_angulos = seleccion_lineas_definitivas(vector_alturas_unidas, vector_angulos_unidos, separacion = 300)
	img_copy2 = pintar_lineas(image, height, width, None, vector_alturas, vector_angulos)
	filename = 'Lineas definitivas foto zoom.jpg'
	target = cv2.cvtColor(img_copy2, cv2.COLOR_RGB2BGR)
	cv2.imwrite(filename, target)

	#Ordenamos alturas para formar máscara
	tam_vector, alturas_ordenadas, angulos_ordenados = ordena_alturas(vector_alturas, vector_angulos)

	#Formamos "vector_mascara" y creamos la máscara
	vector_mascara = []

	#Filtramos las líneas según sus alturas (nos quedamos con aquellas que están en la franja central de la imagen)
	alturas_ordenadas = [x for x in alturas_ordenadas if x > 850 and x < 2150]

	print('Altura banda zoom:',alturas_ordenadas)
	print('')

	vector_mascara.append([alturas_ordenadas[0], alturas_ordenadas[1]])
	#Máscara que elimina todo menos la banda
	mascara = creacion_mascara(height, width, vector_mascara, flag = 1)	

	#Aplicamos la máscara
	target = cv2.bitwise_and(image,image, mask=mascara)	
	filename = 'Banda aislada foto zoom.jpg'
	target = cv2.cvtColor(target, cv2.COLOR_RGB2BGR)
	cv2.imwrite(filename, target)
	
	target_gray = cv2.cvtColor(target, cv2.COLOR_RGB2GRAY)	

	if plot_banda == 1:
		plt.subplot(131),plt.imshow(image)
		plt.title('Zoom Image'), plt.xticks([]), plt.yticks([])
		plt.subplot(132),plt.imshow(target)
		plt.title('Banda identificada'), plt.xticks([]), plt.yticks([])		
		plt.subplot(133),plt.imshow(target_gray, cmap = 'gray')
		plt.title('Banda grayscale'), plt.xticks([]), plt.yticks([])			
		plt.show()	

	#Suavizado previo a calcular los gradientes vertical y horizontal de la imagen en escala de grises
	blurred = cv2.GaussianBlur(target_gray,(15,15),0)

	#Cálculo de gradientes y conversión a valores enteros positivos
	grad_x = cv2.Sobel(blurred, cv2.CV_16S, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
	abs_grad_x = cv2.convertScaleAbs(grad_x)

	grad_y = cv2.Sobel(blurred, cv2.CV_16S, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
	abs_grad_y = cv2.convertScaleAbs(grad_y)
	
	#Cálculo gradiente absoluto 
	gradient1 = cv2.subtract(grad_x, grad_y)
	gradient2 = cv2.convertScaleAbs(gradient1)
	filename = 'Valor absoluto gradiente foto zoom.jpg'
	target = cv2.cvtColor(gradient2, cv2.COLOR_RGB2BGR)
	cv2.imwrite(filename, target)

	if plot_gradientes == 1:
		plt.subplot(221),plt.imshow(abs_grad_x,cmap = 'gray')
		plt.title('Gradiente X'), plt.xticks([]), plt.yticks([])
		plt.subplot(222),plt.imshow(abs_grad_y,cmap = 'gray')
		plt.title('Gradiente Y'), plt.xticks([]), plt.yticks([])		
		plt.subplot(223),plt.imshow(gradient1,cmap = 'gray')
		plt.title('Resta'), plt.xticks([]), plt.yticks([])	
		plt.subplot(224),plt.imshow(gradient2,cmap = 'gray')
		plt.title('Valor absoluto'), plt.xticks([]), plt.yticks([])
		plt.show()				

	#Se binariza la imagen
	umbral,binaria = cv2.threshold(gradient2,45,255,cv2.THRESH_BINARY)

	#Se hace un cierre para formarlos rectángulos que engloban a los códigos de barras
	kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 5))   		# (Ancho, alto)
	closed = cv2.morphologyEx(binaria, cv2.MORPH_CLOSE, kernel1)

	#Luego se hace una apertura para limpiar la imagen y quedarnos solo con los rectángulos de los códigos de barras
	kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (45, 75))		# (Ancho, alto) 
	opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel2)

	#Resultado con la máscara que idealmente solo tiene los rectángulos de los códigos de barras, aunque puede tener puntos sueltos
	masked = cv2.bitwise_and(image, image, mask=opened)

	#Dilatado para asegurarnos que los rectángulos circunscriben a los códigos de barras por completo 
	kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 50))		# (Ancho, alto) 
	dilated = cv2.dilate(opened, kernel3)

	#Resultado con la máscara que tiene los códigos de barras cirncunscritos por completos
	masked2 = cv2.bitwise_and(image, image, mask=dilated)

	#Realizamos un etiquetado de la imagen binaria
	output = cv2.connectedComponentsWithStats(dilated, 4, cv2.CV_32S)
	(numLabels, labels, stats, centroids) = output

	mascara_area = numpy.zeros((height, width), dtype="uint8")

	for i in range(1, numLabels):		#Obviamos el índice 0 que corresponde al fondo negro
		x = stats[i, cv2.CC_STAT_LEFT]
		y = stats[i, cv2.CC_STAT_TOP]
		w = stats[i, cv2.CC_STAT_WIDTH]
		h = stats[i, cv2.CC_STAT_HEIGHT]
		area = stats[i, cv2.CC_STAT_AREA]

		#Umbral de píxeles que se aplica a cada etiqueta para eliminar los posibles puntos blancos sueltos de la imagen y, quedarnos seguro solo con los rectángulos de los códigos de barras
		ok_area = area > 100000 

		#Si el área de esa etiqueta es superior, añadimos esa etiqueta a la nueva máscara "mascara_area" que ya no contendrá los puntos sueltos
		if ok_area == True:
			componentMask = (labels == i).astype("uint8") * 255
			mascara_area = cv2.bitwise_or(mascara_area, componentMask)
	
	# plt.subplot(311),plt.imshow(image,cmap = 'gray')
	# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
	# plt.subplot(312),plt.imshow(dilated,cmap = 'gray')
	# plt.title('Dilatado'), plt.xticks([]), plt.yticks([])
	# plt.subplot(313),plt.imshow(mascara_area,cmap = 'gray')
	# plt.title('Máscara áreas'), plt.xticks([]), plt.yticks([])
	# plt.show()	

	#Resultado final tras eliminar los puntos sueltos 
	masked3 = cv2.bitwise_and(image, image, mask=mascara_area)

	if plot_morfologia == 1:
		plt.subplot(231),plt.imshow(image,cmap = 'gray')
		plt.title('Original image'), plt.xticks([]), plt.yticks([])
		plt.subplot(232),plt.imshow(binaria,cmap = 'gray')
		plt.title('Binaria'), plt.xticks([]), plt.yticks([])		
		plt.subplot(233),plt.imshow(closed,cmap = 'gray')
		plt.title('Cierre'), plt.xticks([]), plt.yticks([])	
		plt.subplot(234),plt.imshow(opened,cmap = 'gray')
		plt.title('Apertura'), plt.xticks([]), plt.yticks([])
		plt.subplot(235),plt.imshow(dilated,cmap = 'gray')
		plt.title('Dilatado'), plt.xticks([]), plt.yticks([])
		plt.subplot(236),plt.imshow(masked3)
		plt.title('Códigos detectados'), plt.xticks([]), plt.yticks([])
		plt.show()			

	print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------')
	print('')

	return target, target_gray, blurred, binaria, closed, opened, dilated, masked, masked2, masked3, mascara_area

def funcion():
	mypath='E:\\Documents\\Juan de Dios\\TFG\\Fotos gasolinera\\Zoom'
	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	images = numpy.empty(len(onlyfiles), dtype=object)
	for n in range(0, len(onlyfiles)):
		images[n] = cv2.imread( join(mypath,onlyfiles[n]) ) 
		images[n] = cv2.cvtColor(images[n], cv2.COLOR_BGR2RGB)

		height, width, channels = images[n].shape 

		target, target_gray, blurred, binaria, closed, opened, dilated, masked, masked2, masked3, mascara_area = calcula_banda(images[n], height, width)
		
		"""
		cv2.imshow('original', img)
		cv2.imshow('binaria', opened)
		cv2.imshow('Codigo aislado', masked)
		cv2.imshow('Contornos', image_copy)
		cv2.waitKey() 
		"""

		# Se buscan los contornos de los códigos de barras (rectángulos) y se pintan
		filtro_area_copy = mascara_area.copy()
		contours, hierarchy = cv2.findContours(filtro_area_copy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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
				cv2.drawContours(masked3, [i], -1, (0, 255, 0), 6)
				cv2.circle(masked3, (cx, cy), 40, (255, 0, 0), -1)
		
		plot_gradientes = 1
		if plot_gradientes == 1:
			plt.subplot(331),plt.imshow(images[n])
			plt.title('Zoom códigos'), plt.xticks([]), plt.yticks([])

			plt.subplot(332),plt.imshow(target_gray,cmap = 'gray')
			plt.title('Zoom escala de grises'), plt.xticks([]), plt.yticks([])

			# plt.subplot(233),plt.imshow(blurred,cmap = 'gray')
			# plt.title('Suavizado'), plt.xticks([]), plt.yticks([])

			plt.subplot(333),plt.imshow(binaria,cmap = 'gray')
			plt.title('Binaria'), plt.xticks([]), plt.yticks([])			
			
			plt.subplot(334),plt.imshow(closed,cmap = 'gray')
			plt.title('Cierre'), plt.xticks([]), plt.yticks([]) 

			plt.subplot(335),plt.imshow(opened,cmap = 'gray')
			plt.title('Apertura'), plt.xticks([]), plt.yticks([])

			plt.subplot(336),plt.imshow(dilated,cmap = 'gray')
			plt.title('Dilatado'), plt.xticks([]), plt.yticks([])

			plt.subplot(337),plt.imshow(mascara_area,cmap = 'gray')
			plt.title('Filtro área'), plt.xticks([]), plt.yticks([])

			plt.subplot(338),plt.imshow(masked3)
			plt.title('Códigos detectados'), plt.xticks([]), plt.yticks([])
			plt.show()	
	
#############################################PROBAR cv2.ADAPTIVE_THRESH_GAUSSIAN_C#########################################################

if __name__ == "__main__":              
	funcion()