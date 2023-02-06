# coding=utf-8

import cv2
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join
import math
import numpy

def configuracion_numero_bandas():
	pass	

def Hough(imagen, numero_lineas_detectadas):
	print('-------------------------------------------------------------------- Búsqueda de líneas horizontales --------------------------------------------------------------------')
	edges = cv2.Canny(imagen,125,225,apertureSize=3,L2gradient=True)
	#print(edges)
	#Búsqueda de líneas horizontales: en el rango [85º,95º] -> aumento umbral de 100 en 100 hasta quedarme con 15 líneas detectadas o menos
	lineas_detectadas = 2000
	umbral = 100
	while(lineas_detectadas>numero_lineas_detectadas):	#Para gasolinera
	# while(lineas_detectadas>25):	#Para Mercadona
		lines = cv2.HoughLines(edges,rho=1,theta=numpy.pi/180,threshold=umbral,srn=0,stn=0,min_theta=numpy.pi/2-0.5*numpy.pi/180,max_theta=numpy.pi/2+0.5*numpy.pi/180)
		# print(lines)
		lineas_detectadas = len(lines)
		print('Líneas detectadas:',len(lines),'---','Umbral:', umbral)
		umbral += 25
	print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------')
	#print(lines)
	print('')

	return edges, lines

def pintar_lineas(imagen, height, width, lines, vector_alturas, vector_angulos):
	img_copy = imagen.copy()									
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
			cv2.line(img_copy, pt1, pt2, (255,0,0), 10, cv2.LINE_AA)
		return img_copy

	else:
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
			cv2.line(img_copy, pt1, pt2, (255,0,0), 10, cv2.LINE_AA)
		return img_copy

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

		if primera_iter == 0:		#else:
			for j in vector_alturas:
				print('Elemento vector:',j)
				if abs(vector_alturas_unidas[i] - j) < separacion:			#Líneas separadas menos de 150 píxeles se considera que representan la misma horizontal
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

def ordena_alturas(vector_alturas, vector_angulos):
	tam_vector = len(vector_alturas)
	print('Tamaño vector:',tam_vector)

	alturas_ordenadas, angulos_ordenados = zip(*sorted(zip(vector_alturas, vector_angulos)))
	print('Vector alturas ordenados:',alturas_ordenadas)
	print('Vector ángulos ordenados:',angulos_ordenados)
	print('')
	return tam_vector, alturas_ordenadas, angulos_ordenados

def emparejamiento_lineas(tam_vector, alturas_ordenadas):
	print('-------------------------------------------------------------------- Emparejamiento de líneas --------------------------------------------------------------------')
	vector_mascara = []			 #Vector de parejas de alturas
	alturas = []				 #Vector de alturas definitivas ordenadas
	vector_desechadas = []		 #Vector de líneas desechadas (las que no se emparejan y se quedan solas)
	indice_pareja = 0 			 #Para saber en qué índice de "vector_mascara" debo meter las líneas desechadas una vez las rellene
	vector_indices = []     	 #Vector que contiene los índice en los que se deben meter las líneas desechadas en "vector_mascara"
	vector_limites_inferiores = [] #Vector para guardar los límites inferiores de las parejas formadas
	i = 0
	while i < tam_vector - 1:		#Si "i" tiene valor correspondiente al último elemento de la lista, no lo podemos emparejar con ninguno,
		altura1 = alturas_ordenadas[i]		#luego el máximo valor de "i" es el penúltimo elemento
		altura2 = alturas_ordenadas[i+1]
		if altura2 - altura1 <= 175:		#Líneas separadas menos de 350 píxeles -> pareja de líneas
			vector_mascara.append([altura1, altura2])
			alturas.append(altura1)
			alturas.append(altura2)
			vector_limites_inferiores.append(altura2)
			# indice_pareja = indice_pareja + 1
			i = i + 2
			print('Líneas emparejadas')
			print(vector_mascara)
			print('')
		else:
			vector_desechadas.append(altura1)
			vector_indices.append(indice_pareja)
			# indice_pareja = indice_pareja + 1
			i = i + 1
			print('Línea desechada')
			print('Vector desechadas:', vector_desechadas)
			print('')	
		indice_pareja = indice_pareja + 1

	print('Valor de "i" al salir del bucle de emparejamiento:', i)
	print('')

	if i == tam_vector - 1:
		altura = alturas_ordenadas[i]
		vector_desechadas.append(altura)
		vector_indices.append(indice_pareja)
		print('Última línea se queda sola para emparejar -> se añade a las líneas desechadas')
		print('')

	# print(vector_mascara[0][0])
	# print(vector_mascara[0][1])		#Elementos de la primera pareja de líneas horizontales
	print('Vector máscara:', vector_mascara)
	print('Vector alturas:', alturas)
	print('Vector límites inferiores parejas:', vector_limites_inferiores)
	numero_de_parejas = len(vector_mascara)
	print('Número de parejas:', numero_de_parejas)

	print('Vector líneas desechadas:', vector_desechadas)
	print('Índices líneas desechadas:', vector_indices)
	numero_lineas_desechadas = len(vector_desechadas)
	print('Número de líneas desechadas:', numero_lineas_desechadas)
	print('')

	print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------')
	return vector_mascara, alturas, vector_limites_inferiores, vector_desechadas, vector_indices, numero_de_parejas, numero_lineas_desechadas

