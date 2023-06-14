# coding=utf-8

import cv2
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join
import math
import numpy
from natsort import natsorted
import sys

bardet = cv2.barcode_BarcodeDetector()

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --- Número de bandas --- Líneas detectadas --- Proximidad para unir líneas --- Proximidad para pareja de líneas --- Separación con borde inferior de la banda de arriba --- Proximidad para eliminar banda ---
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --- 		2 		   --- 		 15 		 --- 			175 		   	 --- 		 450 - 350 - 200	      --- 		 Límite inferior + 4 * ancho máximo		      --- 				400				 ---
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --- 		3 		   --- 		 20 		 --- 			150 	  	  	 --- 	     400 - 300 - 150 	      --- 		 Límite inferior + 3 * ancho máximo		      ---				350				 ---
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --- 		4 		   --- 		 30 		 --- 			115  	  	  	 --- 		 275 - 175 - 25		      --- 		 Límite inferior + 3 * ancho máximo		      ---				275				 ---	
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --- 		5 		   --- 		 35 		 --- 			75  	  	  	 --- 	     150 				      --- 		 Límite inferior + 3 * ancho máximo		      ---								 ---
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Configuramos ciertas variables según el número de bandas que se deben identificar
def configuracion_numero_bandas(numero_bandas):
	print('----------------------------------------------------------- Configuración parámetros según número de bandas --------------------------------------------------------')
	if numero_bandas == 2:
		separacion = 175
		separacion3 = 450			#separacion2 + 100
		separacion2 = 350
		separacion_min = 200		#separacion2 - 150
		distancia_eliminar = 400

	elif numero_bandas == 3:
		separacion = 150
		separacion3 = 400			#separacion2 + 100
		separacion2 = 300
		separacion_min = 150		#separacion2 - 150
		distancia_eliminar = 350

	elif numero_bandas == 4:
		separacion = 115
		separacion3 = 275			#separacion2 + 100
		separacion2 = 175
		separacion_min = 25			#separacion2 - 150
		distancia_eliminar = 275

	print('Se configuran los parámetros para', numero_bandas, 'bandas')
	print('Separación para unir líneas:', separacion)
	print('Separación para formar pareja grande:', separacion3)
	print('Separación para formar pareja pequeña:', separacion2)
	print('Separación mínima para formar pareja:', separacion_min)
	print('Separación para eliminar parejas muy próximas:', distancia_eliminar)
	print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------')
	print('')

	return separacion, separacion3, separacion2, separacion_min, distancia_eliminar

#Función que calcula la transformada de Hough en busca de líneas horizontales (rho resolución 1 píxel, theta = 90º +- 2.5º)
def Hough(imagen, numero_lineas_detectadas):
	print('-------------------------------------------------------------------- Búsqueda de líneas horizontales --------------------------------------------------------------------')
	edges = cv2.Canny(imagen,125,225,apertureSize=3,L2gradient=True)
	#Búsqueda de líneas horizontales: en el rango [87.5º,92.5º] -> aumento el umbral (threshold) de 25 en 25 hasta quedarme con menos de 10 líneas detectadas
	lineas_detectadas = 2000
	umbral = 100
	while(lineas_detectadas>numero_lineas_detectadas):	
		lines = cv2.HoughLines(edges,rho=1,theta=numpy.pi/180,threshold=umbral,srn=0,stn=0,min_theta=numpy.pi/2-2.5*numpy.pi/180,max_theta=numpy.pi/2+2.5*numpy.pi/180)
		lineas_detectadas = len(lines)
		print('Líneas detectadas:',len(lines),'---','Umbral:', umbral)
		umbral += 25
	print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------')
	print('')

	return edges, lines

#Función para pintar las líneas detectadas y las definitivas seleccionadas
def pintar_lineas(imagen, height, width, lines, vector_alturas, vector_angulos):
	img_copy = imagen.copy()									
	if lines is not None:
		for i in range(len(lines)):
			rho = lines[i][0][0]
			theta = lines[i][0][1]
			a = math.cos(theta)
			b = math.sin(theta)
			x0 = a * rho				# x = rho * cos(theta)
			y0 = b * rho				# y = rho * sin(theta)
			pt1 = (int(x0 + math.sqrt(height**2+width**2)*(-b)), int(y0 + math.sqrt(height**2+width**2)*(a)))			#Tamaño imagen: 3000(alto) x 4000(ancho)
			pt2 = (int(x0 - math.sqrt(height**2+width**2)*(-b)), int(y0 - math.sqrt(height**2+width**2)*(a)))
			cv2.line(img_copy, pt1, pt2, (255,0,0), 10, cv2.LINE_AA)
		
		return img_copy

	else:
		for i in range(len(vector_alturas)):
			rho = vector_alturas[i]
			theta = vector_angulos[i]
			a = math.cos(theta)
			b = math.sin(theta)
			x0 = a * rho				# x = rho * cos(theta)
			y0 = b * rho				# y = rho * sin(theta)
			pt1 = (int(x0 + math.sqrt(height**2+width**2)*(-b)), int(y0 + math.sqrt(height**2+width**2)*(a)))			#Tamaño imagen: 3000(alto) x 4000(ancho)
			pt2 = (int(x0 - math.sqrt(height**2+width**2)*(-b)), int(y0 - math.sqrt(height**2+width**2)*(a)))
			cv2.line(img_copy, pt1, pt2, (255,0,0), 10, cv2.LINE_AA)
		
		return img_copy

#Función para agrupar los pares (rho, theta) que representan la misma horizontal
def seleccion_lineas_definitivas(vector_alturas_unidas, vector_angulos_unidos, separacion):
	vector_alturas = []
	vector_angulos = []
	primera_iter = 1
	distinto = 1

	print('-------------------------------------------------------------------- Selección de líneas definitivas --------------------------------------------------------------------')

	for i in range(len(vector_alturas_unidas)):
		print('rho:',vector_alturas_unidas[i])
		distinto = 1
		if primera_iter == 1:
			vector_alturas.append(vector_alturas_unidas[i])
			vector_angulos.append(vector_angulos_unidos[i])
			primera_iter = 0

		if primera_iter == 0:		
			for j in vector_alturas:
				print('Elemento vector:',j)
				if abs(vector_alturas_unidas[i] - j) < separacion:			#Líneas separadas menos de "separacion"" píxeles se considera que representan la misma horizontal
					print('Misma línea-------------------------------')
					print('Vector_alturas:',vector_alturas)
					print('Vector_angulos:',vector_angulos)
					print('')
					distinto = 0
					break

			if distinto == 1:										#Una vez comprobado que es distinto a todos los elementos ya existentes en "vector_alturas"
				vector_alturas.append(vector_alturas_unidas[i])		#lo añadimos
				vector_angulos.append(vector_angulos_unidos[i])
				print('Añadimos línea--------------------------------')
				print('Vector_alturas:',vector_alturas)
				print('Vector_angulos:',vector_angulos)
				print('')	
	print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------')
	
	return vector_alturas, vector_angulos

