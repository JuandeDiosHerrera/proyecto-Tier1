#!/usr/bin/env python2
# coding=utf-8

import numpy as np
import cv2

def funcion():
	img = cv2.imread("/home/juan/Descargas/ean13.jpg") 
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	cv2.imshow('original', img)

	"""
	gaus = cv2.GaussianBlur(gray,(5,5),0)
	"""
	# Cálculo gradientes y conversión a valores enteros positivos
	grad_x = cv2.Sobel(gray, cv2.CV_16S, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
	abs_grad_x = cv2.convertScaleAbs(grad_x)

	grad_y = cv2.Sobel(gray, cv2.CV_16S, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
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
	#binaria1 = cv2.adaptiveThreshold(abs_grad_x,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
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
	gradient = cv2.subtract(grad_x, grad_y)
	gradient = cv2.convertScaleAbs(gradient)
	#blurred = cv2.blur(gradient, (9, 9))

	# Se binariza la imagen y se cierra para formar el rectángulo que engloba al código de barras
	umbral,binaria = cv2.threshold(gradient,200,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	#cv2.imshow('binaria', binaria)
	kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
	closed = cv2.morphologyEx(binaria, cv2.MORPH_CLOSE, kernel1)
	#cv2.imshow('cierre', closed)

	kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
	opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel1)
	#opened = cv2.erode(closed, kernel2, iterations = 4)
	#opened = cv2.dilate(closed, kernel2, iterations = 4)

	#cv2.imshow('apertura', opened)


	# Se buscan los contornos del rectángulo y se pintan
	contours, hierarchy = cv2.findContours(opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	image_copy = img.copy()
	#print(len(contours[0]))
	#print('\n')
	#print(contours[0][7][0])

	# Para sacar solo las esquinas del contorno no el contorno entero
	"""
	for i in range(len(contours[0])):
	    x = contours[0][i][0][0]
	    y = contours[0][i][0][1]
	    #print(x,y)
	    cv2.circle(image_copy, (x,y), 3, (0,0,255), -1)
	    #cv2.drawContours(image_copy, [contours[i], [], (0,0,255), 6)
	    #cv2.drawContours(image_copy, [contours[i], 1, (0,0,255), 6)
	"""
	for i in contours:
	    M = cv2.moments(i)
	    if M['m00'] != 0:
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])
		cv2.drawContours(image_copy, [i], -1, (0, 255, 0), 2)
		cv2.circle(image_copy, (cx, cy), 4, (0, 0, 255), -1)

	cv2.imshow('Contornos', image_copy)
	masked = cv2.bitwise_and(img, img, mask=opened)

	cv2.imshow('Codigo aislado', masked)

	cv2.waitKey() 

	#############################################PROBAR cv2.ADAPTIVE_THRESH_GAUSSIAN_C#########################################################

if __name__ == "__main__":              
    funcion()