def ancho_bandas(numero_de_parejas, vector_mascara):
	vector_anchos = []
	if numero_de_parejas != 0:
		for i in range(numero_de_parejas):
			# print(i)
			vector_anchos.append(int(vector_mascara[i][1]-vector_mascara[i][0]))
		print('Vector anchos:', vector_anchos)
		ancho = max(vector_anchos)
		print('Ancho máximo:', ancho)	
		print('')
	else:
		print("No hay parejas formadas para obtener el ancho máximo")
		print('')
	return vector_anchos, ancho

def creacion_mascara(height, width, vector_mascara, flag):
	mascara = numpy.zeros((height, width),numpy.uint8)
	for h0, h1 in vector_mascara:
		lim_inferior = int(h0) 
		lim_superior = int(h1) 
		# print(lim_inferior, lim_superior)
		#Caso para las parejas detectadas directamente a través de las línea de Hough
		if flag == 1:	#Límite superior - 20 píxeles y límite inferior + 20 píxeles para en caso de que las líneas detectadas no sean completamente 
			mascara[lim_inferior - 20 : lim_superior + 20, :] = 1	#horizontales, asegurarnos que en la banda entra todo el código de barras																													
		else:	#Para el relleno de líneas sueltas y la creación de bandas artificiales
			mascara[lim_inferior : lim_superior, :] = 1
	return mascara

def relleno_lineas_sueltas(height, numero_bandas, vector_mascara, numero_de_parejas, vector_limites_inferiores, vector_desechadas, numero_lineas_desechadas, vector_indices, ancho):
	#Saco ancho máximo de las bandas ya detectadas
	#Compruebo si con la altura (componente "y") que tiene en la imagen puede ser una línea de banda 
	#Si es, relleno hacia un lado y hacia el otro y hago una AND con el filtro de color (con las bandas horizontales completas). Luego comparo 
	#y me quedo con la que tenga más píxeles en blanco que será la que rellene hacia el lado correcto, decremento "numero_lineas_desechadas" e incremento "numero_de_parejas"
	separacion_teorica = int(height / numero_bandas)	

	print('-------------------------------------------------------------------- Relleno de líneas sueltas --------------------------------------------------------------------')

	for i in range(len(vector_desechadas)):
		# print(i)
		print('Línea desechada:', vector_desechadas[i])
		print('Vector límites inferiores:', vector_limites_inferiores)
		#Las líneas detectadas en los productos suelen estar justo debajo de una banda horizontal que es cuando acaba 
		#la parte de arriba de las cajas/tetrabrick. Si se detecta el final de las cajas/tetrabrick por debajo, da igual porque nos sirve
		#para detectar el límite superior de la banda que está debajo de la caja/tetrabrick. Para ello debo mirar que la banda de arriba
		#de la línea desechada que queremos rellenar ya está detectada		
		#Miro que el índice anterior no esté en el vector de índices y por lo tanto, ya es una pareja formada. También miro que desde el límite inferior de la banda de arriba a la línea haya poca distancia (se ha establecido una distancia de 3 veces el ancho máximo)			
		
		# indice_banda_anterior = vector_indices[i] - 1
		# altura_lim_inferior_banda_anterior = vector_mascara[indice_banda_anterior][1]

		aux1 = vector_limites_inferiores
		aux2 = [x - vector_desechadas[i] for x in aux1]	#Resto el valor de la línea desechada a cada elemento del vector de límites inferiores de las parejas ya formadas
		print('Limites inferiores restados:', aux2)		#El elemento negativo de "aux" más grande (más cerca del 0), será el elemento que buscamos

		# Obtenemos el valor del límite inferior de la pareja más cercana por arriba
		minimo = aux2[0]
		indice = 0
		for j in range(len(aux2)):
			# print(i)
			if aux2[j] < 0 and aux2[j] > minimo:
				minimo = aux2[j]
				indice = j

		# print(type(minimo))
		# print(type(i))

		print('Límite inferior de la banda de arriba:', aux1[indice])

		# print(vector_desechadas[i])
		# print(aux1[indice] + 4 * ancho)
		# print(vector_indices[i])

