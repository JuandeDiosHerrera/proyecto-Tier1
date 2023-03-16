# coding=utf-8

import cv2
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join
import math
import numpy
from natsort import natsorted

# def configuracion_numero_bandas():
# 	pass	

def Hough(imagen, numero_lineas_detectadas):
	print('-------------------------------------------------------------------- Búsqueda de líneas horizontales --------------------------------------------------------------------')
	edges = cv2.Canny(imagen,125,225,apertureSize=3,L2gradient=True)
	#print(edges)
	#Búsqueda de líneas horizontales: en el rango [85º,95º] -> aumento umbral de 100 en 100 hasta quedarme con 15 líneas detectadas o menos
	lineas_detectadas = 2000
	umbral = 100
	while(lineas_detectadas>numero_lineas_detectadas):	#Para gasolinera
	# while(lineas_detectadas>25):	#Para Mercadona
		lines = cv2.HoughLines(edges,rho=1,theta=numpy.pi/180,threshold=umbral,srn=0,stn=0,min_theta=numpy.pi/2-2.5*numpy.pi/180,max_theta=numpy.pi/2+2.5*numpy.pi/180)
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

def ordena_alturas(vector_alturas, vector_angulos):
	tam_vector = len(vector_alturas)
	print('Tamaño vector:',tam_vector)

	alturas_ordenadas, angulos_ordenados = zip(*sorted(zip(vector_alturas, vector_angulos)))
	print('Vector alturas ordenados:',alturas_ordenadas)
	print('Vector ángulos ordenados:',angulos_ordenados)
	print('')
	return tam_vector, alturas_ordenadas, angulos_ordenados

def emparejamiento_lineas(tam_vector, alturas_ordenadas, height, numero_bandas):
	print('-------------------------------------------------------------------- Emparejamiento de líneas --------------------------------------------------------------------')
	vector_mascara = []			 #Vector de parejas de alturas
	alturas = []				 #Vector de alturas definitivas ordenadas
	vector_desechadas = []		 #Vector de líneas desechadas (las que no se emparejan y se quedan solas)
	indice_pareja = 0 			 #Para saber en qué índice de "vector_mascara" debo meter las líneas desechadas una vez las rellene
	vector_indices = []     	 #Vector que contiene los índice en los que se deben meter las líneas desechadas en "vector_mascara"
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

		if altura3 - altura1 <= 400 and altura3 - altura1 >= 150:	#Caso de 3 líneas muy juntas, nos quedamos con la dos más exteriores
			vector_mascara.append([altura1, altura3])
			alturas.append(altura1)						
			alturas.append(altura3)
			vector_limites_inferiores.append(altura3)
			# indice_pareja = indice_pareja + 1
			i = i + 3
			print('Líneas emparejadas:', [altura1, altura3])
			print(vector_mascara)
			print('')
		elif altura2 - altura1 <= 300 and altura2 - altura1 >= 150:		#Líneas separadas menos de 350 píxeles -> pareja de líneas
			vector_mascara.append([altura1, altura2])
			alturas.append(altura1)						# "altura1" es la línea de arriba y "altura2" es la línea de abajo
			alturas.append(altura2)
			vector_limites_inferiores.append(altura2)
			# indice_pareja = indice_pareja + 1
			i = i + 2
			print('Líneas emparejadas:', [altura1, altura2])
			print(vector_mascara)								#Incrementamos el índice de las líneas desechadas solo cuando formamos 
			print('')											#pareja, ya altura3-altura1 o altura2-altura1
		else:
			vector_desechadas.append(altura1)
			vector_indices.append(indice_pareja)
			# indice_pareja = indice_pareja + 1
			i = i + 1
			print('Línea desechada:', altura1)
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

	print('Vector ocupación:', vector_ocupacion)
	print('')
	print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------')
	return vector_mascara, alturas, vector_limites_inferiores, vector_ocupacion, vector_desechadas, vector_indices, numero_de_parejas, numero_lineas_desechadas

