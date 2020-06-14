import cv2
import numpy as np
import matplotlib.pyplot as plt
import urllib
from os import path
from time import time

from Transformada import codificadorDCT, descodificadorDCT
from Quantificacao import codificadorQuantificacao, descodificadorQuantificacao
from DC import codificadorDC, descodificadorDC
from AC import codificadorAC, descodificadorAC
from CodificacaoFinal import codificarImagem, descodificarImagem


def downloadImage():
    urllib.request.urlretrieve("https://homepages.cae.wisc.edu/~ece533/images/lena.bmp","lena.bmp")

x = cv2.imread("lena.bmp")

img_yuv = cv2.cvtColor(x, cv2.COLOR_BGR2YUV)
x, y, y1 = cv2.split(img_yuv)

qualidade = [10, 20, 30, 40, 50, 60, 70, 80, 90]
SNR_arr = []
taxas_arr = []
SNR_CV_arr = []
compressaoTds = []


def splitImage (x):
    dct_array = np.full((int(len(x) * len(x[0]) / 64), 64), 10, dtype='float32')
    
    array_To_DCT = np.zeros(64, dtype='float32')
    indice_bloco = 0
    indice_array = 0
    
    # Separar em blocos de 8x8
    for l in range(int(len(x)/8)):
        for c in range(int(len(x)/8)):
            for xx in range(8):
                for y in range(8):            
                    array_To_DCT[indice_bloco] = x[(l*8)+xx][(c*8)+y]
                    indice_bloco += 1
            
            dct_array[indice_array] = array_To_DCT
            indice_array += 1
            array_To_DCT = np.zeros(64, dtype='float32')
            indice_bloco = 0
    return dct_array

def CalcularSNR (pr, original):
	return (10 * np.log10 (np.sum(np.sum(np.power(pr.astype('float'),2)))/np.sum(np.sum(np.power((pr.astype('float')-original.astype('float')),2)))))

for q in qualidade:

    print ("Qualidade " + str(q))

    time1 = time()
    dct_array = splitImage(x)
    dct = codificadorDCT(dct_array)

    array = codificadorQuantificacao(dct, q)

    array_diferencial = codificadorDC(array)

    tuplos = codificadorAC(array_diferencial)

    codificarImagem(tuplos, str(q) + ".bin")
    sub1 = time() - time1
    print ("compressao " + str(sub1))

    time3 = time()
    i_huff = descodificarImagem(str(q) + ".bin")

    array_dif = descodificadorAC(i_huff)

    array_quant = descodificadorDC(array_dif)

    blocos = descodificadorQuantificacao(array_quant, q)

    idct = descodificadorDCT(blocos)
    sub2 = time() - time3
    print ("descompressao " + str(sub2))

    print ("tempo total " + str(sub1 + sub2))
    print ("")
    
    SNR = CalcularSNR (idct, x)
    print ("SNR " + str(SNR))

    size_ini = path.getsize("LenaGreyScale.bmp")
    size_end = path.getsize(str(q) + ".bin")
    taxa = 1.* size_ini / size_end
    print ("taxa: " + str(taxa))
    print ("")

    cv2.imwrite("Ouput" + str(q) + ".jpg", idct)

    SNR_arr.append(SNR)
    compressaoTds.append(taxa)

# Grafico SNR / Taxa
plt.plot(compressaoTds, SNR_arr, 'g')

plt.xlabel('Taxa de Compressao')
plt.ylabel('SNR')
plt.show()

# Grafico SNR / Qualidade
plt.plot(qualidade, SNR_arr)
plt.xlabel('Qualidade')
plt.ylabel("SNR")
plt.show()

# Grafico Taxa / Qualidade
plt.plot(qualidade, compressaoTds)
plt.xlabel('Qualidade')
plt.ylabel("Taxa de Compressao")