import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from time import time
import urllib
from scipy.fftpack import dct, idct


def codificarImagem (lista, filename):
    
    bits = []
    for valor in lista:
        if isinstance(valor, tuple):
            if (valor[0] == 0 and valor[1] == 0):
                bits.append('1010')
            else:
                if valor[1] > 0:
                    val = valor[0]
                    binario = bin(valor[1])[2:]
                    size = len(binario)
                elif valor[1] < 0:
                    val = valor[0]
                    binario_aux = bin(valor[1])[3:]
                    binario = ''.join('1' if i == '0' else '0' for i in binario_aux)
                    size = len(binario)
                else:
                    val = valor[0]
                    size = 0
                    binario = ""
                
                bits.append(K5[(val, size)])
                bits.append(binario)
        else:
            if valor > 0:
                a = bin(valor)[2:]
                size = K3[len(a)]
            elif valor < 0:
                bin_aux = bin(valor)[3:]
                a = ''.join('1' if i == '0' else '0' for i in bin_aux)
                size = K3[len(a)]
            else:
                size = K3[valor]
                a = ""
            
            bits.append(size)
            bits.append(a)
    
    mensagem = ''.join(bits)
    escreverFicheiro(mensagem, filename)
    return mensagem

x_img = cv2.imread("bola_0x.tiff")
cv2.imwrite("bola_0x.jpeg",x_img,(cv2.IMWRITE_JPEG_QUALITY,50))