def ancho_bandas(numero_de_parejas, vector_mascara):
	vector_anchos = []
	ancho = 0
	if numero_de_parejas != 0:
		for i in range(numero_de_parejas):
			# print(i)
			vector_anchos.append(int(vector_mascara[i][1]-vector_mascara[i][0]))
		print('Vector anchos:', vector_anchos)
		ancho = max(vector_anchos)
		print('Ancho máximo:', ancho)	
		print('')		
	else:	#En caso de que no haya parejas formadas, se informa con un mensaje y se devuelve dos "None". Se establecerá un valor razonable para el
			#ancho como 50 píxeles más que la proximidad para formar una pareja
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

def relleno_lineas_sueltas(height, numero_bandas, vector_mascara, vector_ocupacion, numero_de_parejas, vector_limites_inferiores, vector_desechadas, numero_lineas_desechadas, vector_indices, ancho):
	#Saco ancho máximo de las bandas ya detectadas
	#Compruebo si con la altura (componente "y") que tiene en la imagen puede ser una línea de banda 
	#Si es, relleno hacia un lado y hacia el otro. Luego decremento "numero_lineas_desechadas" e incremento "numero_de_parejas"

	print('-------------------------------------------------------------------- Relleno de líneas sueltas --------------------------------------------------------------------')

	for i in range(len(vector_desechadas)):
		# print(i)
		print('Línea desechada:', vector_desechadas[i])
		print('Vector límites inferiores:', vector_limites_inferiores)
		#Las líneas detectadas en los productos suelen estar justo debajo de una banda horizontal que es cuando acaba 
		#la parte de arriba de las cajas/tetrabrick. Si se detecta el final de las cajas/tetrabrick por debajo, da igual porque nos sirve
		#para detectar el límite superior de la banda que está debajo de la caja/tetrabrick. Para ello debo mirar que la banda de arriba
		#de la línea desechada que queremos rellenar ya está detectada		
		#También miro que desde el límite inferior de la banda de arriba a la línea haya suficiente distancia (se ha establecido una distancia de 3 veces el ancho máximo)			
		
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

		#Condiciones:
		# - Línea desechada separada más de 3 veces el ancho máximo de las bandas ya detectadas ó tener índice 0 y por tanto ser la banda de más arriba
		# - Que todavía falten parejas por formar (menos parejas que bandas)
		# - Estar en una franja en la que no hay ninguna pareja aún	
		separacion_teorica = int(height / numero_bandas)					
		indice_vector_ocupacion = 0
		alturas_franjas = [separacion_teorica * (i + 1) for i in range(0, numero_bandas)]
		print('Franjas:', alturas_franjas)

		relleno = 0
		for j in range(len(alturas_franjas)):
			if j == 0:	#Con el índice 0 se compara con altura 0 y el primer elemento de "alturas_franjas"
				if vector_desechadas[i] > 0 and vector_desechadas[i] < alturas_franjas[j] and vector_ocupacion[j] == 0:
					relleno = 1 
					print('Franja superior:', 0, '---','Franja inferior:', alturas_franjas[j], '---', 'Elemento vector ocupación:', vector_ocupacion[j], '---', 'Relleno:', relleno)
					break
				else:				
					relleno = 0
					print('Franja superior:', 0, '---','Franja inferior:', alturas_franjas[j], '---', 'Elemento vector ocupación:', vector_ocupacion[j], '---', 'Relleno:', relleno)
			else:
				if vector_desechadas[i] > alturas_franjas[j-1] and vector_desechadas[i] < alturas_franjas[j] and vector_ocupacion[j] == 0:
					relleno = 1 
					print('Franja superior:', alturas_franjas[j-1], '---','Franja inferior:', alturas_franjas[j], '---', 'Elemento vector ocupación:', vector_ocupacion[j], '---', 'Relleno:', relleno)
					break
				else:				
					relleno = 0
					print('Franja superior:', alturas_franjas[j-1], '---','Franja inferior:', alturas_franjas[j], '---', 'Elemento vector ocupación:', vector_ocupacion[j], '---', 'Relleno:', relleno)

		print('Valor de j al salir del bucle:', j)
		# "aux1[indice]" es la altura del límite de abajo de la banda más cercana por arriba a la línea desechada en cuestión
		if (vector_desechadas[i] > aux1[indice] + 3 * ancho or vector_indices[i] == 0) and numero_de_parejas < numero_bandas and relleno == 1: 
			if vector_desechadas[i] - ancho < 0:	
				vector_mascara.insert(vector_indices[i], [0, vector_desechadas[i] + ancho])	#Relleno hacia ambos lados
				print('Línea rellenada hacia ambos lados:', [0, vector_desechadas[i] + ancho])
			elif vector_desechadas[i] + ancho > 3000:
				vector_mascara.insert(vector_indices[i], [vector_desechadas[i] - ancho, 3000])	#Relleno hacia ambos lados
				print('Línea rellenada hacia ambos lados:', [vector_desechadas[i] - ancho, 3000])
			else:
				vector_mascara.insert(vector_indices[i], [vector_desechadas[i] - ancho, vector_desechadas[i] + ancho])	#Relleno hacia ambos lados
				print('Línea rellenada hacia ambos lados:', [vector_desechadas[i] - ancho, vector_desechadas[i] + ancho])
			vector_limites_inferiores.insert(vector_indices[i], vector_desechadas[i] + ancho)
			vector_ocupacion[j] = 1
			numero_de_parejas = numero_de_parejas + 1			
			print('Vector máscara tras añadir la línea:', vector_mascara)
			print('Vector límites inferiores tras añadir la línea:', vector_limites_inferiores)
			print('Vector ocupación:', vector_ocupacion)
		else:
			print('Línea eliminada definitivamente')
			vector_indices = [x - 1 for x in vector_indices]			
			print('Vector índices:', vector_indices)
		
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
	return vector_mascara, vector_limites_inferiores, vector_ocupacion, numero_de_parejas, numero_lineas_desechadas

