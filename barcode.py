import cv2
from matplotlib import pyplot as plt

 
bardet = cv2.barcode_BarcodeDetector()
img = cv2.imread("E:\\Documents\\Juan de Dios\\TFG\\foto.jpg")
ok, decoded_info, decoded_type, corners = bardet.detectAndDecode(img)
"""
cv2.imshow('Image', img)
cv2.waitKey()
"""

print(ok)
print('')
print('Decoded info:',decoded_info)
print('')
print('Decoded type:',decoded_type)
print('')
print('Corners:', corners)
print('')
#print(len(corners))

img_copy = img.copy()

for i in range(len(corners)):  
    for j in range(4):              
        x = corners[i][j][0]                #Desde esquina inferior izquierda en sentido horario
        y = corners[i][j][1]
        #print(x,y)
        cv2.circle(img_copy, (int(x),int(y)), 15, (255,0,0), -1)
    
plt.subplot(111),plt.imshow(img_copy)
plt.title('Image'), plt.xticks([]), plt.yticks([])
plt.show()