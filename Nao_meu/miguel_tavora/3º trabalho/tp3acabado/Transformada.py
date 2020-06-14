import numpy as np
from scipy.fftpack import dct, idct


def DCT2D (arr):
    return dct(dct(arr.T, norm='ortho').T, norm='ortho')

def IDCT2D (arr):
    return idct(idct(arr.T, norm='ortho').T, norm='ortho')

def codificadorDCT(dct_array):
    dcts = []
    
    for bloco in dct_array:
        bloco8x8 = bloco.reshape(int(len(bloco)/8), 8)
        dcts.append(DCT2D(bloco8x8))
    return np.rint(dcts)
        
def descodificadorDCT(dct_values):
    
    idcts = []
    for bloco in dct_values:
        idcts.append(IDCT2D(bloco))
    
    idcts = np.rint(idcts)
    length = 64
    new_array =[]
    
    for i in range(length):
        for c in range(8):
            for x in range(length):
                new_array.append(idcts[x+i*length][c])

    return np.array(new_array).reshape(512, 512)