#Función que ordena los pares (rho, theta) definitivos de par con menor rho a par con mayor rho
def ordena_alturas(vector_alturas, vector_angulos):
	tam_vector = len(vector_alturas)
	print('Tamaño vector:',tam_vector)

	alturas_ordenadas, angulos_ordenados = zip(*sorted(zip(vector_alturas, vector_angulos)))
	print('Vector alturas ordenados:',alturas_ordenadas)
	print('Vector ángulos ordenados:',angulos_ordenados)
	print('')
	
	return tam_vector, alturas_ordenadas, angulos_ordenados

#Miramos si dos pares están cerca, si es así, los agrupamos formando una banda
def emparejamiento_lineas(tam_vector, alturas_ordenadas, height, numero_bandas, vector_aprendizaje, separacion3, separacion2, separacion_min):
	print('-------------------------------------------------------------------- Emparejamiento de líneas --------------------------------------------------------------------')
	vector_mascara = []			 #Vector de parejas de alturas
	alturas = []				 #Vector de alturas definitivas ordenadas
	vector_desechadas = []		 #Vector de líneas desechadas (las que no se emparejan y se quedan solas)
	indice_pareja = 0 			 #Para saber en qué índice de "vector_mascara" debo meter las líneas desechadas una vez las rellene
	vector_indices = []     	 #Vector que contiene los índices en los que se deben meter las líneas desechadas en "vector_mascara"
	vector_limites_inferiores = [] #Vector para guardar los límites inferiores de las parejas formadas
	i = 0									
	while i < tam_vector - 1:				#Ejemplo: 6 líneas -> i va [0, 4] < 6 - 1 = 5
		altura1 = alturas_ordenadas[i]		#Si "i" tiene valor correspondiente al último elemento de la lista, no lo podemos emparejar con ninguno,	
		altura2 = alturas_ordenadas[i+1]	#luego el máximo valor de "i" es el penúltimo elemento
		if i < tam_vector - 2:				#Ejemplo: 6 líneas -> i va [0, 3] < 6 - 2 = 4
			altura3 = alturas_ordenadas[i+2]
			print('Alturas:', altura1, '-', altura2, '-', altura3)
		else:
			print('Alturas:', altura1, '-', altura2)

		if altura3 - altura1 <= separacion3 and altura3 - altura1 >= separacion_min:	#Caso de 3 líneas muy juntas, nos quedamos con la dos más exteriores
			vector_mascara.append([altura1, altura3])
			alturas.append(altura1)						
			alturas.append(altura3)
			vector_limites_inferiores.append(altura3)
			i = i + 3
			print('Líneas emparejadas:', [altura1, altura3])
			print(vector_mascara)
			print('')
		elif altura2 - altura1 <= separacion2 and altura2 - altura1 >= separacion_min:		#Líneas separadas menos de "separacion2" píxeles -> pareja de líneas
			vector_mascara.append([altura1, altura2])
			alturas.append(altura1)						# "altura1" es la línea de arriba y "altura2" es la línea de abajo
			alturas.append(altura2)
			vector_limites_inferiores.append(altura2)
			i = i + 2
			print('Líneas emparejadas:', [altura1, altura2])
			print(vector_mascara)								#Incrementamos el índice de las líneas desechadas solo cuando formamos 
			print('')											#pareja, ya sea altura3-altura1 o altura2-altura1
		else:
			vector_desechadas.append(altura1)
			vector_indices.append(indice_pareja)
			i = i + 1
			print('Línea desechada:', altura1)
			print('Vector desechadas:', vector_desechadas)
			print('')	
		indice_pareja = indice_pareja + 1

	print('Valor de "i" al salir del bucle de emparejamiento:', i)
	print('')

	#Si i es el índice del último elemento del vector, no lo podemos emparejar con otra línea, luego añadimos esa línea al resto de líneas desechadas
	if i == tam_vector - 1:
		altura = alturas_ordenadas[i]
		vector_desechadas.append(altura)
		vector_indices.append(indice_pareja)
		print('Última línea se queda sola para emparejar -> se añade a las líneas desechadas')
		print('')
	
	numero_de_parejas = len(vector_mascara)	
	numero_lineas_desechadas = len(vector_desechadas)	

	separacion_teorica = int(height / numero_bandas)								
	vector_ocupacion = numpy.zeros(numero_bandas)	#Para saber qué posiciones están ocupadas (0 libre - 1 ocupado)

	for i in range(numero_de_parejas):		#Ubico cada pareja en "vector_ocupacion" para saber qué bandas son las que hay que crear artificialmente 		
		ubicado = 0
		indice_pareja = 1
		altura_de_abajo = vector_mascara[i][1]				#Límite inferior de las parejas ya formadas
			
		#Averiguo qué posición tiene cada pareja en el "vector_ocupacion"	
		while ubicado == 0:		
			factor = indice_pareja * separacion_teorica
			if altura_de_abajo <= factor:
				vector_ocupacion[indice_pareja - 1] = 1
				ubicado = 1
			indice_pareja = indice_pareja + 1	

	print('Vector máscara:', vector_mascara)
	print('Vector alturas:', alturas)
	print('Vector límites inferiores parejas:', vector_limites_inferiores)
	print('Número de parejas:', numero_de_parejas)
	print('Vector ocupación:', vector_ocupacion)

	print('Vector líneas desechadas:', vector_desechadas)
	print('Índices líneas desechadas:', vector_indices)
	print('Número de líneas desechadas:', numero_lineas_desechadas)
	print('')
	print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------')
	
	return vector_mascara, alturas, vector_limites_inferiores, vector_ocupacion, vector_desechadas, vector_indices, numero_de_parejas, numero_lineas_desechadas

#Obtengo el ancho (diferencia en la altura) de las bandas. Se calcula como altura del límite inferior - altura del límite superior
def ancho_bandas(numero_de_parejas, vector_mascara):
	print('-------------------------------------------------------------------- Cálculo ancho bandas --------------------------------------------------------------------')
	vector_anchos = []
	ancho = 0
	if numero_de_parejas != 0:
		for i in range(len(vector_mascara)):
			if vector_mascara[i][0] != 0 and vector_mascara[i][1] != 0:	#Para asegurarme que es una pareja cuyos dos valores ya han sido dados -> es decir no podría ser [1279,0]
				vector_anchos.append(int(vector_mascara[i][1] - vector_mascara[i][0]))			

		print('Vector anchos:', vector_anchos)
		ancho = max(vector_anchos)
		print('Ancho máximo:', ancho)	
		print('')		
	else:	#En caso de que no haya parejas formadas, se informa con un mensaje 
		print("No hay parejas formadas para obtener el ancho máximo")
		print('')
		print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------')

	return vector_anchos, ancho

#Función que recibe "vector_mascara" con las alturas de los límites de las bandas y crea una máscara que al aplicarla a la imagen, nos deja solo las bandas y el resto de la imagen a (0, 0, 0) que es el color negro
def creacion_mascara(height, width, vector_mascara, flag):
	mascara = numpy.zeros((height, width),numpy.uint8)
	for h0, h1 in vector_mascara:
		lim_inferior = int(h0) 
		lim_superior = int(h1) 
		#Caso para las parejas detectadas directamente a través de las línea de Hough
		if flag == 1:	#Límite superior - 20 píxeles y límite inferior + 20 píxeles para en caso de que las líneas detectadas no sean completamente horizontales, asegurarnos que en la banda entra todo el código de barras	
			mascara[lim_inferior - 20 : lim_superior + 20, :] = 1																													
		else:	#Para la creación de bandas artificiales
			mascara[lim_inferior : lim_superior, :] = 1
	
	return mascara

