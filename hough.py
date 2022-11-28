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
		images[n] = cv2.cvtColor(images[n], cv2.COLOR_BGR2RGB)

		gray = cv2.cvtColor(images[n], cv2.COLOR_RGB2GRAY)

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

		if lines is not None:
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

		# print('Vector alturas:',vector_alturas)
		# print('')

		# print(vector_alturas)
		# print('Longitud alturas:',len(vector_alturas))

		#Pinto las líneas definitivas
		if lines is not None:
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
		#print(tam_vector)

		#Ordenamos los vectores de menor rho a mayor y los ángulos acorde a cómo se han ordenado las distancias (rho)
		alturas_ordenadas, angulos_ordenados = zip(*sorted(zip(vector_alturas, vector_angulos)))
		print('Vector alturas ordenados:',alturas_ordenadas)
		print('Vector ángulos ordenados:',angulos_ordenados)
		print('')

		#Emparejamos las líneas detectadas
		vector_mascara = []
		alturas = []
		i = 0
		while i <= tam_vector - 1:
			#if i+1 <= tam_vector - 1:		   #Si "i" tiene valor correspondiente al último elemento de la lista, no lo podemos emparejar con ninguno
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
		#print(mascara)

		for h0, h1 in vector_mascara:
			lim_inferior = int(h0) 
			lim_superior = int(h1) 
			# print(lim_inferior, lim_superior)
			mascara[lim_inferior:lim_superior, :] = 1

		# print(mascara.max())

		target = cv2.bitwise_and(images[n],images[n], mask=mascara)

		#Transformada de Hough probabilística
		# linesP = cv2.HoughLinesP(edges,rho=1,theta=numpy.pi/180,threshold=300,minLineLength=100,maxLineGap=5)

		# #print(linesP)
		# #print(lines1)
		# #print(lines1[0][2][0])			#Campo 0: nada, campo 1: el par (rho, theta), campo 2: rho [0] y theta [1]

		# # Draw the lines
		# if linesP is not None:
		# 	#print('hola')
		# 	for i in range(0, len(linesP)):
		# 		l = linesP[i][0]
		# 		cv2.line(img_copy2, (l[0], l[1]), (l[2], l[3]), (255,0,0), 3, cv2.LINE_AA)

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

		#############################################PROBAR cv2.ADAPTIVE_THRESH_GAUSSIAN_C#########################################################

if __name__ == "__main__":
	funcion()