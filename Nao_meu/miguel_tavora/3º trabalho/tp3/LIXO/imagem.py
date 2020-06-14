from TP2 import gera_huffman
from TP2 import codifica
from TP2 import descodifica
from TP2 import escrever
from TP2 import ler

import numpy as np
from time import time
from os import path
import cv2
import matplotlib.pyplot as plt


# Lê e mostra a imagem em níveis de cinzento
x = cv2.imread("lena.bmp",cv2.IMREAD_GRAYSCALE)
cv2.imshow("Imagem Original", x)

# Converte a imagem (matriz) numa sequência de números (array)
xi = x.ravel()

# Calcula o histogram
h, bins, patches = plt.hist(xi, 256, [0,256])

# Gera o código de Huffman
t0 = time()
tabela_codigo = gera_huffman(np.arange(0,256),h)
t1 = time()
print("Tempo que demora a gerar huffman: " + str(t1-t0))
print()


# Calcular a entropia da fonte H(s)
entropia = 0
for x in h:
    p = x / np.sum(h)
    if(p == 0):
        pp = 0

    else:
        pp= float(p * np.log2(p))
        
    entropia += pp

print("Entropia: " + str(-entropia))
print()


# Calcular o número médio de bits por símbolo


# Calcular a eficiência


# Codifica o ficheiro
t2 = time()
seq_bit0 = codifica(xi,tabela_codigo)
t3 = time()
print("Tempo que demora a codificar: " + str(t3-t2))
print()


# Gravar o ficheiro
escrever(seq_bit0, "imagem.txt")
size = path.getsize("imagem.txt")
print("Tamanho do ficheiro: " + str(size))
print()


# Lê ficheiro
seq_bit1 = ler("imagem.txt")


# Descodifica o ficheiro
t4 = time()
yi = descodifica(seq_bit1,tabela_codigo)
t5 = time()
print("Tempo que demora a descodificar: " + str(t5-t4))


plt.show()
cv2.waitKey(0)
plt.close("all")
cv2.destroyAllWindows()
