#!/usr/bin/env python2

import numpy as np
import cv2
import zbar
#from pyzbar import pyzbar


img = cv2.imread("/home/juan/Descargas/ean13.jpg") 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
"""
#Forma 1


gaus = cv2.GaussianBlur(gray,(5,5),0)
"""
grad_x = cv2.Sobel(gray, cv2.CV_16S, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
abs_grad_x = cv2.convertScaleAbs(grad_x)
"""
grad_y = cv2.Sobel(gray, cv2.CV_16S, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
abs_grad_y = cv2.convertScaleAbs(grad_y)

grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

cv2.imshow('original', img)
cv2.imshow('gray', grad)
cv2.waitKey() 
"""

#Forma 2
median = cv2.medianBlur(gray, 5)
#print("Tipo de median", type(median))
#print("Tipo de grad_x", type(grad_x))
th3 = cv2.adaptiveThreshold(median,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
cv2.imshow('original', img)
cv2.imshow('adaptativo', th3)
cv2.waitKey() 


