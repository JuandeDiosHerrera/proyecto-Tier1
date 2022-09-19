import cv2
 
bardet = cv2.barcode_BarcodeDetector()
img = cv2.imread("E:\\Documents\\Juan de Dios\\TFG\\foto.jpg")
ok, decoded_info, decoded_type, corners = bardet.detectAndDecode(img)