def bandas_artificiales(height, numero_bandas, vector_mascara, vector_ocupacion, numero_de_parejas, vector_limites_inferiores, numero_lineas_desechadas):
	print('-------------------------------------------------------------------- Relleno bandas artificiales --------------------------------------------------------------------')
	#Miro la altura de las bandas ya detectadas y sabiendo que son equidistantes creo artificialmente las que queden 
	#hasta llegar a "numero_de_parejas == numero_bandas -> hasta completar el vector de ocupación" 
		
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
		elif i < len(vector_ocupacion) - 2 and vector_ocupacion[i] == 1 and vector_ocupacion[i+2] == 1:
			altura1_media = int((vector_mascara[i][0] + vector_mascara[i][1]) / 2)
			altura2_media = int((vector_mascara[i+2][0] + vector_mascara[i+2][1]) / 2)
			vector_separaciones.append(int((altura2_media - altura1_media) / 2))
		i = i + 1		

	if len(vector_separaciones) == 0:
		print('No hay dos bandas consecutivas para obtener la separación entre ellas')	
		
######################################## MIRAR EL CASO EN QUE NO HAY BANDAS CONSECUTIVAS (EL ELSE) ###############################################
	separacion_teorica = int(height / numero_bandas)				
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

def eliminacion_bandas_productos(height, numero_bandas, vector_mascara, vector_ocupacion, numero_de_parejas, vector_limites_inferiores):
	print('---------------------------------------------------------- Eliminación bandas en productos --------------------------------------------------------------------')
	print('Vector máscara:', vector_mascara)
	print('')

	valor_auxiliar = 0
	#Quizás hacer el bucle for con la longitud de "vector_mascara" -> for i in range(len(vector_mascara) - 1)
	for i in range(len(vector_mascara) - 1):	#Ejemplo: 4 bandas detectadas -> i va [0, 2] < 4 - 1 = 3
		print('Índice:',i,'---',vector_mascara[i-valor_auxiliar][1],'---',vector_mascara[i+1-valor_auxiliar][0])
		if abs(vector_mascara[i-valor_auxiliar][1]-vector_mascara[i+1-valor_auxiliar][0]) < 350:	#Parejas muy próximas -> eliminamos la de abajo
			print('Pareja eliminada:', vector_mascara[i+1])
			vector_mascara.pop(i+1)
			vector_limites_inferiores.pop(i+1)
			print('Vector máscara tras eliminar pareja en zona de productos:', vector_mascara)
			valor_auxiliar = valor_auxiliar + 1
			numero_de_parejas = numero_de_parejas - 1
		print('')

	#Recalculamos el "vector_ocupacion"
	separacion_teorica = int(height / numero_bandas)								

	vector_ocupacion = [0, 0, 0]
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

	print('Vector máscara:', vector_mascara)
	print('Vector ocupación:', vector_ocupacion)
	print('Número de parejas actuales:', numero_de_parejas)
	print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------')
	print('')
	return vector_mascara, vector_limites_inferiores, numero_de_parejas, vector_ocupacion

