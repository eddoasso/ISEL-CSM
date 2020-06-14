import cv2
import numpy as np
import matplotlib.pyplot as plt
import urllib
from os import path
from time import time
from PIL import Image

from Transformada import codificadorDCT, descodificadorDCT
from Quantificacao import codificadorQuantificacao, descodificadorQuantificacao
from DC import codificadorDC, descodificadorDC
from AC import codificadorAC, descodificadorAC
from CodificacaoFinal import codificarImagem, descodificarImagem


def downloadImage():
    urllib.request.urlretrieve("https://homepages.cae.wisc.edu/~ece533/images/lena.bmp","lena.bmp")

imagemPIL = Image.open("LenaGreyScale.bmp")
x = cv2.imread("lena.bmp")

img_yuv = cv2.cvtColor(x, cv2.COLOR_BGR2YUV)
x, y, y1 = cv2.split(img_yuv)

qualidade = [10, 20, 30, 40, 50, 60, 70, 80, 90]
SNRs = []
compressões = []
SNRsPIL = []
compressõesPIL = []


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
    print("############################## QUALIDADE", q,"##############################")
    #print ("Qualidade " + str(q))

    time1 = time()
    arr = splitImage(x)
    dct = codificadorDCT(arr)
    array = codificadorQuantificacao(dct, q)
    array_diferencial = codificadorDC(array)
    tuplos = codificadorAC(array_diferencial)
    codificarImagem(tuplos, str(q) + ".bin")
    tempoC = time() - time1
    print ("Tempo de Compressão:", tempoC)
    
    time3 = time()
    i_huff = descodificarImagem(str(q) + ".bin")
    array_dif = descodificadorAC(i_huff)
    array_quant = descodificadorDC(array_dif)
    blocos = descodificadorQuantificacao(array_quant, q)

    idct = descodificadorDCT(blocos)
    tempoD = time() - time3
    print ("Tempo de Descompressão:", tempoD)
    print ("Tempo de Compressão e Descompressão:", (tempoC + tempoD))
    
    SNR = CalcularSNR (idct, x)
    print ("SNR:", SNR)
    original = path.getsize("LenaGreyScale.bmp")
    final = path.getsize(str(q) + ".bin")
    taxa = original/final
    print ("Taxa de compressão:", taxa)
    cv2.imwrite("Output" + str(q) + ".jpg", idct)
    
    imagemPIL.save(("OutputPIL" + str(q) + ".jpeg"), "JPEG", quality=q)
    finalPIL = path.getsize(("OutputPIL" + str(q) + ".jpeg"))
    taxaPIL = original/finalPIL
    
    pil = cv2.imread(("OutputPIL" + str(q) + ".jpeg"))
    orig = cv2.imread("LenaGreyScale.bmp")
    SNRPIL = CalcularSNR (pil, orig)
    
    SNRs.append(SNR)
    compressões.append(taxa)
    
    SNRsPIL.append(SNRPIL)
    compressõesPIL.append(taxaPIL)

# Grafico SNR / Taxa
plt.plot(SNRs, compressões, 'b')
plt.plot(SNRsPIL, compressõesPIL, 'g')

plt.xlabel('SNR')
plt.ylabel('Taxa de Compressão')
plt.savefig('Grafico.png')
plt.show()