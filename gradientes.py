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

		# gray = cv2.cvtColor(images[n], cv2.COLOR_RGB2GRAY)

		filtro_color = 0

		plot_gradientes = 1
		plot_color = 0
		plot_hough = 0

		#Busco las bandas horizontales por su color
		if filtro_color == 1:
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
			target = cv2.bitwise_and(images[n],images[n], mask=closed_banda)

			if plot_color == 1:
				# print('hola')
				plt.subplot(231),plt.imshow(images[n])
				plt.title('Original Image'), plt.xticks([]), plt.yticks([])

				plt.subplot(232),plt.imshow(mask1, cmap='gray')
				plt.title('Máscara color'), plt.xticks([]), plt.yticks([])

				plt.subplot(233),plt.imshow(opened_banda, cmap='gray')
				plt.title('Apertura'), plt.xticks([]), plt.yticks([])

				plt.subplot(234),plt.imshow(closed_banda, cmap='gray')
				plt.title('Cierre'), plt.xticks([]), plt.yticks([])

				plt.subplot(235),plt.imshow(target)
				plt.title('Color detection'), plt.xticks([]), plt.yticks([])
				plt.show()
		
		# Busco las bandas horizontales por transformada de Hough
		else:
			edges = cv2.Canny(images[n],125,225,apertureSize=3,L2gradient=True)
			#print(edges)
			height, width = edges.shape
			#print(height,width)

			kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))		# (Ancho, alto)
			#closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

			#Búsqueda de líneas horizontales: en el rango [85º,95º] -> aumento umbral de 100 en 100 hasta quedarme con 15 líneas detectadas o menos
			lineas_detectadas = 2000
			umbral = 100
			while(lineas_detectadas>15):
				lines = cv2.HoughLines(edges,rho=1,theta=numpy.pi/180,threshold=umbral,srn=0,stn=0,min_theta=numpy.pi/2-0.08726,max_theta=numpy.pi/2+0.08726)
				# print(lines)
				lineas_detectadas = len(lines)
				print(len(lines),umbral)
				umbral += 100

			#print(lines)
			print('')

			img_copy1 = images[n].copy()
			img_copy2 = images[n].copy()

			if lines is not None:
				for i in range(len(lines)):
					#print(i)
					rho = lines[i][0][0]
					theta = lines[i][0][1]
					#print(rho,theta)
					a = math.cos(theta)
					b = math.sin(theta)
					x0 = a * rho				# x = rho * cos(theta)
					y0 = b * rho				# y = rho * sin(theta)
					pt1 = (int(x0 + math.sqrt(height**2+width**2)*(-b)), int(y0 + math.sqrt(height**2+width**2)*(a)))			#Tamaño imagen: 3000(alto) x 4000(ancho)
					pt2 = (int(x0 - math.sqrt(height**2+width**2)*(-b)), int(y0 - math.sqrt(height**2+width**2)*(a)))
					#print(pt1,pt2)
					cv2.line(img_copy1, pt1, pt2, (255,0,0), 10, cv2.LINE_AA)

				#Miro la altura de las líneas y desecho las que representan la misma línea horizontal para quedarme solo con una
				vector_alturas = []
				vector_angulos = []
				primera_iter = 1
				distinto = 1
			
				for i in lines:
					print('rho:',i[0][0])
					distinto = 1
					if primera_iter == 1:
						vector_alturas.append(i[0][0])
						vector_angulos.append(i[0][1])
						primera_iter = 0

					if primera_iter == 0:
						for j in vector_alturas:
							print('elemento vector:',j)
							if abs(i[0][0] - j) < 100:			#Líneas separadas menos de 100 píxeles se considera que representan la misma horizontal
								print('Misma línea----------------------')
								print('Vector_alturas:',vector_alturas)
								print('Vector_angulos:',vector_angulos)
								print('')
								distinto = 0
								break

						if distinto == 1:						#Una vez comprobado que es distinto a todos los elementos ya existentes en "vector_alturas"
							vector_alturas.append(i[0][0])		#los añadimos
							vector_angulos.append(i[0][1])
							print('Añadimos línea-----------------------')
							print('Vector_alturas:',vector_alturas)
							print('Vector_angulos:',vector_angulos)
							print('')

				#Pinto las líneas definitivas			
				for i in range(len(vector_alturas)):
					#print(i)
					rho = vector_alturas[i]
					theta = vector_angulos[i]
					#print(rho,theta)
					a = math.cos(theta)
					b = math.sin(theta)
					x0 = a * rho				# x = rho * cos(theta)
					y0 = b * rho				# y = rho * sin(theta)
					pt1 = (int(x0 + math.sqrt(height**2+width**2)*(-b)), int(y0 + math.sqrt(height**2+width**2)*(a)))			#Tamaño imagen: 3000(alto) x 4000(ancho)
					pt2 = (int(x0 - math.sqrt(height**2+width**2)*(-b)), int(y0 - math.sqrt(height**2+width**2)*(a)))
					#print(pt1,pt2)
					cv2.line(img_copy2, pt1, pt2, (255,0,0), 10, cv2.LINE_AA)

			tam_vector = len(vector_alturas)
			print('Tamaño vector:',tam_vector)
			print('')

			#Ordenamos los vectores de menor rho a mayor y los ángulos acorde a cómo se han ordenado las distancias (rho)
			alturas_ordenadas, angulos_ordenados = zip(*sorted(zip(vector_alturas, vector_angulos)))
			print('Vector alturas ordenados:',alturas_ordenadas)
			print('Vector ángulos ordenados:',angulos_ordenados)
			print('')

			#Emparejamos las líneas detectadas
			vector_mascara = []
			alturas = []
			i = 0
			while i < tam_vector - 1:
				# if i <= tam_vector - 1:		   #Si "i" tiene valor correspondiente al último elemento de la lista, no lo podemos emparejar con ninguno
				altura1 = alturas_ordenadas[i]
				altura2 = alturas_ordenadas[i+1]
				if altura2 - altura1 <= 500:		#Líneas separadas menos de 500 píxeles -> pareja de líneas
					vector_mascara.append([altura1, altura2])
					alturas.append(altura1)
					alturas.append(altura2)
					i = i + 2
					print('Líneas emparejadas')
					print(vector_mascara)
					print('')
				else:
					i = i + 1
					print('Línea desechada')
					print('')

			print('Vector máscara:', vector_mascara)
			print('Vector alturas:', alturas)
			# print(vector_mascara[0][0])
			# print(vector_mascara[0][1])		#Elementos de la primera pareja de líneas horizontales
			numero_de_parejas = len(vector_mascara)
			indice_parejas = 0

			#Creamos máscara para filtrar por alturas
			mascara = numpy.zeros((height, width),numpy.uint8)
			for h0, h1 in vector_mascara:
				lim_inferior = int(h0) 
				lim_superior = int(h1) 
				# print(lim_inferior, lim_superior)
				mascara[lim_inferior:lim_superior, :] = 1

			# print(mascara.max())

			target = cv2.bitwise_and(images[n],images[n], mask=mascara)

			if plot_hough == 1:
				plt.subplot(231),plt.imshow(images[n])
				plt.title('Original Image'), plt.xticks([]), plt.yticks([])

				plt.subplot(232),plt.imshow(edges,cmap = 'gray')
				plt.title('Edges detection'), plt.xticks([]), plt.yticks([])

				plt.subplot(233),plt.imshow(img_copy1)
				plt.title('Líneas detectadas '), plt.xticks([]), plt.yticks([])

				plt.subplot(234),plt.imshow(img_copy2)
				plt.title('Líneas definitivas'), plt.xticks([]), plt.yticks([])

				plt.subplot(235),plt.imshow(mascara, cmap = 'gray')
				plt.title('Líneas definitivas'), plt.xticks([]), plt.yticks([])

				plt.subplot(236),plt.imshow(target)
				plt.title('Bandas detectadas'), plt.xticks([]), plt.yticks([])
				plt.show()

		# Cálculo gradientes y conversión a valores enteros positivos
		target_gray = cv2.cvtColor(target, cv2.COLOR_RGB2GRAY)		

		grad_x = cv2.Sobel(target_gray, cv2.CV_16S, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
		abs_grad_x = cv2.convertScaleAbs(grad_x)

		grad_y = cv2.Sobel(target_gray, cv2.CV_16S, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
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
		
		# binaria1 = cv2.adaptiveThreshold(gradient2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,251,0)
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

		image_copy = images[n].copy()

		masked = cv2.bitwise_and(images[n], images[n], mask=closed)
		
		"""
		cv2.imshow('original', img)
		cv2.imshow('binaria', opened)
		cv2.imshow('Codigo aislado', masked)
		cv2.imshow('Contornos', image_copy)
		cv2.waitKey() 
		"""

		if plot_gradientes == 1:
			plt.subplot(231),plt.imshow(target_gray,cmap = 'gray')
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
		
	#############################################PROBAR cv2.ADAPTIVE_THRESH_GAUSSIAN_C#########################################################

if __name__ == "__main__":              
	funcion()






