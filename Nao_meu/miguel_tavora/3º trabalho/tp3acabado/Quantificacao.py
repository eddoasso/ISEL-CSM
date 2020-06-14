from tab_jpeg import Q
import numpy as np

def codificadorQuantificacao (arr, q):
    
    imagem = arr.copy()
    
    for i in range(len(imagem)):
        imagem[i] = np.divide(imagem[i], (Q * fatorQualidade(q)))
        
    return np.rint(imagem)


def descodificadorQuantificacao (arr, q):
    
    imagem = arr.copy()
    
    for i in range(len(imagem)):
        imagem[i] = np.multiply(imagem[i], (Q * fatorQualidade(q)))
    
    return imagem

def fatorQualidade (q):
    if(q <= 50):
        a = 50.0 / q
    else:
        a = 2.0 - (q * 2.0)/100.0
    return a 