#Función que crea bandas artificiales cuando no hemos sido capaces de formar todas las parejas a partir de las líneas detectadas por Hough. Para ello utiliza la suposición de que las bandas son equidistantes
def bandas_artificiales(height, numero_bandas, vector_mascara, vector_ocupacion, numero_de_parejas, vector_limites_inferiores, primera_iter):
	print('-------------------------------------------------------------------- Relleno bandas artificiales --------------------------------------------------------------------')
	#Miro la altura de las bandas ya detectadas y sabiendo que son equidistantes creo artificialmente las que queden 
	#hasta llegar a "numero_de_parejas == numero_bandas -> hasta completar el vector de ocupación" 	
	i = 0				
	separacion = 0

	#En cuanto sea capaz de calcular la separación entre bandas, dejo de buscar ya que al suponer que son equisdistantes, el resto de resultados nos dará una valor de separación similar
	while(i < len(vector_ocupacion) - 1):		#Ejemplo: 4 bandas -> i va [0, 2] < 4 - 1 = 3
		#Miro si la banda que estoy mirando y la siguiente están ocupadas. En ese casos tenemos dos bandas consecutivas ocupadas
		if vector_ocupacion[i] == 1 and vector_ocupacion[i+1] == 1:											
			altura1_media = int((vector_mascara[i][0] + vector_mascara[i][1]) / 2)
			altura2_media = int((vector_mascara[i+1][0] + vector_mascara[i+1][1]) / 2)
			separacion = altura2_media - altura1_media
			break
		#Miro si la banda que estoy mirando y la que está dos posiciones más por delante están ocupadas. En ese casos obtendríamos 2 * (separación entre bandas) y se dividiría entre dos para obtener la separación entre bandas consecutivas
		elif i < len(vector_ocupacion) - 2 and vector_ocupacion[i] == 1 and vector_ocupacion[i+2] == 1:		#Banda ocupada, hueco, banda ocupada
			altura1_media = int((vector_mascara[i][0] + vector_mascara[i][1]) / 2)
			altura2_media = int((vector_mascara[i+2][0] + vector_mascara[i+2][1]) / 2)
			separacion = int((altura2_media - altura1_media) / 2)
			break
		#Miro si la banda que estoy mirando y la que está tres posiciones más por delante están ocupadas. En ese casos obtendríamos 3 * (separación entre bandas) y se dividiría entre tres para obtener la separación entre bandas consecutivas
		elif i < len(vector_ocupacion) - 3 and vector_ocupacion[i] == 1 and vector_ocupacion[i+3] == 1:		#Banda ocupada, hueco, banda ocupada
			altura1_media = int((vector_mascara[i][0] + vector_mascara[i][1]) / 2)
			altura2_media = int((vector_mascara[i+3][0] + vector_mascara[i+3][1]) / 2)
			separacion = int((altura2_media - altura1_media) / 3)
			break
		i = i + 1		

	#Separación teórica que se usa en caso de no haber podido calcular la separación entre bandas
	separacion_teorica = int(height / numero_bandas)		

	if separacion == 0:
		print('No hay dos bandas consecutivas para obtener la separación entre ellas -> se usa la separación teórica')	
		separacion = separacion_teorica		
		
	print('Vector máscara:', vector_mascara)
	print('Separación teórica:', separacion_teorica)
	print('Vector ocupación:', vector_ocupacion)
	print('Separación entre bandas:', separacion)
	print('')

	#Conociendo ya la separación, relleno las bandas que están vacías usando el ancho de las bandas calculado en la función "ancho_bandas()" y la separación entre ellas que lo acabamos de calcular			
	for i in range(len(vector_ocupacion)):	#Miro si la banda de arriba o de abajo de la vacía está ocupada para usarla como referencia
		print('Índice vector ocupación:', i)
		if vector_ocupacion[i] == 0: 
			if i > 0 and vector_ocupacion[i-1] == 1:
				print('i-1')
				print('Pareja usada:', [vector_mascara[i-1][0], vector_mascara[i-1][1]])
				vector_mascara.pop(i)
				vector_mascara.insert(i, [vector_mascara[i-1][0]+separacion-50, vector_mascara[i-1][1]+separacion+50])
				print('Añadida banda artificial:', [vector_mascara[i][0], vector_mascara[i][1]])
				if primera_iter == 1:
					vector_limites_inferiores = numpy.insert(vector_limites_inferiores, i, vector_mascara[i][1])
				else:
					vector_limites_inferiores[i] = vector_mascara[i][1]
				print('Añadido límite inferior:', vector_limites_inferiores)
				numero_de_parejas = numero_de_parejas + 1
				print('Vector máscara tras añadir banda artificial:', vector_mascara)
				vector_ocupacion[i] = 1
				print('Vector ocupación:', vector_ocupacion)

			elif i < len(vector_ocupacion) - 1 and vector_ocupacion[i+1] == 1:
				print('i+1')
				print('Pareja usada:', [vector_mascara[i+1][0], vector_mascara[i+1][1]])
				vector_mascara.pop(i)
				vector_mascara.insert(i, [vector_mascara[i][0]-separacion-50, vector_mascara[i][1]-separacion+50])
				print('Añadida banda artificial:', [vector_mascara[i][0], vector_mascara[i][1]])
				if primera_iter == 1:
					vector_limites_inferiores = numpy.insert(vector_limites_inferiores, i, vector_mascara[i][1])
				else:
					vector_limites_inferiores[i] = vector_mascara[i][1]
				print('Añadido límite inferior:', vector_limites_inferiores)
				numero_de_parejas = numero_de_parejas + 1
				print('Vector máscara tras añadir banda artificial:', vector_mascara)
				vector_ocupacion[i] = 1
				print('Vector ocupación:', vector_ocupacion)
			else:
				print('No se puede tomar ninguna banda de referencia')
		else:
			pass	
		print('')

	print('Vector límites inferiores parejas tras crear bandas artificiales:', vector_limites_inferiores)
	print('Vector máscara tras relleno artificial:', vector_mascara)
	print('Número de parejas tras bandas artificiales:', numero_de_parejas)
	print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------')
	print('')

	return vector_mascara, vector_limites_inferiores, numero_de_parejas, vector_ocupacion, separacion

