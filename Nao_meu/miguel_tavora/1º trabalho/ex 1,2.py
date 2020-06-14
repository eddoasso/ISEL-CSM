import cv2
import numpy as np
import matplotlib.pyplot as plt

x_img = cv2.imread( "lenac.tif" ) #lê a imagem
cv2.imshow('Original Image' , x_img ) #mostra a imagem mas fecha logo

print (x_img.dtype) #imprime a imagem
print (x_img.shape)

cv2.waitKey ( 0 ) #espera que a janela seja fechada ate clicar na tecla
cv2.destroyAllWindows ( ) #fecha as imagens abertas

cv2.imwrite('file1.jpg' , x_img , (cv2.IMWRITE_JPEG_QUALITY,80)) #qualidade de 80%


x_img2 = cv2.imread("file1.jpg")
cv2.imshow('Original Image', x_img)

print (x_img.dtype)
print (x_img.shape)

#SNR2 = 10*np.log10(np.sum(np.sum(np.power(x_img2.astype('uint16')))/(np.sum(np.sum(np.power(x_img2-x_img.astype('uint16')))))) #np.sum faz o somatorio das coisas, tmb existe np.power()eleva ao quadrado

cv2.waitKey ( 0 )
cv2.destroyAllWindows ( )

cv2.imwrite('file2.jpg' , x_img , (cv2.IMWRITE_JPEG_QUALITY,10))

x_img3 = cv2.imread("file2.jpg")
cv2.imshow('Original Image', x_img)

print (x_img.dtype)
print (x_img.shape)

SNR3 = 10*np.log10(np.sum(np.sum(x_img3**2))/(np.sum(np.sum((x_img3-x_img)**2))))

cv2.waitKey ( 0 )
cv2.destroyAllWindows ( )


#SNR = 10*np.log10(np.sum(np.sum(x_img2**2))/(np.sum(np.sum(np.power(x_img2-x_img)))))

#print(SNR2)

#print(SNR3)