############### POR AHORA SE RELLENA HACIA AMBOS LADOS, HABRÁ QUE SABER DE ALGUNA MANERA QUÉ LADO ES EL CORRECTO #####################################
############### TAMBIÉN MIRAR POR SI PUEDE SER UNA LÍNEA QUE ESTÁ EN LOS PRODUCTOS Y QUE POR LO TANTO NO SIRVE #######################################

		if (vector_desechadas[i] > aux1[indice] + 2 * ancho or vector_indices[i] == 0) and numero_de_parejas < numero_bandas: 	
			
			vector_mascara.insert(vector_indices[i], [vector_desechadas[i] - ancho, vector_desechadas[i] + ancho])
			vector_limites_inferiores.insert(vector_indices[i], vector_desechadas[i] + ancho)
			numero_de_parejas = numero_de_parejas + 1
			print('Línea rellenada hacia ambos lados:', [vector_desechadas[i] - ancho, vector_desechadas[i] + ancho])
			print('Vector máscara tras añadir la línea:', vector_mascara)
			print('Vector límites inferiores tras añadir la línea:', vector_limites_inferiores)
		else:
			print('Línea eliminada definitivamente')
		
		numero_lineas_desechadas = numero_lineas_desechadas - 1
		print('Líneas desechadas restantes:', numero_lineas_desechadas)
		# vector_desechadas.remove(vector_desechadas[i])
		# vector_indices.remove(vector_indices[i])	#Eliminamos el índice de la línea desechada en cuestión	
		# print(vector_desechadas)
		# print(vector_indices)
		print('')

	print('Vector límites inferiores parejas tras rellenar líneas desechadas:', vector_limites_inferiores)
	print('Vector máscara tras añadir líneas desechadas:', vector_mascara)
	print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------')
	print('')
	return vector_mascara, vector_limites_inferiores, numero_de_parejas, numero_lineas_desechadas

def bandas_artificiales(height, numero_bandas, vector_mascara, numero_de_parejas, vector_limites_inferiores, numero_lineas_desechadas):
	print('-------------------------------------------------------------------- Relleno bandas artificiales --------------------------------------------------------------------')
	#Miro la altura de las bandas ya detectadas y sabiendo que son equidistantes creo artificialmente las que queden 
	#hasta llegar a "numero_de_parejas == numero_bandas -> hasta completar el vector de ocupación" 
	separacion_teorica = int(height / numero_bandas)								
	vector_ocupacion = numpy.zeros(numero_bandas)	#Para saber qué posiciones están ocupadas (0 libre - 1 ocupado)

	for i in range(numero_de_parejas):		#Igual que range(len(vector_mascara))	Ubico cada pareja en "vector_ocupacion"
		# print(i)							#para saber qué bandas son las que hay que crear artificialmente 
		ubicado = 0
		indice_pareja = 1
		altura_de_abajo = vector_mascara[i][1]				#Límite inferior de las parejas ya formadas
		# if altura_de_arriba - separacion <= 0:			#Compruebo si es la banda de más arriba
		# 	vector_ocupacion[0] = 1
		# elif altura_de_arriba + separacion >= height:		#Compruebo si es la banda de más abajo
		# 	vector_ocupacion[-1] = 1
		# else:
			
		while ubicado == 0:		#Averiguo qué posición tiene cada pareja en el "vector_ocupacion"
			factor = indice_pareja * separacion_teorica
			if altura_de_abajo <= factor:
				vector_ocupacion[indice_pareja - 1] = 1
				ubicado = 1
			indice_pareja = indice_pareja + 1
	
	#Saco la separación que hay entre dos bandas consecutivas
	i = 0				
	vector_separaciones = []

