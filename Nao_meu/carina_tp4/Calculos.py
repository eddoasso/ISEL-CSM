import numpy as np
import cv2
import os

#recebe strings dos nomes
def SNR(original, descomprimida):
    imagem_original = cv2.imread(original)
    imagem_descomprimida = cv2.imread(descomprimida)
    parte1 = (np.sum(np.sum((imagem_descomprimida ** 2.0)) * 1.0))
    parte2 = (np.sum(np.sum(((imagem_descomprimida - imagem_original) ** 2) * 1.0 )))
    resultado = 0
    if(parte2 != 0):
        divisao = np.divide(parte1, parte2)
        resultado = 10 * np.log10(divisao)
    return abs(resultado)


#recebe strings dos nomes
def taxaCompressao(imagem_original, imagem_descomprimida): #bytes
    #tamanho_original = os.stat(imagem_original).st_size
    tamanho_original = (os.path.getsize(imagem_original))*1.0
    tamanho_novo = (os.path.getsize(imagem_descomprimida))*1.0
    return np.divide(tamanho_original, tamanho_novo)*1.0

#recebe string do nome do ficheiro original
def entropia(filename):
    file = open(filename, "r", encoding='ISO-8859-1')
    simbolos = list(file.read())
    unique, counts = np.unique(simbolos, return_counts=True)
    probs = counts/len(simbolos) #array probabilidade

    resultado = 0
    for i in range(len(probs)):
        resultado = resultado + (probs[i]*np.log2(probs[i])*1.0)

    return (-1.0)*resultado

#fazer soma de todos os pixeis ao quadrado e depois normalizar,
#ou seja(dividir pela quantidade total de pixeis)
#recebe string do nome do ficheiro original
def energia_media_pixel(filename):
    image = cv2.imread(filename)
    width = np.shape(image)[1]
    height = np.shape(image)[0]
    r, g, b = cv2.split(image)
    sR = [[int(elem) * int(elem) for elem in inner] for inner in r]
    sG = [[int(elem) * int(elem) for elem in inner] for inner in g]
    sB = [[int(elem) * int(elem) for elem in inner] for inner in b]
    energy = (np.sum(sR) + np.sum(sG) + np.sum(sB))*1.0 / (width * height)
    return energy*1.0

