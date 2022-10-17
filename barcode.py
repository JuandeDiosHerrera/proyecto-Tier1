import cv2
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join
import numpy
 
bardet = cv2.barcode_BarcodeDetector()

mypath='C:\\Users\\joseh\\Documents\\Juan de Dios\\TFG\\Fotos'
#mypath='E:\\Documents\\Juan de Dios\\TFG\\Fotos'
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
images = numpy.empty(len(onlyfiles), dtype=object)
for n in range(0, len(onlyfiles)):
    images[n] = cv2.imread( join(mypath,onlyfiles[n]) )
    images[n] = cv2.cvtColor(images[n], cv2.COLOR_BGR2RGB)

    ok, decoded_info, decoded_type, corners = bardet.detectAndDecode(images[n])
   
    """
    plt.subplot(111),plt.imshow(images[n])
    plt.title('Image'), plt.xticks([]), plt.yticks([])
    plt.show()
    
    # Detección, códigos decodificados, tipos de códigos y esquinas de los códigos:
    print(ok)    
    print('Decoded info:',decoded_info)
    print('Decoded type:',decoded_type)
    print('Corners:', corners)
    print('')
    """

    img_copy = images[n].copy()
    #print(corners)
    if ok == False:
        print('Código de barra no detectado')

        plt.subplot(111),plt.imshow(images[n])
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        plt.show()

    else:
        for i in range(len(corners)):  
            for j in range(4):              
                x = corners[i][j][0]                #Desde esquina inferior izquierda en sentido horario
                y = corners[i][j][1]
                #print(x,y)
                cv2.circle(img_copy, (int(x),int(y)), 15, (255,0,0), -1)
        
        plt.subplot(121),plt.imshow(images[n])
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])

        plt.subplot(122),plt.imshow(img_copy)
        plt.title('Barcode detection'), plt.xticks([]), plt.yticks([])
        plt.show()
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


    