#Si al formar parejas en la función "emparejamiento_lineas()", tenemos dos bandas muy próximas, eliminamos la banda inferior. En la memoria explicaremos por qué se ha decidido eliminar la banda que está más abajo de las dos
def eliminacion_bandas_productos(height, numero_bandas, vector_mascara, vector_ocupacion, numero_de_parejas, vector_limites_inferiores, distancia_eliminar):
	print('---------------------------------------------------------- Eliminación bandas en productos --------------------------------------------------------------------')
	print('Vector máscara:', vector_mascara)
	print('')
	valor_auxiliar = 0

	#Bandas a una separación inferior a "distancia_eliminar" píxeles, se elimina la banda de abajo
	for i in range(len(vector_mascara) - 1):	#Ejemplo: 4 bandas detectadas -> i va [0, 2] < 4 - 1 = 3
		print('Índice:',i,'---',vector_mascara[i-valor_auxiliar][1],'---',vector_mascara[i+1-valor_auxiliar][0])
		if abs(vector_mascara[i-valor_auxiliar][1]-vector_mascara[i+1-valor_auxiliar][0]) < distancia_eliminar:	#Parejas muy próximas -> eliminamos la de abajo
			print('Pareja eliminada:', vector_mascara[i+1])
			vector_mascara.pop(i+1)
			vector_limites_inferiores.pop(i+1)
			print('Vector máscara tras eliminar pareja en zona de productos:', vector_mascara)
			valor_auxiliar = valor_auxiliar + 1
			numero_de_parejas = numero_de_parejas - 1
		print('')

	#Recalculamos el "vector_ocupacion"
	separacion_teorica = int(height / numero_bandas)								
	print('Numero de parejas', numero_de_parejas)
	vector_ocupacion = numpy.zeros(numero_bandas)
	for i in range(numero_de_parejas):		#Ubico cada pareja en "vector_ocupacion" 
		ubicado = 0
		indice_pareja = 1
		altura_de_abajo = vector_mascara[i][1]				#Límite inferior de las parejas ya formadas		
			
		#Averiguo qué posición tiene cada pareja en el "vector_ocupacion"	
		while ubicado == 0:		
			factor = indice_pareja * separacion_teorica
			if altura_de_abajo <= factor:
				vector_ocupacion[indice_pareja - 1] = 1
				ubicado = 1
			indice_pareja = indice_pareja + 1

	print('Vector máscara:', vector_mascara)
	print('Vector ocupación:', vector_ocupacion)
	print('Número de parejas actuales:', numero_de_parejas)
	print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------')
	print('')

	return vector_mascara, vector_limites_inferiores, numero_de_parejas, vector_ocupacion

#Divide la imagen en tantas franjas horizontales como número de bandas a identificar. Además, le calcula la transformada de Hough a cada banda en busca de líneas horizontales
def Hough_franjas(numero_bandas, height, width, image, numero_lineas_a_detectar):
	edges, lines = Hough(image, 50)
	plot_franjas = 0
	plot_edges = 0

	if numero_bandas == 2:
		cuarto1 = numpy.zeros((height, width),numpy.uint8)			
		cuarto1[0 : int(height/2), :] = 1

		cuarto2 = numpy.zeros((height, width),numpy.uint8)			
		cuarto2[int(height/2) : height, :] = 1

		image1 = cv2.bitwise_and(image, image, mask=cuarto1)
		image2 = cv2.bitwise_and(image, image, mask=cuarto2)

		if plot_franjas == 1:
			plt.subplot(221),plt.imshow(image,cmap = 'gray')
			plt.title('Imagen original'), plt.xticks([]), plt.yticks([])

			plt.subplot(222),plt.imshow(image1,cmap = 'gray')
			plt.title('1ª franja'), plt.xticks([]), plt.yticks([])

			plt.subplot(223),plt.imshow(image2,cmap = 'gray')
			plt.title('2ª franja'), plt.xticks([]), plt.yticks([])	
			plt.show()

		edges1, lines1 = Hough(image1, numero_lineas_a_detectar)	
		img_copy11 = pintar_lineas(image, height, width, lines1, None, None)	#Para pintar todas las líneas detectadas en la franja 1

		edges2, lines2 = Hough(image2, numero_lineas_a_detectar)	
		img_copy12 = pintar_lineas(image, height, width, lines2, None, None)	#Para pintar todas las líneas detectadas en la franja 2

		#Hay que unir los 2 elementos "lineX"
		vector_alturas_unidas = []
		vector_angulos_unidos = []
		for i in lines1:
			vector_alturas_unidas.append(i[0][0])
			vector_angulos_unidos.append(i[0][1])
		for i in lines2:
			vector_alturas_unidas.append(i[0][0])
			vector_angulos_unidos.append(i[0][1])
		
		if plot_edges == 1:
			plt.subplot(221),plt.imshow(img_copy11)
			plt.title('Cuarto 1'), plt.xticks([]), plt.yticks([])

			plt.subplot(222),plt.imshow(img_copy12)
			plt.title('Cuarto 2'), plt.xticks([]), plt.yticks([])	
			plt.show()
	elif numero_bandas == 3:
		cuarto1 = numpy.zeros((height, width),numpy.uint8)			
		cuarto1[0 : int(height/3), :] = 1

		cuarto2 = numpy.zeros((height, width),numpy.uint8)			
		cuarto2[int(height/3) : int(2*height/3), :] = 1

		cuarto3 = numpy.zeros((height, width),numpy.uint8)			
		cuarto3[int(2*height/3) : height, :] = 1

		image1 = cv2.bitwise_and(image, image, mask=cuarto1)
		image2 = cv2.bitwise_and(image, image, mask=cuarto2)
		image3 = cv2.bitwise_and(image, image, mask=cuarto3)

		if plot_franjas == 1:
			plt.subplot(221),plt.imshow(image,cmap = 'gray')
			plt.title('Imagen original'), plt.xticks([]), plt.yticks([])

			plt.subplot(222),plt.imshow(image1,cmap = 'gray')
			plt.title('1ª franja'), plt.xticks([]), plt.yticks([])

			plt.subplot(223),plt.imshow(image2,cmap = 'gray')
			plt.title('2ª franja'), plt.xticks([]), plt.yticks([])	

			plt.subplot(224),plt.imshow(image3,cmap = 'gray')	
			plt.title('3ª franja'), plt.xticks([]), plt.yticks([])
			plt.show()

		edges1, lines1 = Hough(image1, numero_lineas_a_detectar)	
		img_copy11 = pintar_lineas(image, height, width, lines1, None, None)	#Para pintar todas las líneas detectadas en la franja 1

		edges2, lines2 = Hough(image2, numero_lineas_a_detectar)	
		img_copy12 = pintar_lineas(image, height, width, lines2, None, None)	#Para pintar todas las líneas detectadas en la franja 2
		
		edges3, lines3 = Hough(image3, numero_lineas_a_detectar)
		img_copy13 = pintar_lineas(image, height, width, lines3, None, None)	#Para pintar todas las líneas detectadas en la franja 3

		#Hay que unir los 3 elementos "lineX"
		vector_alturas_unidas = []
		vector_angulos_unidos = []
		for i in lines1:
			vector_alturas_unidas.append(i[0][0])
			vector_angulos_unidos.append(i[0][1])
		for i in lines2:
			vector_alturas_unidas.append(i[0][0])
			vector_angulos_unidos.append(i[0][1])
		for i in lines3:
			vector_alturas_unidas.append(i[0][0])
			vector_angulos_unidos.append(i[0][1])
		
		if plot_edges == 1:
			plt.subplot(221),plt.imshow(img_copy11)
			plt.title('Cuarto 1'), plt.xticks([]), plt.yticks([])

			plt.subplot(222),plt.imshow(img_copy12)
			plt.title('Cuarto 2'), plt.xticks([]), plt.yticks([])	

			plt.subplot(223),plt.imshow(img_copy13)	
			plt.title('Cuarto 3'), plt.xticks([]), plt.yticks([])
			plt.show()
	elif numero_bandas == 4:
		cuarto1 = numpy.zeros((height, width),numpy.uint8)			
		cuarto1[0 : int(height/4), :] = 1

		cuarto2 = numpy.zeros((height, width),numpy.uint8)			
		cuarto2[int(height/4) : int(height/2), :] = 1

		cuarto3 = numpy.zeros((height, width),numpy.uint8)			
		cuarto3[int(height/2) : int(3*height/4), :] = 1

		cuarto4 = numpy.zeros((height, width),numpy.uint8)			
		cuarto4[int(3*height/4) : height, :] = 1

		image1 = cv2.bitwise_and(image, image, mask=cuarto1)
		image2 = cv2.bitwise_and(image, image, mask=cuarto2)
		image3 = cv2.bitwise_and(image, image, mask=cuarto3)
		image4 = cv2.bitwise_and(image, image, mask=cuarto4)

		if plot_franjas == 1:
			plt.subplot(231),plt.imshow(image,cmap = 'gray')
			plt.title('Imagen original'), plt.xticks([]), plt.yticks([])

			plt.subplot(232),plt.imshow(image1,cmap = 'gray')
			plt.title('1ª franja'), plt.xticks([]), plt.yticks([])

			plt.subplot(233),plt.imshow(image2,cmap = 'gray')
			plt.title('2ª franja'), plt.xticks([]), plt.yticks([])	

			plt.subplot(234),plt.imshow(image3,cmap = 'gray')	
			plt.title('3ª franja'), plt.xticks([]), plt.yticks([])

			plt.subplot(235),plt.imshow(image4,cmap = 'gray')	
			plt.title('4ª franja'), plt.xticks([]), plt.yticks([])
			plt.show()

		edges1, lines1 = Hough(image1, numero_lineas_a_detectar)	
		img_copy11 = pintar_lineas(image, height, width, lines1, None, None)	#Para pintar todas las líneas detectadas en la franja 1

		edges2, lines2 = Hough(image2, numero_lineas_a_detectar)	
		img_copy12 = pintar_lineas(image, height, width, lines2, None, None)	#Para pintar todas las líneas detectadas en la franja 2
		
		edges3, lines3 = Hough(image3, numero_lineas_a_detectar)
		img_copy13 = pintar_lineas(image, height, width, lines3, None, None)	#Para pintar todas las líneas detectadas en la franja 3
			
		edges4, lines4 = Hough(image4, numero_lineas_a_detectar)	
		img_copy14 = pintar_lineas(image, height, width, lines4, None, None)	#Para pintar todas las líneas detectadas en la franja 4

		#Hay que unir los 4 elementos "lineX"
		vector_alturas_unidas = []
		vector_angulos_unidos = []
		for i in lines1:
			vector_alturas_unidas.append(i[0][0])
			vector_angulos_unidos.append(i[0][1])
		for i in lines2:
			vector_alturas_unidas.append(i[0][0])
			vector_angulos_unidos.append(i[0][1])
		for i in lines3:
			vector_alturas_unidas.append(i[0][0])
			vector_angulos_unidos.append(i[0][1])
		for i in lines4:
			vector_alturas_unidas.append(i[0][0])
			vector_angulos_unidos.append(i[0][1])
		
		if plot_edges == 1:
			plt.subplot(221),plt.imshow(img_copy11)
			plt.title('Cuarto 1'), plt.xticks([]), plt.yticks([])

			plt.subplot(222),plt.imshow(img_copy12)
			plt.title('Cuarto 2'), plt.xticks([]), plt.yticks([])	

			plt.subplot(223),plt.imshow(img_copy13)	
			plt.title('Cuarto 3'), plt.xticks([]), plt.yticks([])

			plt.subplot(224),plt.imshow(img_copy14)	
			plt.title('Cuarto 4'), plt.xticks([]), plt.yticks([])
			plt.show()

	return edges, vector_alturas_unidas, vector_angulos_unidos

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

	#Saco las dos líneas que delimitan la banda
	vector_alturas, vector_angulos = seleccion_lineas_definitivas(vector_alturas_unidas, vector_angulos_unidos, separacion = 300)

	#Ordenamos alturas para formar máscara
	tam_vector, alturas_ordenadas, angulos_ordenados = ordena_alturas(vector_alturas, vector_angulos)

	#Formamos "vector_mascara" y creamos la máscara
	vector_mascara = []

	#Filtramos las alturas según si están en la franja central de la imagen
	alturas_ordenadas = [x for x in alturas_ordenadas if x > 850 and x < 2150]

	print('Altura banda zoom:',alturas_ordenadas)
	print('')

	vector_mascara.append([alturas_ordenadas[0], alturas_ordenadas[1]])
	#Máscara que elimina todo menos la banda
	mascara = creacion_mascara(height, width, vector_mascara, flag = 1)	

	#Aplicamos la máscara
	target = cv2.bitwise_and(image,image, mask=mascara)	
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

