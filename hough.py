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
	cv2.imshow('edges', edges)
	
        lines = cv2.HoughLinesP(edges, 0.8, np.pi / 180, 90, minLineLength=100, maxLineGap=10) # Hough Lines Transform
	
	edges_copy = edges.copy()

	# Draw the lines
    	if lines is not None:
		#cv2.LineSegmentDetector.drawSegments(edges_copy, lines)

		for i in range(0, len(lines)):
		    rho = lines[i][0][0]
		    theta = lines[i][0][1]
		    a = math.cos(theta)
		    b = math.sin(theta)
		    x0 = a * rho
		    y0 = b * rho
		    pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
		    pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
		    cv2.line(edges_copy, pt1, pt2, (0,0,255), 3, cv2.CV_AA)

	cv2.imshow('lines', edges_copy)
	cv2.waitKey() 

	#############################################PROBAR cv2.ADAPTIVE_THRESH_GAUSSIAN_C#########################################################

if __name__ == "__main__":              
    funcion()

