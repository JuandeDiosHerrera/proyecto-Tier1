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

		height, width = edges.shape 

		#Búsqueda de líneas horizontales: en el rango [80º,100º]
		lines = cv2.HoughLines(edges,rho=1,theta=numpy.pi/180,threshold=1200,srn=0,stn=0,min_theta=numpy.pi/2-0.08726,max_theta=numpy.pi/2+0.08726)
		#print(len(lines))
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
				a = math.cos(theta)
				b = math.sin(theta)
				x0 = a * rho
				y0 = b * rho
				pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
				pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
				cv2.line(img_copy1, pt1, pt2, (255,0,0), 10, cv2.LINE_AA)

		# Draw the lines
		if linesP is not None:
			#print('holw')
			for i in range(0, len(linesP)):
				l = linesP[i][0]
				cv2.line(img_copy2, (l[0], l[1]), (l[2], l[3]), (255,0,0), 3, cv2.LINE_AA)

		plt.subplot(221),plt.imshow(images[n])
		plt.title('Original Image'), plt.xticks([]), plt.yticks([])

		plt.subplot(222),plt.imshow(edges,cmap = 'gray')
		plt.title('Edges detection'), plt.xticks([]), plt.yticks([])
		
		plt.subplot(223),plt.imshow(img_copy1)
		plt.title('Líneas detectadas '), plt.xticks([]), plt.yticks([])
		
		plt.subplot(224),plt.imshow(img_copy2)
		plt.title('Líneas detectadas prob'), plt.xticks([]), plt.yticks([])		
		plt.show()
		
		#############################################PROBAR cv2.ADAPTIVE_THRESH_GAUSSIAN_C#########################################################

if __name__ == "__main__":              
	funcion()