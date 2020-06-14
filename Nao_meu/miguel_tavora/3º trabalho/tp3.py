import cv2
import numpy as np
import matplotlib.pyplot as plt
import urllib
from scipy.fftpack import dct, idct
import tab_jpeg as tab

########################## EXERCICIO 1 ##########################
# Fazer o download do ficheiro da lena
def downloadImage():
    urllib.request.urlretrieve("https://homepages.cae.wisc.edu/~ece533/images/lena.bmp","lena.bmp")

image = cv2.imread('lena.bmp')
img_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
y, u, v = cv2.split(img_yuv)
cv2.imshow('image', y)
cv2.waitKey (0)
cv2.destroyAllWindows()
########################## EXERCICIO 2 ##########################

# Funcao para calcular o dct 2d
def DCT2D (arr):
    return dct(dct(arr.T, norm='ortho').T, norm='ortho')

# Funcao para calcular o idct 2d
def IDCT2D (arr):
    return idct(idct(arr.T, norm='ortho').T, norm='ortho')

########################## EXERCICIO 3 ##########################

def codificadorDCT (img):
    imagem = img.copy().astype('float64')
    for x in range (0, len(imagem), 8):
        for y in range (0, len(imagem[0]), 8):
            imagem[x:x+8, y:y+8] = DCT2D(imagem[x:x+8, y:y+8])
    return imagem

def descodificadorDCT (img):
    image = img.copy()
    for x in range (0, len(image), 8):
        for y in range (0, len(image[0]), 8):
            image[x:x+8, y:y+8] = IDCT2D (image[x:x+8, y:y+8])
    return image.astype('uint8')

########################## EXERCICIO 4 ##########################

def codificadorQuantificacao (dctMatrix, q):
    image = dctMatrix.copy()
    for x in range (0, len(image), 8):
        for y in range (0, len(image[0]), 8):
            image[x:x+8, y:y+8] = (np.divide(image[x:x+8, y:y+8], tab.Q)) * q
    return np.rint(image)

def descodificadorQuantificacao (arr):
    image = arr.copy()
    for x in range (0, len(image), 8):
        for y in range (0, len(image[0]), 8):
            image[x:x+8, y:y+8] = np.multiply(image[x:x+8, y:y+8], tab.Q)
    return image

########################## EXERCICIO 6 ##########################

def codificadorDC (arr):
    print(np.roll(arr, 1))

zigzag = [
            [0, 0],
            [0, 1], [1, 0],
            [2, 0], [1, 1], [0, 2],
            [0, 3], [1, 2], [2, 1], [3, 0],
            [4, 0], [3, 1], [2, 2], [1, 3], [0, 4],
            [0, 5], [1, 4], [2, 3], [3, 2], [4, 1], [5, 0],
            [6, 0], [5, 1], [4, 2], [3, 3], [2, 4], [1, 5], [0, 6],
            [0, 7], [1, 6], [2, 5], [3, 4], [4, 3], [5, 2], [6, 1], [7, 0],
            [7, 1], [6, 2], [5, 3], [4, 4], [3, 5], [2, 6], [1, 7],
            [2, 7], [3, 6], [4, 5], [5, 4], [6, 3], [7, 2],
            [7, 3], [6, 4], [5, 5], [4, 6], [3, 7],
            [4, 7], [5, 6], [6, 5], [7, 4],
            [7, 5], [6, 6], [5, 7],
            [6, 7], [7, 6],
            [7, 7] 
        ]

codificado = codificadorDCT (y)
quantificacao = codificadorQuantificacao (codificado, 1)
codificadorDC()