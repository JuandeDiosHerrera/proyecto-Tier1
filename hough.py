#!/usr/bin/env python2
# coding=utf-8

import cv2
from matplotlib import pyplot as plt
import numpy as np
import math

def funcion():
	img = cv2.imread("/home/juan/Descargas/ean13.jpg") 
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	#cv2.imshow('original', img)

	edges = cv2.Canny(img,100,200)
	#cv2.imshow('edges', edges)

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

	
	plt.subplot(221),plt.imshow(img)
	plt.title('Original Image'), plt.xticks([]), plt.yticks([])
	plt.subplot(222),plt.imshow(edges,cmap = 'gray')
	plt.title('Edges Image'), plt.xticks([]), plt.yticks([])
	plt.subplot(223),plt.imshow(img_copy1)
	plt.title('Standard Hough'), plt.xticks([]), plt.yticks([])
	plt.subplot(224),plt.imshow(img_copy2)
	plt.title('Probabilistic Hough'), plt.xticks([]), plt.yticks([])
	plt.show()
	
	#cv2.imshow('lines', img_copy)
	#cv2.waitKey() 

	#############################################PROBAR cv2.ADAPTIVE_THRESH_GAUSSIAN_C#########################################################

if __name__ == "__main__":              
    funcion()