def Hough_franjas(numero_bandas, height, width, image, numero_lineas_a_detectar):
	edges, lines = Hough(image, 50)
	if numero_bandas == 2:
		cuarto1 = numpy.zeros((height, width),numpy.uint8)			
		cuarto1[0 : int(height/2), :] = 1

		cuarto2 = numpy.zeros((height, width),numpy.uint8)			
		cuarto2[int(height/2) : height, :] = 1

		image1 = cv2.bitwise_and(image, image, mask=cuarto1)
		image2 = cv2.bitwise_and(image, image, mask=cuarto2)

		plot_franjas = 0
		if plot_franjas == 1:
			plt.subplot(221),plt.imshow(image,cmap = 'gray')
			plt.title('Edges'), plt.xticks([]), plt.yticks([])

			plt.subplot(222),plt.imshow(image1,cmap = 'gray')
			plt.title('1ª franja'), plt.xticks([]), plt.yticks([])

			plt.subplot(223),plt.imshow(image2,cmap = 'gray')
			plt.title('2ª franja'), plt.xticks([]), plt.yticks([])	
			plt.show()

		edges1, lines1 = Hough(image1, numero_lineas_a_detectar)	
		img_copy11 = pintar_lineas(image, height, width, lines1, None, None)	#Para pintar todas las líneas detectadas

		edges2, lines2 = Hough(image2, numero_lineas_a_detectar)	
		img_copy12 = pintar_lineas(image, height, width, lines2, None, None)	#Para pintar todas las líneas detectadas

		#Hay que unir los 2 elementos "lineX"
		vector_alturas_unidas = []
		vector_angulos_unidos = []
		for i in lines1:
			vector_alturas_unidas.append(i[0][0])
			vector_angulos_unidos.append(i[0][1])
		for i in lines2:
			vector_alturas_unidas.append(i[0][0])
			vector_angulos_unidos.append(i[0][1])
		
		plot_edges = 0
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

		plot_franjas = 0
		if plot_franjas == 1:
			plt.subplot(221),plt.imshow(image,cmap = 'gray')
			plt.title('Edges'), plt.xticks([]), plt.yticks([])

			plt.subplot(222),plt.imshow(image1,cmap = 'gray')
			plt.title('1ª franja'), plt.xticks([]), plt.yticks([])

			plt.subplot(223),plt.imshow(image2,cmap = 'gray')
			plt.title('2ª franja'), plt.xticks([]), plt.yticks([])	

			plt.subplot(224),plt.imshow(image3,cmap = 'gray')	#Pinto todas las líneas detectadas
			plt.title('3ª franja'), plt.xticks([]), plt.yticks([])
			plt.show()

		edges1, lines1 = Hough(image1, numero_lineas_a_detectar)	
		img_copy11 = pintar_lineas(image, height, width, lines1, None, None)	#Para pintar todas las líneas detectadas

		edges2, lines2 = Hough(image2, numero_lineas_a_detectar)	
		img_copy12 = pintar_lineas(image, height, width, lines2, None, None)	#Para pintar todas las líneas detectadas
		
		edges3, lines3 = Hough(image3, numero_lineas_a_detectar)
		img_copy13 = pintar_lineas(image, height, width, lines3, None, None)	#Para pintar todas las líneas detectadas

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
		
		plot_edges = 0
		if plot_edges == 1:
			plt.subplot(221),plt.imshow(img_copy11)
			plt.title('Cuarto 1'), plt.xticks([]), plt.yticks([])

			plt.subplot(222),plt.imshow(img_copy12)
			plt.title('Cuarto 2'), plt.xticks([]), plt.yticks([])	

			plt.subplot(223),plt.imshow(img_copy13)	#Pinto todas las líneas detectadas
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

		plot_franjas = 0
		if plot_franjas == 1:
			plt.subplot(231),plt.imshow(image,cmap = 'gray')
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

		edges1, lines1 = Hough(image1, numero_lineas_a_detectar)	
		img_copy11 = pintar_lineas(image, height, width, lines1, None, None)	#Para pintar todas las líneas detectadas

		edges2, lines2 = Hough(image2, numero_lineas_a_detectar)	
		img_copy12 = pintar_lineas(image, height, width, lines2, None, None)	#Para pintar todas las líneas detectadas
		
		edges3, lines3 = Hough(image3, numero_lineas_a_detectar)
		img_copy13 = pintar_lineas(image, height, width, lines3, None, None)	#Para pintar todas las líneas detectadas
			
		edges4, lines4 = Hough(image4, numero_lineas_a_detectar)	
		img_copy14 = pintar_lineas(image, height, width, lines4, None, None)	#Para pintar todas las líneas detectadas

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
		
		plot_edges = 0
		if plot_edges == 1:
			plt.subplot(221),plt.imshow(img_copy11)
			plt.title('Cuarto 1'), plt.xticks([]), plt.yticks([])

			plt.subplot(222),plt.imshow(img_copy12)
			plt.title('Cuarto 2'), plt.xticks([]), plt.yticks([])	

			plt.subplot(223),plt.imshow(img_copy13)	#Pinto todas las líneas detectadas
			plt.title('Cuarto 3'), plt.xticks([]), plt.yticks([])

			plt.subplot(224),plt.imshow(img_copy14)	#Pinto las líneas definitivas
			plt.title('Cuarto 4'), plt.xticks([]), plt.yticks([])
			plt.show()

	return edges, vector_alturas_unidas, vector_angulos_unidos