#Función que realiza la fase de aprendizaje
def fase_aprendizaje(vector_mascara, vector_desechadas, vector_aprendizaje, numero_bandas):
	print('---------------------------------------------------------- Emparejamiento usando vector aprendizaje --------------------------------------------------------------------')
	numero_de_parejas = 0
	vector_mascara_def = []		
	for i in range(numero_bandas):
		vector_mascara_def.extend([[0,0]])
	vector_limites_inferiores_def = numpy.zeros(numero_bandas)

	vector_desechar_parejas = numpy.zeros(len(vector_mascara))

	print('Vector aprendizaje:', vector_aprendizaje)
	print('')

	#Bucle para recorrer el vector aprendizaje
	for i in range(len(vector_aprendizaje)):		
		print('Elemento vector aprendizaje:', vector_aprendizaje[i])
		#Bucle para recorrer el vector máscara. Así comparo cada pareja formada en "vector_mascara" con cada elemento del "vector_aprendizaje"
		for j in range(len(vector_mascara)):		
			print('Elemento vector máscara:', vector_mascara[j])
			#Si la pareja estudiada de "vector_mascara" está a la misma altura que la pareja que se está comprobando de "vector_aprendizaje", se añade a la máscara definitiva
			if abs(vector_mascara[j][0] - vector_aprendizaje[i][0]) < 100 and abs(vector_mascara[j][1] - vector_aprendizaje[i][1]) < 100 and vector_aprendizaje[i] != [0, 0]:	
				vector_mascara_def[i] = [vector_mascara[j][0], vector_mascara[j][1]]
				vector_limites_inferiores_def[i] = vector_mascara[j][1]
				print('Añadida pareja a vector mascara definitivo:', vector_mascara_def)	
				numero_de_parejas = numero_de_parejas  + 1
			else:	
				vector_desechar_parejas[j] = vector_desechar_parejas[j] + 1
		print('')

	#Hay que añadir las parejas que no pasan al vector máscara definitivo a las líneas desechadas para ver si alguna línea suelta, ya no como pareja, se puede añadir al vector máscara definitivo
	for i in range(len(vector_mascara)):
		if vector_desechar_parejas[i] == len(vector_aprendizaje):
			print('Añadida pareja', vector_mascara[i], 'a las líneas desechadas')
			vector_desechadas.append(vector_mascara[i][0])		
			vector_desechadas.append(vector_mascara[i][1])		#Añado la pareja formada a las líneas desechadas

	print('Vector máscara tras añadir parejas completas:', vector_mascara_def)
	print('Vector desechadas después de añadir parejas desechadas:', vector_desechadas)
	print('')

	#Bucle para recorrer el vector aprendizaje
	for i in range(len(vector_aprendizaje)):		
		print('Elemento vector aprendizaje:', vector_aprendizaje[i])
		#Bucle para recorrer el vector de líneas desechadas y ver si podemos añadir alguna en el vector máscara definitivo
		for j in range(len(vector_desechadas)):			
			print('Línea desechada:', vector_desechadas[j])
			#Añado un límite superior
			if abs(vector_aprendizaje[i][0] - vector_desechadas[j]) < 100 and vector_aprendizaje[i][0] != 0:
				vector_mascara_def[i][0] = vector_desechadas[j]
				print('Añadido límite superior a vector mascara definitivo:', vector_mascara_def)	
			#Añado un límite inferior
			elif abs(vector_aprendizaje[i][1] - vector_desechadas[j]) < 100 and vector_aprendizaje[i][1] != 0:
				vector_mascara_def[i][1] = vector_desechadas[j]
				vector_limites_inferiores_def[i] = vector_desechadas[j]
				print('Añadido límite inferior a vector mascara definitivo:', vector_mascara_def)	
		print('')

	print('Vector máscara definitivo:', vector_mascara_def)
	print('Vector límites inferiores:', vector_limites_inferiores_def)
	print('Número de parejas completas:', numero_de_parejas)

	return vector_mascara_def, vector_limites_inferiores_def, numero_de_parejas

