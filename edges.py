#!/usr/bin/env python2
# coding=utf-8

import cv2
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join
import numpy
import math

def funcion():
	#mypath='C:\\Users\\joseh\\Documents\\Juan de Dios\\TFG\\Fotos'
	mypath='E:\\Documents\\Juan de Dios\\TFG\\Fotos'
	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	images = numpy.empty(len(onlyfiles), dtype=object)
	for n in range(0, len(onlyfiles)):
		images[n] = cv2.imread( join(mypath,onlyfiles[n]) ) 
		images[n] = cv2.cvtColor(images[n], cv2.COLOR_BGR2RGB)
		#cv2.imshow('original', img)

		edges = cv2.Canny(images[n],100,200)
		#cv2.imshow('edges', edges)

		kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (100, 7))
		closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel1)
		#cv2.imshow('cierre', closed)

		kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
		opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel2)

		# Se buscan los contornos del rectángulo y se pintan
		opened_copy = opened.copy()
		contours, hierarchy = cv2.findContours(opened_copy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		image_copy = images[n].copy()

		# Obtención de los rectángulos que circunscriben a los códigos de barras
		minRect = [None]*len(contours)
		#print(range(len(contours[0])))
		#print(contours)
		for i, c in enumerate(contours):
			#print(c)
			minRect[i] = cv2.minAreaRect(c)	#(center(x, y), (width, height), angle of rotation) = cv2.minAreaRect(points)
		#print(minRect)

		"""
		# Para sacar solo las esquinas del contorno no el contorno entero	
		for i in range(len(contours[0])):
			x = contours[0][i][0][0]
			y = contours[0][i][0][1]
			#print(x,y)
			cv2.circle(image_copy, (x,y), 7, (0,0,255), -1)
			#cv2.drawContours(image_copy, [contours[i], [], (0,0,255), 6)
			#cv2.drawContours(image_copy, [contours[i], 1, (0,0,255), 6)
		"""
		for i in contours:
			M = cv2.moments(i)
			#if M['m00'] != 0:
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])
			#cv2.drawContours(image_copy, [i], -1, (0, 255, 0), 6)
			cv2.circle(image_copy, (cx, cy), 20, (255, 0, 0), -1)

		masked = cv2.bitwise_and(images[n], images[n], mask=opened)
		"""
		
		#Búsqueda de las líneas con la transformada de Hough estándary la probabilística	
			lines1 = cv2.HoughLines(edges, 1, np.pi / 180, 150, None, 0, 0)
		img_copy1 = img.copy()
		#print(lines1)
		#print(lines1[0][2][0])			#Campo 0: nada, campo 1: el par (rho, theta), campo 2: rho [0] y theta [1]
			if lines1 is not None:
			for i in range(len(lines1[0])):
				rho = lines1[0][i][0]
				theta = lines1[0][i][1]
				a = math.cos(theta)
				b = math.sin(theta)
				x0 = a * rho
				y0 = b * rho
				pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
				pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
				cv2.line(img_copy1, pt1, pt2, (255,0,0), 1, cv2.CV_AA)

			lines2 = cv2.HoughLinesP(edges, 0.8, np.pi / 180, 90, minLineLength=100, maxLineGap=10) # Hough Lines Transform	
		img_copy2 = img.copy()
			
		#print(lines2)
		#print(range(0,len(lines[0])))
		#print(lines2[0][0][3])		#Campo 0: nada, campo 1: pareja de puntos (comienzo y fin del segmento), campo 2: (x0 y0 x1 y1)
		
		# Draw the lines	
			if lines2 is not None:			
			for i in range(len(lines2[0])):
				l = lines2[0][i]
				#print(l)
				cv2.line(img_copy2, (l[0], l[1]), (l[2], l[3]), (255,0,0), 1, cv2.CV_AA)
		
		"""
		plt.subplot(231),plt.imshow(images[n])
		plt.title('Original Image'), plt.xticks([]), plt.yticks([])

		plt.subplot(232),plt.imshow(edges,cmap = 'gray')
		plt.title('Edges Image'), plt.xticks([]), plt.yticks([])
		"""
		plt.subplot(233),plt.imshow(img_copy1)
		plt.title('Standard Hough'), plt.xticks([]), plt.yticks([])

		plt.subplot(234),plt.imshow(img_copy2)
		plt.title('Probabilistic Hough'), plt.xticks([]), plt.yticks([])
		"""
		plt.subplot(233),plt.imshow(opened,cmap = 'gray')
		plt.title('Morphologic Image'), plt.xticks([]), plt.yticks([])

		plt.subplot(234),plt.imshow(image_copy,cmap = 'gray')
		plt.title('Centros de masas'), plt.xticks([]), plt.yticks([])

		plt.subplot(235),plt.imshow(masked)
		plt.title('Barcode detection'), plt.xticks([]), plt.yticks([])		
		plt.show()
		
		#cv2.imshow('lines', img_copy)
		#cv2.waitKey() 

	#############################################PROBAR cv2.ADAPTIVE_THRESH_GAUSSIAN_C#########################################################

if __name__ == "__main__":              
    funcion()

