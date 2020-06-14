import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

########################################### Exercicio 1 ###########################################

x_img = cv2.imread('lenac.tif')
#cv2.imshow('Original Image', x_img)
print(x_img.dtype)
print(x_img.shape)
#cv2.waitKey (0)
#cv2.destroyAllWindows()


########################################### Exercicio 2 ###########################################
cv2.imwrite ('file1.jpg', x_img, (cv2.IMWRITE_JPEG_QUALITY, 80))
cv2.imwrite ('file2.jpg', x_img, (cv2.IMWRITE_JPEG_QUALITY, 10))

img80 = cv2.imread ('file1.jpg')
img10 = cv2.imread ('file2.jpg')

def SNR (pr, original):
	return (10 * np.log10 (np.sum(np.sum(np.power(pr.astype('float'),2)))/np.sum(np.sum(np.power((pr.astype('float')-original.astype('float')),2)))))

# Falta formula do PSNR
def PSNR (pr, original):
	MSE = np.mean( (pr - original) ** 2 )
	pixMAX = 255
	return 20*np.log10(pixMAX/np.sqrt(MSE))

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
	print("PSNR80: " + str(PSNR (img80, x_img)))
	print("PSNR10: " + str(PSNR (img10, x_img)))

ex2 ()

########################################### Exercicio 3 ###########################################

x_img_g = cv2.cvtColor(x_img , cv2.COLOR_BGR2GRAY)
cv2.imshow('Gray Image', x_img_g )
cv2.imwrite('file3.bmp', x_img_g )

cv2.waitKey (0)
cv2.destroyAllWindows()

########################################### Exercicio 4 ###########################################

def ex4 ():
	h = plt.hist (x_img_g.ravel(), 256, [0, 256])
	plt.show ()

	tons = np.sum(h[0] != 0)
	print("Diferentes tons de cinzento: "+ str(tons))
	print("Diferentes tons de cinzento (max): " + str(np.max(x_img_g.ravel())))
	print("Diferentes tons de cinzento (min): " + str(np.min(x_img_g.ravel())))

ex4()

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
	
ex5()


########################################### Exercicio 6 ###########################################

def ex6 ():
	y = x_img & 0b10000000
	cv2.imwrite ('lena_4.bmp', y)

ex6 ()

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
	cv2.imwrite('dither.jpg', dithered)
	return dithered

dithered = ex7 ()
########################################### Exercicio 8 ###########################################

def ex8 (pic):
	size = os.stat('dither.jpg').st_size
	ret,x_img= cv2.threshold(pic, 127, 255, cv2.THRESH_BINARY)
	count=0
	leFinal=[]
	ajuda=[]
	for i in range(len(x_img)):
		for j in range(len(x_img[0])):
			if(x_img[i][j]==255):
				ajuda.append(1)
			else:
				ajuda.append(0)
			count+=1
			if(count==8):
				leFinal.append(np.packbits(ajuda))
				ajuda.clear()
				count=1
	leFinal = np.array(leFinal)
	leFinal.tofile('file.bin')
	size1 = os.stat('file.bin').st_size
	print ("Taxa de Compressao: " + str(100-(size1/size)*100))

ex8 (dithered)

########################################### Exercicio 9 ###########################################

def fazer (dimX, dimY, ang, angB, angD, g, d=False):
	if (np.rad2deg(ang) >= 0):
		print("\nAngulo Delta: " + str(np.rad2deg(angD)))
		print("Angulo: " + str(np.rad2deg(ang)))
		print("Angulo Anterior: " + str(np.rad2deg(angB)))

		for i in range (int(dimX/2) + 1):
			for j in range (int(dimY/2) + 1):
				r = np.sqrt(i**2 + j**2)
				if (int(np.round(r*np.cos(ang))) >= i and int(np.round(r*np.sin(ang))) <= j):
					if (int(np.round(r*np.cos(angB))) <= i and int(np.round(r*np.sin(angB))) >= j):
						g[i][j]=0
					else:
						if (d):
							g[i][j]=255
				else:
					if (d):
						g[i][j]=255
		
		print("Angulo Seguinte: " + str(np.rad2deg(ang)-2*np.rad2deg(angD)))
		g = np.array(g)
		return fazer (dimX, dimY, ang-2*angD, angB-2*angD, angD, g)
	
	return g

def appendVertically (g2, g, dimY):
	k = []
	for i in range (int(dimY)):
		if (i < int(dimY/2)):
			k.append(g2[i])
		else:
			k.append(g[i-int(dimY/2)])
	return np.array(k)

def appendHorizontally (k, q, dimX):
	leFinal = []
	for i in range (dimX):
		leFinal.append([])
		for j in range (dimX):
			if (j < int(dimX/2)):
				#print("i: " + str(i) + " j: " + str(j))
				leFinal[i].append(q[i][j])
			else:
				leFinal[i].append(k[i][j-int(dimX/2)])

	return np.array(leFinal)


def ex9 (ang1):
	ang = np.deg2rad(90-ang1)
	angD = np.deg2rad(ang1)
	angB = np.deg2rad(90)

	dimX = dimY = 500

	# Preencher a imagem
	g=[]
	for i in range (int(dimX/2) + 1):
		g.append([])
		for j in range (int(dimY/2) + 1):
			g[i].append(0)

	# Criar todos os quadrantes
	g = fazer (dimX, dimY, ang, angB, angD, g, True)
	g2 = np.rot90(g)
	g3 = np.rot90(g, 2)
	g4 = np.rot90(g, 3)
	
	# Juntar os quandrantes numa imagem
	k = appendVertically (g2, g, dimY)
	q = appendVertically (g3, g4, dimY)
	leFinal = appendHorizontally (k, q, dimX)

	cv2.imshow('ex9', leFinal.astype('uint8'))
	cv2.waitKey (0)
	cv2.destroyAllWindows ()

ex9 (5)