################### MIRAR CÓMO ARREGLAR CUANDO "VECTOR_MASCARA" TIENE MENOR LONGITUD QUE "VECTOR_OCUPACION" (LÍNEA "ALTURA2_MEDIA"") ########################################

	while(i < len(vector_ocupacion) - 1):		#Ejemplo: 4 bandas -> i va [0, 2] < 4 - 1 = 3
		# if vector_ocupacion[i] == 1 and vector_ocupacion[i-1] == 1 and i > 0:
		# 	altura1_media = int((vector_mascara[i-1][0] + vector_mascara[i-1][1]) / 2)
		# 	altura2_media = int((vector_mascara[i][0] + vector_mascara[i][1]) / 2)
		# 	vector_separaciones.append(altura2_media - altura1_media)
		# 	i = i + 2
		if vector_ocupacion[i] == 1 and vector_ocupacion[i+1] == 1:
			altura1_media = int((vector_mascara[i][0] + vector_mascara[i][1]) / 2)
			altura2_media = int((vector_mascara[i+1][0] + vector_mascara[i+1][1]) / 2)
			vector_separaciones.append(altura2_media - altura1_media)	
			# i = i + 1	
		else:
			pass
		i = i + 1		

	if len(vector_separaciones) == 0:
		print('No hay dos bandas consecutivas para obtener la separación entre ellas')	
		
######################################## MIRAR EL CASO EN QUE NO HAY BANDAS CONSECUTIVAS (EL ELSE) ###############################################

	print('Vector máscara:', vector_mascara)
	print('Separación teórica:', separacion_teorica)
	print('Vector ocupación:', vector_ocupacion)
	print('')

	print('Vector separaciones:', vector_separaciones)
	separacion = int(sum(vector_separaciones)/len(vector_separaciones))
	print('Separación media entre bandas:', separacion)
	print('')
						
	for i in range(len(vector_ocupacion)):	#Miro si la banda de arriba o de abajo de la vacía está ocupada para usarla como referencia
		print('Índice vector ocupación:', i)
		if vector_ocupacion[i] == 0: 
			if vector_ocupacion[i-1] == 1 and i > 0 and numero_de_parejas < numero_bandas:
				# print('i-1')
				print('Pareja usada:', [vector_mascara[i-1][0], vector_mascara[i-1][1]])
				vector_mascara.insert(i, [vector_mascara[i-1][0]+separacion-20, vector_mascara[i-1][1]+separacion+20])
				print('Añadida banda artificial:', [vector_mascara[i][0], vector_mascara[i][1]])
				vector_limites_inferiores.insert(i, vector_mascara[i][1])
				print('Añadido límite inferior:', vector_limites_inferiores)
				numero_de_parejas = numero_de_parejas + 1
				print('Vector máscara tras añadir banda artificial:', vector_mascara)
				vector_ocupacion[i] = 1
				print('Vector ocupación:', vector_ocupacion)

			elif vector_ocupacion[i+1] == 1 and i < len(vector_ocupacion) - 1 and numero_de_parejas < numero_bandas:
				# print('i+1')
				print('Pareja usada:', [vector_mascara[i+1][0], vector_mascara[i+1][1]])
				vector_mascara.insert(i, [vector_mascara[i+1][0]-separacion-20, vector_mascara[i+1][1]-separacion+20])
				print('Añadida banda artificial:', [vector_mascara[i][0], vector_mascara[i][1]])
				vector_limites_inferiores.insert(i, vector_mascara[i][1])
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
######################################## MIRAR EL CASO EN QUE NO HAY BANDA OCUPADA NI POR ARRIBA NI POR ABAJO DE LA VACÍA (EL ELSE) ###############################################
	print('Vector límites inferiores parejas tras crear bandas artificiales:', vector_limites_inferiores)
	print('Vector máscara tras relleno artificial:', vector_mascara)
	print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------')
	print('')

	# for i in range(numero_bandas):
	# 	pass
	return vector_mascara, vector_limites_inferiores, numero_de_parejas, vector_ocupacion, separacion

