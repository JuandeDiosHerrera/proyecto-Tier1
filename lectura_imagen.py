#!/usr/bin/env python2
# coding=utf-8

import numpy as np
import cv2
import zbar
#from pyzbar import pyzbar


img = cv2.imread("/home/juan/Descargas/ean13.jpg") 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

"""
gaus = cv2.GaussianBlur(gray,(5,5),0)
"""
# Clculo gradientes y conversión a valores enteros positivos
grad_x = cv2.Sobel(gray, cv2.CV_16S, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
abs_grad_x = cv2.convertScaleAbs(grad_x)

grad_y = cv2.Sobel(gray, cv2.CV_16S, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
abs_grad_y = cv2.convertScaleAbs(grad_y)
"""
grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

cv2.imshow('original', img)
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
cv2.imshow('cierre', closed)

kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel1)
#opened = cv2.erode(closed, kernel2, iterations = 4)
#opened = cv2.dilate(closed, kernel2, iterations = 4)

cv2.imshow('apertura', opened)


# Se buscan los contornos del rectángulo y se pintan
contours, hierarchy = cv2.findContours(opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
image_copy = img.copy()
cv2.drawContours(image_copy, contours, 3, (0,0,255), 3)
cv2.imshow('Contornos', image_copy)

"""
cv2.imshow('binaria2', closed2)
cv2.drawContours(img, contours, 3, (0,255,0), 3)
kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 10))
closed2 = cv2.erode(closed1, kernel2, iterations = 3)
"""

cv2.waitKey() 