def calcula_banda(image, height, width):
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

	print('Altura banda zoom:',alturas_ordenadas)

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
	# plt.title('Resta'), plt.xtic plt.yticks(ks([]),[])		
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

	print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------')
	print('')

	return target_gray, binaria, closed, opened, masked

def funcion():
	#mypath='C:\\Users\\joseh\\Documents\\Juan de Dios\\TFG\\Fotos'
	#mypath='E:\\Documents\\Juan de Dios\\TFG\\Fotos folio'
	# mypath='E:\\Documents\\Juan de Dios\\TFG\\Fotos gasolinera\\3B'
	#mypath='E:\\Documents\\Juan de Dios\\TFG\\Fotos productos'
	# mypath='E:\\Documents\\Juan de Dios\\TFG\\Fotos Mercadona\\4B'
	mypath='E:\\Documents\\Juan de Dios\\TFG\\Fotos Mercadona\\Misma altura'
	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	onlyfiles = natsorted(onlyfiles)
	images = numpy.empty(len(onlyfiles), dtype=object)
	for n in range(0, len(onlyfiles)):
		images[n] = cv2.imread( join(mypath,onlyfiles[n]) ) 
		hsv = cv2.cvtColor(images[n], cv2.COLOR_BGR2HSV)
		images[n] = cv2.cvtColor(images[n], cv2.COLOR_BGR2RGB)

		height, width, channels = images[n].shape 
		#print('alto:', height)
		#print('ancho:', width)

		# gray = cv2.cvtColor(images[n], cv2.COLOR_RGB2GRAY)

		numero_bandas = 3
		numero_lineas_a_detectar = 10

		vector_aprendizaje = [[0,0], [0,0], [0,0]]	

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --- Número de bandas --- Líneas detectadas --- Proximidad para unir líneas --- Proximidad para pareja de líneas --- Separación con borde inferior de la banda de arriba --- Proximidad para eliminar banda ---
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --- 		2 		   --- 		 15 		 --- 			175 		   	 --- 			  350 			      --- 		 Límite inferior + 4 * ancho máximo		      --- 				400				 ---
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --- 		3 		   --- 		 20 		 --- 			150 	  	  	 --- 			  300 			      --- 		 Límite inferior + 3 * ancho máximo		      ---				350				 ---
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --- 		4 		   --- 		 30 		 --- 			115  	  	  	 --- 			  175 			      --- 		 Límite inferior + 3 * ancho máximo		      ---				275				 ---	
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --- 		5 		   --- 		 35 		 --- 			75  	  	  	 --- 			  150 			      --- 		 Límite inferior + 3 * ancho máximo		      ---								 ---
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

		#Busco las bandas horizontales por su color
		filtro_color = 0
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
			edges, vector_alturas_unidas, vector_angulos_unidos = Hough_franjas(numero_bandas, height, width, images[n], numero_lineas_a_detectar)

			if len(vector_alturas_unidas) != 0:
				img_copy1 = pintar_lineas(images[n], height, width, None, vector_alturas_unidas, vector_angulos_unidos)	#Para pintar todas las líneas detectadas

				#Miro la altura de las líneas y desecho las que representan la misma línea horizontal para quedarme solo con una
				vector_alturas, vector_angulos = seleccion_lineas_definitivas(vector_alturas_unidas, vector_angulos_unidos, separacion = 150)

				#Pinto las líneas definitivas			
				img_copy2 = pintar_lineas(images[n], height, width, None, vector_alturas, vector_angulos)	#Para pintar las líneas definitivas 
			else:
				print('Ninguna línea detectada')

			#Obtenemos el número de líneas a emparejar y ordenamos los vectores de menor rho a mayor y los ángulos acorde a cómo se han ordenado las distancias (rho)
			tam_vector, alturas_ordenadas, angulos_ordenados = ordena_alturas(vector_alturas, vector_angulos)

			#Emparejamos las líneas detectadas
			vector_mascara, alturas, vector_limites_inferiores, vector_ocupacion, vector_desechadas, vector_indices, numero_de_parejas, numero_lineas_desechadas = emparejamiento_lineas(tam_vector, alturas_ordenadas, height, numero_bandas)
								
			# Ancho de las bandas ya detectadas
			vector_anchos, ancho = ancho_bandas(numero_de_parejas, vector_mascara)
			if ancho == 0:
				ancho = 350

			#Creamos máscara para filtrar por alturas solo con las parejas detectadas directamente
			mascara = creacion_mascara(height, width, vector_mascara, flag = 1)	


			# plt.subplot(111),plt.imshow(img_copy2)	#Pinto las líneas definitivas
			# plt.title('Líneas definitivas'), plt.xticks([]), plt.yticks([])
			# plt.show()


			#Si el número de parejas es menor que el número de bandas significa que todavía faltan bandas por detectar
			if numero_lineas_desechadas != 0 and numero_de_parejas < numero_bandas:	#Quizás es un while ------- Miro si debo rellenar una línea desechada para formar una banda
				vector_mascara, vector_limites_inferiores, vector_ocupacion, numero_de_parejas, numero_lineas_desechadas = relleno_lineas_sueltas(height, numero_bandas, vector_mascara, vector_ocupacion, numero_de_parejas, vector_limites_inferiores, vector_desechadas, numero_lineas_desechadas, vector_indices, ancho)

			#En caso de que falten bandas por detectar, las creo artificialmente
			if numero_lineas_desechadas == 0 and numero_de_parejas < numero_bandas:	#Hay que crear artificialmente bandas horizontales
				vector_mascara, vector_limites_inferiores, numero_de_parejas, vector_ocupacion, separacion = bandas_artificiales(height, numero_bandas, vector_mascara, vector_ocupacion, numero_de_parejas, vector_limites_inferiores, numero_lineas_desechadas)
			
			#Copia del vector actual para comparar cuando eliminemos alguna pareja
			vector_mascara_copia = vector_mascara

			#Creamos máscara con rellenos y bandas artificiales antes de eliminar parejas en zona de productos
			mascara2 = creacion_mascara(height, width, vector_mascara, flag = 0)	

			#Resultado con rellenos y bandas artificiales
			target1 = cv2.bitwise_and(images[n],images[n], mask=mascara2)

			#Comprobamos que las bandas formadas no estén en zona de productos, si es así, eliminamos esa pareja y formamos la máscara con las parejas eliminadas
			
			#############################################################################################################################################
			#Quizás se podría quitar la eliminación de bandas en zonas de productos "eliminacion_bandas_productos()" porque
			#con la fase de aprendizaje ya vamos a eliminar esas alturas
			#############################################################################################################################################
			
			vector_mascara, vector_limites_inferiores, numero_de_parejas, vector_ocupacion = eliminacion_bandas_productos(height, numero_bandas, vector_mascara, vector_ocupacion, numero_de_parejas, vector_limites_inferiores)
			mascara3 = creacion_mascara(height, width, vector_mascara, flag = 0)	

			#Si al eliminar parejas tenemos menos que el numero de bandas, debemos de crear bandas artificiales (llamada a función de crear bandas artificiales)
			# if numero_de_parejas < numero_bandas:
			# 	vector_mascara, vector_limites_inferiores, numero_de_parejas, vector_ocupacion, separacion = bandas_artificiales(height, numero_bandas, vector_mascara, vector_ocupacion, numero_de_parejas, vector_limites_inferiores, numero_lineas_desechadas)
			
			#Máscara definitiva
			mascara4 = creacion_mascara(height, width, vector_mascara, flag = 0)

			# mascara4 = cv2.bitwise_or(mascara, mascara4)	#Las parejas detectadas directamente se ensancharon 20 píxeles hacia arriba y 20 píxeles 
															#hacia abajo, luego hacemos una or para quedarnos con las parejas iniciales ensanchadas
			
			#Resultado final tras eliminar bandas en productos y rellenar con bandas artificiales las bandas restantes
			target2 = cv2.bitwise_and(images[n],images[n], mask=mascara4)

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

			plot_bandas = 1
			if plot_bandas == 1:				
				plt.subplot(331),plt.imshow(img_copy2)
				plt.title('Líneas definitivas'), plt.xticks([]), plt.yticks([])

				plt.subplot(332),plt.imshow(mascara, cmap = 'gray')	#Pinto la máscara con las parejas iniciales			
				plt.title('Parejas iniciales'), plt.xticks([]), plt.yticks([])

				plt.subplot(333),plt.imshow(mascara2, cmap = 'gray')	#Pinto la máscara con los rellenos y bandas artificiales		
				plt.title('Rellenos y bandas artificiales'), plt.xticks([]), plt.yticks([])

				plt.subplot(334),plt.imshow(target1)	#Resultado con rellenos y bandas artificiales
				plt.title('Resultado con rellenos y bandas artificiales'), plt.xticks([]), plt.yticks([])

				plt.subplot(335),plt.imshow(mascara3, cmap = 'gray')	#Pinto la máscara sin las parejas en la zona de productos y con las bandas definitivas		
				plt.title('Parejas eliminadas'), plt.xticks([]), plt.yticks([])

				plt.subplot(336),plt.imshow(mascara4, cmap = 'gray')	#Pinto la máscara sin las parejas en la zona de productos y con las bandas definitivas		
				plt.title('Nuevo relleno y máscara definitiva'), plt.xticks([]), plt.yticks([])

				plt.subplot(337),plt.imshow(target2)	#Resultado con las bandas definitivas
				plt.title('Bandas detectadas'), plt.xticks([]), plt.yticks([])
				plt.show()

			#Una vez creada la máscara definitiva, aplicamos la fase de aprendizaje
			#Leemos de las fotos de cerca con un bucle for y aplicamos "gradientes.py"
			#Segundo bucle para leer las fotos con zoom de las bandas identificadas
			print('----------------------------------------------------------------- Fase de aprendizaje --------------------------------------------------------------------')
			mypath2='E:\\Documents\\Juan de Dios\\TFG\\Fotos gasolinera\\Zoom'
			onlyfiles2 = [ f for f in listdir(mypath2) if isfile(join(mypath2,f)) ]
			onlyfiles2 = natsorted(onlyfiles2)
			# print(onlyfiles2)
			images2 = numpy.empty(len(onlyfiles2), dtype=object)
			"""
			for m in range(0, len(onlyfiles2)):
				images2[m] = cv2.imread( join(mypath2,onlyfiles2[m]) ) 
				images2[m] = cv2.cvtColor(images2[m], cv2.COLOR_BGR2RGB)

				# plt.subplot(111),plt.imshow(images2[m])	#Pinto las líneas definitivas
				# plt.title('Foto'), plt.xticks([]), plt.yticks([])
				# plt.show()	

				target_gray, binaria, closed, opened, masked = calcula_banda(images2[n], height, width)

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
	funcion()






