import cv2
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join
from lineas import calcula_banda
import numpy
 
bardet = cv2.barcode_BarcodeDetector()

# mypath='C:\\Users\\joseh\\Documents\\Juan de Dios\\TFG\\Fotos folio'
mypath='E:\\Documents\\Juan de Dios\\TFG\\Fotos gasolinera\\Zoom'
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
images = numpy.empty(len(onlyfiles), dtype=object)
for n in range(0, len(onlyfiles)):
	images[n] = cv2.imread( join(mypath,onlyfiles[n]) )
	images[n] = cv2.cvtColor(images[n], cv2.COLOR_BGR2RGB)
	height, width, channels = images[n].shape 


	target, target_gray, blurred, binaria, closed, opened, masked = calcula_banda(images[n], height, width)

	kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 50))		# (Ancho, alto) 
	dilated = cv2.dilate(opened, kernel3)

	masked2 = cv2.bitwise_and(images[n], images[n], mask=dilated)


	ok, decoded_info, decoded_type, corners = bardet.detectAndDecode(masked2)		
	
	# Detección, códigos decodificados, tipos de códigos y esquinas de los códigos:
	print(ok)    
	print('Decoded info:',decoded_info)
	print('Decoded type:',decoded_type)		
	print('Corners:', corners)					 #"Corners" desde esquina inferior izquierda en sentido horario
	print('')	

	# plt.subplot(111),plt.imshow(images[n])
	# plt.title('Imagen'), plt.xticks([]), plt.yticks([])
	# plt.show()

	# plt.subplot(221),plt.imshow(images[n])
	# plt.title('Zoom Image'), plt.xticks([]), plt.yticks([])
	# plt.subplot(222),plt.imshow(target)
	# plt.title('Banda identificada'), plt.xticks([]), plt.yticks([])		
	# plt.subplot(223),plt.imshow(target_gray, cmap = 'gray')
	# plt.title('Banda grayscale'), plt.xticks([]), plt.yticks([])	
	# plt.show()	

	plt.subplot(231),plt.imshow(blurred,cmap = 'gray')
	plt.title('Suavizado gaussiano'), plt.xticks([]), plt.yticks([])
	plt.subplot(232),plt.imshow(binaria,cmap = 'gray')
	plt.title('Binaria'), plt.xticks([]), plt.yticks([])		
	plt.subplot(233),plt.imshow(closed,cmap = 'gray')
	plt.title('Cierre'), plt.xticks([]), plt.yticks([])	
	plt.subplot(234),plt.imshow(opened,cmap = 'gray')
	plt.title('Apertura'), plt.xticks([]), plt.yticks([])
	plt.subplot(235),plt.imshow(dilated,cmap = 'gray')
	plt.title('Dilatado'), plt.xticks([]), plt.yticks([])
	plt.subplot(236),plt.imshow(masked2)
	plt.title('Códigos detectados'), plt.xticks([]), plt.yticks([])
	plt.show()	



	
	lista_anchos = []
	lista_alturas = []  
	lista_areas = []  

	img_copy = images[n].copy()
	#print(corners)
	if ok == False:
		print('Código de barra no detectado')

		# plt.subplot(111),plt.imshow(images[n])
		# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
		# plt.show()

	else:
		for i in range(len(corners)):  # Para todos los códigos de barras
			lista_x = []
			lista_y = []
			for j in range(4):  # Para un código de barras concreto           
				x = int(corners[i][j][0])                #Desde esquina inferior izquierda en sentido horario
				y = int(corners[i][j][1])
				lista_x.append(x)
				lista_y.append(y)

				#print(x,y)
				cv2.circle(img_copy, (int(x),int(y)), 15, (255,0,0), -1) 

			ancho = lista_x[3] - lista_x[0]
			alto = lista_y[0] - lista_y[2]
			#print(ancho,alto)
			#print(lista_y)
			lista_anchos.append(ancho)
			lista_alturas.append(alto)
			lista_areas.append(ancho*alto)

			#print(lista_alturas)
			#print('\n')

		# print(lista_alturas,lista_anchos,lista_areas)    

		# plt.subplot(121),plt.imshow(images[n])
		# plt.title('Original Image'), plt.xticks([]), plt.yticks([])

		# plt.subplot(122),plt.imshow(img_copy)
		# plt.title('Barcode detection'), plt.xticks([]), plt.yticks([])
		# plt.show()
		"""
		plt.subplot(111),plt.imshow(img_copy)
		plt.title('Image'), plt.xticks([]), plt.yticks([])
		plt.show()
		"""
"""
cv2.imshow('Image', img)
cv2.waitKey()
"""


#print(len(corners))


	
