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
	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	images = numpy.empty(len(onlyfiles), dtype=object)
	for n in range(0, len(onlyfiles)):
		images[n] = cv2.imread( join(mypath,onlyfiles[n]) ) 
		images[n] = cv2.cvtColor(images[n], cv2.COLOR_BGR2RGB)

		gray = cv2.cvtColor(images[n], cv2.COLOR_BGR2GRAY)

		edges = cv2.Canny(images[n],125,225,apertureSize=3,L2gradient=True)
		#print(edges)
		height, width = edges.shape 
		#print(height,width)

		kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))		# (Ancho, alto) 
		closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

		#Búsqueda de líneas horizontales: en el rango [85º,95º]
		lines = cv2.HoughLines(closed,rho=1,theta=numpy.pi/180,threshold=2000,srn=0,stn=0,min_theta=numpy.pi/2-0.08726,max_theta=numpy.pi/2+0.08726)
		print(len(lines))
		linesP = cv2.HoughLinesP(edges,rho=1,theta=numpy.pi/180,threshold=300,minLineLength=100,maxLineGap=5)
		img_copy1 = images[n].copy()
		img_copy2 = images[n].copy()	
		
		#print(linesP)
		#print(lines1)
		#print(lines1[0][2][0])			#Campo 0: nada, campo 1: el par (rho, theta), campo 2: rho [0] y theta [1]
		if lines is not None:
			for i in range(0, len(lines)):
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
				print(pt1,pt2)
				cv2.line(img_copy1, pt1, pt2, (255,0,0), 10, cv2.LINE_AA)

		# Draw the lines
		if linesP is not None:
			#print('hola')
			for i in range(0, len(linesP)):
				l = linesP[i][0]
				cv2.line(img_copy2, (l[0], l[1]), (l[2], l[3]), (255,0,0), 3, cv2.LINE_AA)

		plt.subplot(221),plt.imshow(images[n])
		plt.title('Original Image'), plt.xticks([]), plt.yticks([])

		plt.subplot(222),plt.imshow(edges,cmap = 'gray')
		plt.title('Edges detection'), plt.xticks([]), plt.yticks([])
		
		plt.subplot(223),plt.imshow(img_copy1)
		plt.title('Líneas detectadas '), plt.xticks([]), plt.yticks([])
		
		plt.subplot(224),plt.imshow(closed,cmap = 'gray')
		plt.title('Rellenar bordes'), plt.xticks([]), plt.yticks([])		
		plt.show()
		
		#############################################PROBAR cv2.ADAPTIVE_THRESH_GAUSSIAN_C#########################################################

if __name__ == "__main__":              
	funcion()