import cv2
from matplotlib import pyplot as plt

 
bardet = cv2.barcode_BarcodeDetector()
img = cv2.imread("E:\\Documents\\Juan de Dios\\TFG\\foto.jpg")
ok, decoded_info, decoded_type, corners = bardet.detectAndDecode(img)

print(ok)
print('')
print('Decoded info:',decoded_info)
print('')
print('Decoded type:',decoded_type)
print('')
print('Corners:', corners)
print('')