#Función que completa las bandas del vector definitivo que se han quedado a medias, es decir, solo con el límite superior o solo con el límite inferior
def completar_bandas_aprendizaje(vector_mascara, vector_limites_inferiores, ancho, height, numero_bandas, numero_de_parejas):
	print('-------------------------------------------------------------------- Completar bandas a medias --------------------------------------------------------------------')
	print("Vector máscara:", vector_mascara)
	for i in range(len(vector_mascara)):
		#Tenemos el límite superior, pero no el inferior así que lo añadimos sabiendo el ancho de las bandas
		if vector_mascara[i][0] != 0 and vector_mascara[i][1] == 0:		
			vector_mascara[i][1] = vector_mascara[i][0] + ancho
			vector_limites_inferiores[i] = vector_mascara[i][1]
			print("Completado límite inferior:", [vector_mascara[i][0], vector_mascara[i][1]])
			print('Añadido límite inferior:', vector_mascara[i][1])
		#Tenemos el límite inferior, pero no el superior así que lo añadimos sabiendo el ancho de las bandas
		elif vector_mascara[i][0] == 0 and vector_mascara[i][1] != 0:	
			vector_mascara[i][0] = vector_mascara[i][1] - ancho
			print("Completado límite superior:", [vector_mascara[i][0], vector_mascara[i][1]])
	
	print("Vector máscara tras completar bandas:", vector_mascara)
	print('Vector límites inferiores tras completar bandas:', vector_limites_inferiores)

	separacion_teorica = int(height / numero_bandas)								
	vector_ocupacion = numpy.zeros(numero_bandas)	#Para saber qué posiciones están ocupadas (0 libre - 1 ocupado)
	
	for i in range(len(vector_ocupacion)):		#Ubico cada pareja en "vector_ocupacion"
		ubicado = 0
		indice_pareja = 1
		altura_de_abajo = vector_mascara[i][1]				#Límite inferior de las parejas ya formadas
			
		if vector_mascara[i][0] != 0 and vector_mascara[i][1] != 0:		#Por asegurarnos, se comprueba que es una pareja formada al completo
			#Averiguo qué posición tiene cada pareja en el "vector_ocupacion"
			while ubicado == 0:		
				factor = indice_pareja * separacion_teorica
				if altura_de_abajo <= factor:
					vector_ocupacion[indice_pareja - 1] = 1
					ubicado = 1
				indice_pareja = indice_pareja + 1

	print('Vector ocupación:', vector_ocupacion)

	numero_de_parejas = 0
	#Cuento el número de parejas formadas
	for i in range(len(vector_mascara)):
		if vector_mascara[i] != [0, 0]:
			numero_de_parejas = numero_de_parejas + 1	
	print('Número de parejas formadas tras aprendizaje:', numero_de_parejas)
	print('')
	
	return vector_mascara, vector_limites_inferiores, vector_ocupacion, numero_de_parejas

#################################################################################################################################################
#################################################################################################################################################
#################################################################################################################################################

