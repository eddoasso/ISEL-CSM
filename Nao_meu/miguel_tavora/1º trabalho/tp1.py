import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

########################################### Exercicio 1 ###########################################

x_img = cv2.imread('lenac.tif')
#cv2.imshow('Original Image', x_img)

#cv2.waitKey (0)
#cv2.destroyAllWindows()

cv2.imwrite ('file1.jpg', x_img, (cv2.IMWRITE_JPEG_QUALITY, 80))
cv2.imwrite ('file2.jpg', x_img, (cv2.IMWRITE_JPEG_QUALITY, 10))

img80 = cv2.imread ('file1.jpg')
img10 = cv2.imread ('file2.jpg')


########################################### Exercicio 2 ###########################################
def SNR (pr, original):
	return (10 * np.log10 (np.sum(np.sum(np.power(pr.astype('float'),2)))/np.sum(np.sum(np.power((pr.astype('float')-original.astype('float')),2)))))

def PSNR (pr, original):
	return (10 * np.log10 (np.sum(np.sum(np.power(pr.astype('float'),2)))/np.sum(np.sum(np.power((pr.astype('float')-original.astype('float')),2)))))

def taxaCompressao ():
	original = os.stat('lenac.tif').st_size
	file1 = os.stat('file1.jpg').st_size
	file2 = os.stat('file2.jpg').st_size
	print("Taxa de Compressao(file1.jpg): " + str(100-(file1/original)*100))
	print("Taxa de Compressao(file2.jpg): " + str(100-(file2/original)*100))

def ex2 ():
	taxaCompressao()

	print("SNR80: " + str(SNR (img80, x_img)))
	print("SNR10: " + str(SNR (img10, x_img)))

ex2 ()

########################################### Exercicio 3 ###########################################

x_img_g = cv2.cvtColor(x_img , cv2.COLOR_BGR2GRAY)
cv2.imshow('Gray Image', x_img_g )
cv2.imwrite('file3.bmp', x_img_g )

cv2.waitKey (0)
cv2.destroyAllWindows()

########################################### Exercicio 4 ###########################################

def ex4 ():
	plt.hist (x_img_g.ravel(), 256, [0, 256])
	plt.show ()

	tons = np.sum(x_img_g != 0)
	print("Diferentes tons de cinzento (max): " + str(np.max(x_img_g.ravel())))
	print("Diferentes tons de cinzento (min): " + str(np.min(x_img_g.ravel())))

#ex4()

########################################### Exercicio 5 ###########################################

def ex5 ():
	bitsamais = 128
	ajuda = 7
	for i in range(8):
		ajuda -= 1
		nmr = 2**ajuda
		y = x_img_g - bitsamais > nmr;
		bitsamais += nmr
		cv2.imshow ('BW', (y*255).astype('uint8'))
		cv2.waitKey (0)
		cv2.destroyAllWindows ()
#ex5()

########################################### Exercicio 6 ###########################################

def ex6 ():
	y = x_img & 0b10000000
	cv2.imwrite ('lena_4.bmp', y)

#ex6 ()

########################################### Exercicio 7 ###########################################

def dither(pixel):
	height,width = np.shape(pixel)    
	for y in range(height):
		for x in range(width):
			oldpixel = pixel[x][y]
			newpixel = 255 if oldpixel > 127 else 0
			pixel[x][y] = newpixel
			error = oldpixel - newpixel
			if(x < len(pixel) - 1):
				pixel[x + 1][y] = pixel[x + 1][y] + (error * (7 / 16))
			if(x > 0 and y < len(pixel) - 1):
				pixel[x - 1][y + 1] = pixel[x - 1][y + 1] + (error * (3 / 16))
			if(y < len(pixel[x]) - 1):
				pixel[x][y + 1] = pixel[x][y + 1] + (error * (5 / 16))
			if(x < len(pixel) - 1 and y < len(pixel[x]) - 1):
				pixel[(x + 1)][(y + 1)] = pixel[(x + 1)][(y + 1)] + (error * (1 / 16))
	return pixel

def ex7 ():
	dithered = dither (x_img_g)
	cv2.imshow('Dithered', dithered)
	cv2.waitKey (0)
	cv2.destroyAllWindows ()

ex7 ()

########################################### Exercicio 8 ###########################################