def eliminacion_bandas_productos(numero_bandas, vector_mascara, numero_de_parejas, vector_limites_inferiores):
	print('---------------------------------------------------------- Eliminación bandas en productos --------------------------------------------------------------------')
	valor_auxiliar = 0
	for i in range(numero_bandas - 1):	#Ejemplo: 4 bandas -> i va [0, 2] < 4 - 1 = 3
		print('Índice:',i,'---',vector_mascara[i-valor_auxiliar][1],'---',vector_mascara[i+1-valor_auxiliar][0])
		if abs(vector_mascara[i-valor_auxiliar][1]-vector_mascara[i+1-valor_auxiliar][0]) < 275:	#Parejas muy próximas -> eliminamos la de abajo
			print('Pareja eliminada:', vector_mascara[i+1])
			vector_mascara.pop(i+1)
			vector_limites_inferiores.pop(i+1)
			print('Vector máscara tras eliminar pareja en zona de productos:', vector_mascara)
			valor_auxiliar = valor_auxiliar + 1
			numero_de_parejas = numero_de_parejas - 1
		print('')
	print('Número de parejas actuales:', numero_de_parejas)
	print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------')
	print('')
	return vector_mascara, vector_limites_inferiores, numero_de_parejas

def funcion():
	#mypath='C:\\Users\\joseh\\Documents\\Juan de Dios\\TFG\\Fotos'
	#mypath='E:\\Documents\\Juan de Dios\\TFG\\Fotos folio'
	# mypath='E:\\Documents\\Juan de Dios\\TFG\\Fotos gasolinera'
	#mypath='E:\\Documents\\Juan de Dios\\TFG\\Fotos productos'
	mypath='E:\\Documents\\Juan de Dios\\TFG\\Fotos Mercadona\\4B'
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

		numero_bandas = 4
		numero_lineas_a_detectar = 10

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --- Número de bandas --- Líneas detectadas --- Proximidad para unir líneas --- Proximidad para pareja de líneas --- Separación con borde inferior de la banda de arriba ---
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --- 		2 		   --- 		 15 		 --- 			150 		   	 --- 			  350 			      --- 		 Límite inferior + 4 * ancho máximo		      ---
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --- 		3 		   --- 		 20 		 --- 			150 	  	  	 --- 			  250 			      --- 		 Límite inferior + 3 * ancho máximo		      ---
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --- 		4 		   --- 		 30 		 --- 			115  	  	  	 --- 			  150 			      --- 		 Límite inferior + 3 * ancho máximo		      ---
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --- 		5 		   --- 		 35 		 --- 			75  	  	  	 --- 			  150 			      --- 		 Límite inferior + 3 * ancho máximo		      ---
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

		#Busco las bandas horizontales por su color
		if filtro_color == 1:
			# Aislamos por el color las bandas horizontales
			# mask1 = cv2.inRange(hsv, (30, 50, 50), (50, 255,255))	#Fotos gasolinera
			mask1 = cv2.inRange(hsv, (7, 134, 145), (7, 233,255))	#Fotos Mercadona

			# kernel1 = numpy.ones((25,25),numpy.uint8)
			# print(kernel1)
			kernel_banda1 = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))		# (Ancho, alto) 
			closed_banda = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, kernel_banda1)

			kernel_banda2 = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 25))		# (Ancho, alto) 
			opened_banda = cv2.morphologyEx(closed_banda, cv2.MORPH_OPEN, kernel_banda2)

			# ## mask o yellow (15,0,0) ~ (36, 255, 255)
			# mask2 = cv2.inRange(hsv, (15,0,0), (36, 255, 255))

			# ## final mask and masked
			# mask = cv2.bitwise_or(mask1, mask2)
			target = cv2.bitwise_and(images[n],images[n], mask=opened_banda)
			
			plot_color = 1
			if plot_color == 1:
				# print('hola')
				plt.subplot(231),plt.imshow(images[n])
				plt.title('Original Image'), plt.xticks([]), plt.yticks([])

				plt.subplot(232),plt.imshow(mask1, cmap='gray')
				plt.title('Máscara color'), plt.xticks([]), plt.yticks([])

				plt.subplot(233),plt.imshow(closed_banda, cmap='gray')
				plt.title('Cierre'), plt.xticks([]), plt.yticks([])

				plt.subplot(234),plt.imshow(opened_banda, cmap='gray')
				plt.title('Apertura'), plt.xticks([]), plt.yticks([])

				plt.subplot(235),plt.imshow(target)
				plt.title('Color detection'), plt.xticks([]), plt.yticks([])
				plt.show()
		
		# Busco las bandas horizontales por transformada de Hough
		else:
			cuarto1 = numpy.zeros((height, width),numpy.uint8)			
			cuarto1[0 : int(height/4), :] = 1

			cuarto2 = numpy.zeros((height, width),numpy.uint8)			
			cuarto2[int(height/4) : int(height/2), :] = 1

			cuarto3 = numpy.zeros((height, width),numpy.uint8)			
			cuarto3[int(height/2) : int(3*height/4), :] = 1

			cuarto4 = numpy.zeros((height, width),numpy.uint8)			
			cuarto4[int(3*height/4) : height, :] = 1

			image1 = cv2.bitwise_and(images[n], images[n], mask=cuarto1)
			image2 = cv2.bitwise_and(images[n], images[n], mask=cuarto2)
			image3 = cv2.bitwise_and(images[n], images[n], mask=cuarto3)
			image4 = cv2.bitwise_and(images[n], images[n], mask=cuarto4)

			plot_edges = 0
			if plot_edges == 1:
				plt.subplot(231),plt.imshow(images[n],cmap = 'gray')
				plt.title('Edges'), plt.xticks([]), plt.yticks([])

				plt.subplot(232),plt.imshow(image1,cmap = 'gray')
				plt.title('1ª franja'), plt.xticks([]), plt.yticks([])

				plt.subplot(233),plt.imshow(image2,cmap = 'gray')
				plt.title('2ª franja'), plt.xticks([]), plt.yticks([])	

				plt.subplot(234),plt.imshow(image3,cmap = 'gray')	#Pinto todas las líneas detectadas
				plt.title('3ª franja'), plt.xticks([]), plt.yticks([])

				plt.subplot(235),plt.imshow(image4,cmap = 'gray')	#Pinto las líneas definitivas
				plt.title('4ª franja'), plt.xticks([]), plt.yticks([])
				plt.show()

			edges, lines = Hough(images[n], 50)

			edges1, lines1 = Hough(image1, numero_lineas_a_detectar)	
			img_copy11 = pintar_lineas(images[n], height, width, lines1, None, None)	#Para pintar todas las líneas detectadas

			edges2, lines2 = Hough(image2, numero_lineas_a_detectar)	
			img_copy12 = pintar_lineas(images[n], height, width, lines2, None, None)	#Para pintar todas las líneas detectadas
			
			edges3, lines3 = Hough(image3, numero_lineas_a_detectar)
			img_copy13 = pintar_lineas(images[n], height, width, lines3, None, None)	#Para pintar todas las líneas detectadas
				
			edges4, lines4 = Hough(image4, numero_lineas_a_detectar)	
			img_copy14 = pintar_lineas(images[n], height, width, lines4, None, None)	#Para pintar todas las líneas detectadas

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

			
			plot_lineas = 1
			if plot_lineas == 1:
				plt.subplot(221),plt.imshow(img_copy11)
				plt.title('Cuarto 1'), plt.xticks([]), plt.yticks([])

				plt.subplot(222),plt.imshow(img_copy12)
				plt.title('Cuarto 2'), plt.xticks([]), plt.yticks([])	

				plt.subplot(223),plt.imshow(img_copy13)	#Pinto todas las líneas detectadas
				plt.title('Cuarto 3'), plt.xticks([]), plt.yticks([])

				plt.subplot(224),plt.imshow(img_copy14)	#Pinto las líneas definitivas
				plt.title('Cuarto 4'), plt.xticks([]), plt.yticks([])
				plt.show()

			if len(vector_alturas_unidas) != 0:
				img_copy1 = pintar_lineas(images[n], height, width, None, vector_alturas_unidas, vector_angulos_unidos)	#Para pintar todas las líneas detectadas

				#Miro la altura de las líneas y desecho las que representan la misma línea horizontal para quedarme solo con una
				vector_alturas, vector_angulos = seleccion_lineas_definitivas(vector_alturas_unidas, vector_angulos_unidos, separacion = 115)

				#Pinto las líneas definitivas			
				img_copy2 = pintar_lineas(images[n], height, width, None, vector_alturas, vector_angulos)	#Para pintar las líneas definitivas 

			else:
				print('Ninguna línea detectada')

			#Obtenemos el número de líneas a emparejar y ordenamos los vectores de menor rho a mayor y los ángulos acorde a cómo se han ordenado las distancias (rho)
			tam_vector, alturas_ordenadas, angulos_ordenados = ordena_alturas(vector_alturas, vector_angulos)

			#Emparejamos las líneas detectadas
			vector_mascara, alturas, vector_limites_inferiores, vector_desechadas, vector_indices, numero_de_parejas, numero_lineas_desechadas = emparejamiento_lineas(tam_vector, alturas_ordenadas)
								
			# Ancho de las bandas ya detectadas
			vector_anchos, ancho = ancho_bandas(numero_de_parejas, vector_mascara)

			#Creamos máscara para filtrar por alturas solo con las parejas detectadas directamente
			mascara = creacion_mascara(height, width, vector_mascara, flag = 1)	

			#Si el número de parejas es menor que el número de bandas significa que todavía faltan bandas por detectar
			if numero_lineas_desechadas != 0 and numero_de_parejas < numero_bandas:	#Quizás es un while ------- Miro si debo rellenar una línea desechada para formar una banda
				vector_mascara, vector_limites_inferiores, numero_de_parejas, numero_lineas_desechadas = relleno_lineas_sueltas(height, numero_bandas, vector_mascara, numero_de_parejas, vector_limites_inferiores, vector_desechadas, numero_lineas_desechadas, vector_indices, ancho)

			#En caso de que falten bandas por detectar, las creo artificialmente
			if numero_lineas_desechadas == 0 and numero_de_parejas < numero_bandas:	#Hay que crear artificialmente bandas horizontales
				vector_mascara, vector_limites_inferiores, numero_de_parejas, vector_ocupacion, separacion = bandas_artificiales(height, numero_bandas, vector_mascara, numero_de_parejas, vector_limites_inferiores, numero_lineas_desechadas)
			
			#Copia del vector actual para comparar cuando eliminemos alguna pareja
			vector_mascara_copia = vector_mascara

			#Creamos máscara con rellenos y bandas artificiales antes de eliminar parejas en zona de productos
			mascara2 = creacion_mascara(height, width, vector_mascara, flag = 0)	

			#Resultado con rellenos y bandas artificiales
			target1 = cv2.bitwise_and(images[n],images[n], mask=mascara2)

			#Comprobamos que las bandas formadas no estén en zona de productos, si es así, eliminamos esa pareja
			vector_mascara, vector_limites_inferiores, numero_de_parejas = eliminacion_bandas_productos(numero_bandas, vector_mascara, numero_de_parejas, vector_limites_inferiores)

			#Si al eliminar parejas tenemos menos que el numero de bandas, debemos de crear bandas artificiales (llamada a función de crear bandas artificiales)
			if numero_de_parejas < numero_bandas:
				vector_mascara, vector_limites_inferiores, numero_de_parejas, vector_ocupacion, separacion = bandas_artificiales(height, numero_bandas, vector_mascara, numero_de_parejas, vector_limites_inferiores, numero_lineas_desechadas)

			
			#Máscara definitiva
			mascara3 = creacion_mascara(height, width, vector_mascara, flag = 0)

			mascara3 = cv2.bitwise_or(mascara, mascara3)	#Las parejas detectadas directamente se ensancharon 20 píxeles hacia arriba y 20 píxeles 
															#hacia abajo, luego hacemos una or para quedarnos con las parejas iniciales ensanchadas
			
			#Resultado final tras eliminar bandas en productos y rellenar con bandas artificiales las bandas restantes
			target2 = cv2.bitwise_and(images[n],images[n], mask=mascara3)

			plot_lineas = 1
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

			plot_bandas = 1
			if plot_bandas == 1:				
				plt.subplot(231),plt.imshow(images[n])
				plt.title('Original Image'), plt.xticks([]), plt.yticks([])

				plt.subplot(232),plt.imshow(mascara, cmap = 'gray')	#Pinto la máscara con las parejas iniciales			
				plt.title('Parejas iniciales'), plt.xticks([]), plt.yticks([])

				plt.subplot(233),plt.imshow(mascara2, cmap = 'gray')	#Pinto la máscara con los rellenos y bandas artificiales		
				plt.title('Rellenos y bandas artificiales'), plt.xticks([]), plt.yticks([])

				plt.subplot(234),plt.imshow(target1)	#Resultado con rellenos y bandas artificiales
				plt.title('Rellenos y bandas artificiales'), plt.xticks([]), plt.yticks([])

				plt.subplot(235),plt.imshow(mascara3, cmap = 'gray')	#Pinto la máscara sin las parejas en la zona de productos y con las bandas definitivas		
				plt.title('Parejas definitivas'), plt.xticks([]), plt.yticks([])

				plt.subplot(236),plt.imshow(target2)	#Resultado con las bandas definitivas
				plt.title('Bandas detectadas'), plt.xticks([]), plt.yticks([])
				plt.show()
			
		# Cálculo gradientes y conversión a valores enteros positivos
		target_gray = cv2.cvtColor(target2, cv2.COLOR_RGB2GRAY)		

		grad_x = cv2.Sobel(target_gray, cv2.CV_16S, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
		abs_grad_x = cv2.convertScaleAbs(grad_x)

		grad_y = cv2.Sobel(target_gray, cv2.CV_16S, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
		abs_grad_y = cv2.convertScaleAbs(grad_y)
		
		# Cálculo gradiente absoluto 
		gradient1 = cv2.subtract(grad_x, grad_y)
		gradient2 = cv2.convertScaleAbs(gradient1)
		#print(gradient2.max())
		#print(gradient2.min())

		# Suavizado: probar cuál funciona mejor (gaussiano)
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

		# Se binariza la imagen, se hace paertura y luego se cierra para formar el rectángulo que engloba al código de barras
		umbral,binaria = cv2.threshold(blurred,125,255,cv2.THRESH_BINARY)	    #Para gasolinera
		# umbral,binaria = cv2.threshold(blurred,75,255,cv2.THRESH_BINARY)		#Para Mercadona
	
		kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))   		# (Ancho, alto)
		# kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 12))   		# (Ancho, alto)
		opened = cv2.morphologyEx(binaria, cv2.MORPH_OPEN, kernel1)

		kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 3))		# (Ancho, alto) 
		# kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 3))		# (Ancho, alto) 
		closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel2)

		image_copy = images[n].copy()

		masked = cv2.bitwise_and(images[n], images[n], mask=closed)
		
		"""
		cv2.imshow('original', img)
		cv2.imshow('binaria', opened)
		cv2.imshow('Codigo aislado', masked)
		cv2.imshow('Contornos', image_copy)
		cv2.waitKey() 
		"""
		
		plot_gradientes = 0
		if plot_gradientes == 1:
			plt.subplot(231),plt.imshow(images[n],cmap = 'gray')
			plt.title('Original Image'), plt.xticks([]), plt.yticks([])

			plt.subplot(232),plt.imshow(blurred,cmap = 'gray')
			plt.title('Suavizado'), plt.xticks([]), plt.yticks([])

			plt.subplot(233),plt.imshow(binaria,cmap = 'gray')
			plt.title('Binaria'), plt.xticks([]), plt.yticks([])

			plt.subplot(234),plt.imshow(opened,cmap = 'gray')
			plt.title('Apertura'), plt.xticks([]), plt.yticks([])
			
			plt.subplot(235),plt.imshow(closed,cmap = 'gray')
			plt.title('Cierre'), plt.xticks([]), plt.yticks([]) 
			
			plt.subplot(236),plt.imshow(masked,cmap = 'gray')
			plt.title('Códigos detectados'), plt.xticks([]), plt.yticks([])
			plt.show()	
		
	#############################################PROBAR cv2.ADAPTIVE_THRESH_GAUSSIAN_C#########################################################

if __name__ == "__main__":              
	funcion()