#Función principal de la etapa 1
def funcion_principal():
	#Se lee el número de bandas y se configuran las variables necesarias
	numero_bandas = int(sys.argv[1])
	separacion, separacion3, separacion2, separacion_min, distancia_eliminar = configuracion_numero_bandas(numero_bandas)
	numero_lineas_a_detectar = 10

	vector_aprendizaje = []		
	for i in range(numero_bandas):
		vector_aprendizaje.extend([[0,0]])

	indice_lectura_codigos = 0
	primera_iter = 1

	#Directorio donde se encuentran las imágenes de las estanterías al completo
	mypath='E:\\Documents\\Juan de Dios\\TFG\\Fotos Mercadona\\Misma altura\\Secuencia1'
	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	onlyfiles = natsorted(onlyfiles)
	images = numpy.empty(len(onlyfiles), dtype=object)
	for n in range(0, len(onlyfiles)):
		images[n] = cv2.imread( join(mypath,onlyfiles[n]) ) 
		hsv = cv2.cvtColor(images[n], cv2.COLOR_BGR2HSV)
		images[n] = cv2.cvtColor(images[n], cv2.COLOR_BGR2RGB)

		height, width, channels = images[n].shape 
			
		#Busco las bandas horizontales por transformada de Hough en cada una de las franjas
		edges, vector_alturas_unidas, vector_angulos_unidos = Hough_franjas(numero_bandas, height, width, images[n], numero_lineas_a_detectar)

		#Si hemos detectado alguna línea
		if len(vector_alturas_unidas) != 0:
			#Para pintar todas las líneas detectadas por Hough
			img_copy1 = pintar_lineas(images[n], height, width, None, vector_alturas_unidas, vector_angulos_unidos)	

			#Miro la altura de las líneas y desecho las que representan la misma línea horizontal para quedarme solo con una
			vector_alturas, vector_angulos = seleccion_lineas_definitivas(vector_alturas_unidas, vector_angulos_unidos, separacion)

			#Pinto las líneas definitivas			
			img_copy2 = pintar_lineas(images[n], height, width, None, vector_alturas, vector_angulos)
		else:
			print('Ninguna línea detectada')

		plot_lineas = 0
		if plot_lineas == 1:
			plt.subplot(221),plt.imshow(images[n])
			plt.title('Original Image'), plt.xticks([]), plt.yticks([])

			plt.subplot(222),plt.imshow(edges,cmap = 'gray')
			plt.title('Edges detection'), plt.xticks([]), plt.yticks([])	

			plt.subplot(223),plt.imshow(img_copy1)	#Pinto todas las líneas detectadas
			plt.title('Líneas detectadas'), plt.xticks([]), plt.yticks([])

			plt.subplot(224),plt.imshow(img_copy2)	#Pinto las líneas definitivas
			plt.title('Líneas definitivas'), plt.xticks([]), plt.yticks([])
			plt.show()

		#Obtenemos el número de líneas a emparejar y ordenamos los vectores de menor rho a mayor y los ángulos acorde a cómo se han ordenado las distancias (rho)
		tam_vector, alturas_ordenadas, angulos_ordenados = ordena_alturas(vector_alturas, vector_angulos)

		#Emparejamos las líneas detectadas			
		vector_mascara, alturas, vector_limites_inferiores, vector_ocupacion, vector_desechadas, vector_indices, numero_de_parejas, numero_lineas_desechadas = emparejamiento_lineas(tam_vector, alturas_ordenadas, height, numero_bandas, vector_aprendizaje, separacion3, separacion2, separacion_min)
		
		#Miramos si alguna de las parejas formadas está muy próxima a otra, en ese caso, eliminamos la banda de abajo
		vector_mascara, vector_limites_inferiores, numero_de_parejas, vector_ocupacion = eliminacion_bandas_productos(height, numero_bandas, vector_mascara, vector_ocupacion, numero_de_parejas, vector_limites_inferiores, distancia_eliminar)

		#A partir de la segunda imagen, usamos el "vector_aprendizaje"
		if primera_iter == 0:
			vector_mascara, vector_limites_inferiores, numero_de_parejas = fase_aprendizaje(vector_mascara, vector_desechadas, vector_aprendizaje, numero_bandas)

		#Obtenemos el ancho de las bandas completas ya detectadas
		if primera_iter == 0:
			vector_anchos, ancho = ancho_bandas(numero_de_parejas, vector_mascara)
			#En caso de no existir ninguna banda completa, suponemos un ancho de banda por defecto
			if ancho == 0:
				ancho = 350

		#Arreglo praa resolver un problema de dimensiones
		if primera_iter == 1 and len(vector_mascara) != len(vector_ocupacion):
			for i in range(len(vector_ocupacion)):
				if vector_ocupacion[i] == 0:
					vector_mascara.insert(i, [0, 0])
					print('Añadido [0, 0] en la posición', i, 'del vector máscara')
		print('Vector máscara tras relleno con ceros:', vector_mascara)
		print('')

		#Completamos las bandas que tras la fase de aprendizaje están solo con uno de los bordes 
		if primera_iter == 0:
			vector_mascara, vector_limites_inferiores, vector_ocupacion, numero_de_parejas = completar_bandas_aprendizaje(vector_mascara, vector_limites_inferiores, ancho, height, numero_bandas, numero_de_parejas)
		
		#Creamos máscara para filtrar por alturas usando las parejas formadas
		mascara = creacion_mascara(height, width, vector_mascara, flag = 1)	

		#Resultado obtenido hasta ahora
		imagen_aprendizaje = cv2.bitwise_and(images[n],images[n], mask=mascara) 

		#En caso de que falten bandas por detectar, las creo artificialmente aplicando la suposición de que son equidistantes
		if numero_de_parejas < numero_bandas:
			vector_mascara, vector_limites_inferiores, numero_de_parejas, vector_ocupacion, separacion_bandas = bandas_artificiales(height, numero_bandas, vector_mascara, vector_ocupacion, numero_de_parejas, vector_limites_inferiores, primera_iter)

		primera_iter = 0

		#Copia del vector actual para comparar cuando eliminemos alguna pareja
		vector_mascara_copia = vector_mascara

		#Creamos la máscara con las bandas artificiales 
		mascara2 = creacion_mascara(height, width, vector_mascara, flag = 0)	

		#Resultado final
		resultado = cv2.bitwise_and(images[n],images[n], mask=mascara2)

		plot_aprendizaje = 1
		if plot_aprendizaje == 1:
			plt.subplot(321),plt.imshow(images[n])	#Imagen original
			plt.title('Original image'), plt.xticks([]), plt.yticks([])

			plt.subplot(322),plt.imshow(mascara, cmap = 'gray')	#Bandas formadas a partir de "vector_aprendizaje"
			plt.title('Learning phase'), plt.xticks([]), plt.yticks([])

			plt.subplot(323),plt.imshow(imagen_aprendizaje)	#Bandas obtenidas en fase de aprendizaje
			plt.title('Result 1'), plt.xticks([]), plt.yticks([])

			plt.subplot(324),plt.imshow(mascara2, cmap = 'gray')	#Bandas artificiales añadidas en caso de que sea necesario
			plt.title('Máscara con bandas artificiales'), plt.xticks([]), plt.yticks([])

			plt.subplot(325),plt.imshow(resultado)	#Resultado final obtenido con el algoritmo completo
			plt.title('Resultado final'), plt.xticks([]), plt.yticks([])
			plt.show()

		# plot_bandas = 1
		# if plot_bandas == 1:				
		# 	plt.subplot(331),plt.imshow(img_copy2)
		# 	plt.title('Líneas definitivas'), plt.xticks([]), plt.yticks([])

		# 	plt.subplot(332),plt.imshow(mascara, cmap = 'gray')	#Pinto la máscara con las parejas iniciales			
		# 	plt.title('Parejas iniciales'), plt.xticks([]), plt.yticks([])

		# 	plt.subplot(333),plt.imshow(mascara2, cmap = 'gray')	#Pinto la máscara con los rellenos y bandas artificiales		
		# 	plt.title('Rellenos y bandas artificiales'), plt.xticks([]), plt.yticks([])

		# 	plt.subplot(334),plt.imshow(target1)	#Resultado con rellenos y bandas artificiales
		# 	plt.title('Resultado con rellenos y bandas artificiales'), plt.xticks([]), plt.yticks([])

		# 	plt.subplot(335),plt.imshow(mascara3, cmap = 'gray')	#Pinto la máscara sin las parejas en la zona de productos y con las bandas definitivas		
		# 	plt.title('Parejas eliminadas'), plt.xticks([]), plt.yticks([])

		# 	plt.subplot(336),plt.imshow(mascara4, cmap = 'gray')	#Pinto la máscara sin las parejas en la zona de productos y con las bandas definitivas		
		# 	plt.title('Nuevo relleno y máscara definitiva'), plt.xticks([]), plt.yticks([])

		# 	plt.subplot(337),plt.imshow(target2)	#Resultado con las bandas definitivas
		# 	plt.title('Bandas detectadas'), plt.xticks([]), plt.yticks([])
		# 	plt.show()

		#Una vez creada la máscara definitiva, aplicamos la fase de aprendizaje
		#Leemos las imágenes del barrido con un bucle for y aplicamos "gradientes.py"
		print('----------------------------------------------------------------- Fase de aprendizaje --------------------------------------------------------------------')
		print('Vector aprendizaje actual:', vector_aprendizaje)
		print('')
		mypath2='E:\\Documents\\Juan de Dios\\TFG\\Fotos gasolinera\\Zoom'
		onlyfiles2 = [ f for f in listdir(mypath2) if isfile(join(mypath2,f)) ]
		onlyfiles2 = natsorted(onlyfiles2)
		# print(onlyfiles2)
		images2 = numpy.empty(len(onlyfiles2), dtype=object)


		#METER LAS DIRECCIONES DE LOS ZOOMS EN UN VECTOR Y ASÍ IR RECORRIÉNDOLO
		#Secuencia 1
		vector_imagen1 = [True, False, True]	#Valores de la imagen 1 para la identificación de códigos de barras (False: detecta - True: no detecta)
		vector_imagen2 = [True, True, False]
		vector_imagen3 = [True, True, True]		#True: lee código - False: no lee código	

		# #Secuencia 2
		# vector_imagen1 = [True, True, True]	#Valores de la imagen 1 para la identificación de códigos de barras (False: detecta - True: no detecta)
		# vector_imagen2 = [False, True, False]
		# vector_imagen3 = [True, True, False]		#True: lee código - False: no lee código

		# #Secuencia 3
		# vector_imagen1 = [True, False]	#Valores de la imagen 1 para la identificación de códigos de barras (False: detecta - True: no detecta)
		# vector_imagen2 = [False, False]
		# vector_imagen3 = [False, False]		#True: lee código - False: no lee código

		#Secuencia 4
		# vector_imagen1 = [False, True, True]	#Valores de la imagen 1 para la identificación de códigos de barras (False: detecta - True: no detecta)
		# vector_imagen2 = [True, True, True]
		# vector_imagen3 = [True, True, False]		#True: lee código - False: no lee código

		vector_imagenes = [vector_imagen1, vector_imagen2, vector_imagen3]

		for m in range(0, len(vector_imagenes[indice_lectura_codigos])):
			# print(vector_imagenes[indice_lectura_codigos][m])
			if vector_imagenes[indice_lectura_codigos][m] == True: 	#Significa que no todo es '0' y que por tanto hemos identificado códigos de barras
				print('Código/s de barras identificado/s en imagen', m, '-> se almacena la altura de la banda', m, ':', [vector_mascara[m][0], vector_mascara[m][1]])
				if (vector_aprendizaje[0][1] == 0 and m  == 0) or (vector_aprendizaje[1][1] == 0 and m  == 1) or (vector_aprendizaje[2][1] == 0 and m  == 2):
					vector_aprendizaje[m] = [vector_mascara[m][0], vector_mascara[m][1]]	#Primera vez que se le da valor a una de las posiciones del vector de aprendizaje

				if vector_aprendizaje[m][0] < vector_mascara[m][0]:	#Si hemos conseguido leer código de una banda con el límite superior
					vector_aprendizaje[m][0] = vector_mascara[m][0]		#más hacia abajo, es porque la banda la podemos estrechar más y seguir leyendo

				if vector_aprendizaje[m][1] > vector_mascara[m][1]:	#Si hemos conseguido leer código de una banda con el límite inferior
					vector_aprendizaje[m][1] = vector_mascara[m][1]		#más hacia arriba, es porque la banda la podemos estrechar más y seguir leyendo

			else:
				print('Código/s de barras NO identificado/s en imagen', m, '-> no se almacena la altura de la banda', m, ':', [vector_mascara[m][0], vector_mascara[m][1]])
			# Si añadiésemos la altura del algoritmo de "gradientes.py" estarían todas entre 850 y 2250, luego esa no es la altura que se debe añadir

			print('Vector aprendizaje modificado:', vector_aprendizaje)
			print('')
		
		indice_lectura_codigos = indice_lectura_codigos + 1
		"""
		for i in range(len(vector_mascara)):
			if banda_correcta[i] == True: 	#Significa que no todo es '0' en dilated y que por tanto hemos identificado códigos de barras
				#Primera vez que se le da valor a una de las posiciones del vector de aprendizaje
				if (vector_aprendizaje[0][1] == 0 and i  == 0) or (vector_aprendizaje[1][1] == 0 and i  == 1) or (vector_aprendizaje[2][1] == 0 and i  == 2):
					vector_aprendizaje[i] = [vector_mascara[i][0], vector_mascara[i][1]]	
				#Si hemos conseguido leer código de una banda con el límite superior más hacia abajo, es porque la banda la podemos estrechar más y seguir leyendo
				if vector_aprendizaje[i][0] < vector_mascara[i][0]:	
					vector_aprendizaje[i][0] = vector_mascara[i][0]		
				#Si hemos conseguido leer código de una banda con el límite inferior más hacia arriba, es porque la banda la podemos estrechar más y seguir leyendo
				if vector_aprendizaje[i][1] > vector_mascara[i][1]:	
					vector_aprendizaje[i][1] = vector_mascara[i][1]		
		"""
		"""
		for m in range(0, len(onlyfiles2)):
			images2[m] = cv2.imread( join(mypath2,onlyfiles2[m]) ) 
			images2[m] = cv2.cvtColor(images2[m], cv2.COLOR_BGR2RGB)

			# plt.subplot(111),plt.imshow(images2[m])	#Pinto las líneas definitivas
			# plt.title('Foto'), plt.xticks([]), plt.yticks([])
			# plt.show()	

			target, target_gray, blurred, binaria, closed, opened, masked = calcula_banda(images2[n], height, width)

			print('Vector máscara:', vector_mascara)
			all_zeros = not numpy.any(opened) #Para ver si todos los elementos de la matriz son 0 (es decir, no se han identificado códigos de barras)
			if all_zeros == False: 	#Significa que no todo es '0' y que por tanto hemos identificado códigos de barras
				print('Código/s de barras identificado/s en imagen', m, '-> se almacena la altura de la banda', m, ':', [vector_mascara[m][0], vector_mascara[m][1]])
				vector_aprendizaje[m] = [vector_mascara[m][0], vector_mascara[m][1]]	#Añadimos la altura al vector definitivo. Cada valor del
																						#índice "k" corresponderá a una banda (k=0 -> banda de más arriba, k=1 -> segunda banda, etc)
			# Si añadiésemos la altura del algoritmo de "gradientes.py" estarían todas entre 850 y 2250, luego esa no es la altura que se debe añadir

			print('Vector aprendizaje:', vector_aprendizaje)

############################################################################################################################################
			# Se buscan los contornos de los códigos de barras (rectángulos) y se pintan
			opened_copy = opened.copy()
			contours, hierarchy = cv2.findContours(opened_copy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

			image_copy = images[n].copy()

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
				plt.subplot(231),plt.imshow(images2[n])
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
############################################################################################################################################
			
		print('-------------------------------------------------------------------- Fin fase de aprendizaje --------------------------------------------------------------------')

		"""
		
	#Guardar imagen 
	# filename = 'savedImage.jpg'
	# target2 = cv2.cvtColor(target2, cv2.COLOR_RGB2BGR)
	# cv2.imwrite(filename, target2)
	# target2 = cv2.cvtColor(target2, cv2.COLOR_BGR2RGB)

		

if __name__ == "__main__":              
	funcion_principal()






