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

########################## EXERCICIO 5 ##########################

# Recebe um numero e retorna string codificada
def codificadorDC_bits (dc):
    textoFinal = ""
    if dc == 0:
           textoFinal += tab.K3[0]
    else:
        binario = np.binary_repr(dc.astype('int'))
        textoFinal += tab.K3[len(binario)]
        if dc < 0:
            novo = ""
            for char in binario:
                if char == "1":
                    novo += "0"
                else:
                    novo += "1"
            textoFinal += novo
        else:
            textoFinal += binario
    return textoFinal

# Recebe quantificacao e retorna array com DC's dos blocos
def codificadorDC_array (arr):
    image = arr.copy()
    dc = []
    anterior = 0
    for x in range (0, len(image), 8):
        for y in range (0, len(image), 8):
            if x == 0 and y == 0:
                anterior = image[x, y]
                dc.append(image[x, y])
            else:
                dc.append(image[x, y] - anterior)
                anterior = image[x, y]
    return dc

########################## EXERCICIO 6 ##########################

def codificadorBlocoAC (bloco):
    #print(bloco)
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
    
    zeros = 0
    cenas = []
    for i in range (8*8):
        x = zigzag[i][0]
        y = zigzag[i][1]
        if i != 0:
            if bloco[x, y] == 0:
                zeros += 1
            else:
                if zeros > 16:
                    while zeros > 16:
                        tt = (15, 0)
                        cenas.append(tt)
                        zeros -= 16
                tuplo = (zeros, np.abs(bloco[x, y]))
                zeros = 0
                cenas.append(tuplo)
                #print(tab.K5[zeros, len(np.binary_repr(np.abs(bloco[x, y]).astype('int')))])
        if i == len(zigzag)-1:
            tuplo0 = (0, 0)
            cenas.append(tuplo0)
    
    #print (cenas)
    return cenas



def codificadorAC (arr):
    image = arr.copy()
    a = []
    for x in range (0, len(image), 8):
        for y in range (0, len(image), 8):
            #print(codificadorBlocoAC (image[x:x+8, y:y+8]))
            a.append(codificadorBlocoAC (image[x:x+8, y:y+8]))
    k = []
    #print(a)
    for i in a:
        for j in i:
            if isinstance(j, tuple):
                k.append(j)
            
    return np.array(k)

################################################################
codificado = codificadorDCT (y)
#print(codificado)
quantificacao = codificadorQuantificacao (codificado, 1)
#print(quantificacao)
x = 0
y = 2   
#print(quantificacao[x:x+8, y:y+8])

codificadoDC = codificadorAC(quantificacao)
#print(codificadoDC)
#codificadoAC = codificadorAC (quantificacao)

#codificadorBlocoAC (quantificacao[x:x+8, y:y+8])