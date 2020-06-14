import numpy as np
from scipy.fftpack import dct, idct


# Funcao para calcular o dct 2d
def DCT2D (arr):
    return dct(dct(arr.T, norm='ortho').T, norm='ortho')

# Funcao para calcular o idct 2d
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
    
    # Colocar os blocos verticalmente
    for i in range(length):
        # Colocar 8 blocos de oito horizontalmente
        for c in range(8):
            # 64 vezes
            for x in range(length):
                # [x+i*length] serve para saltar os de 64 em 64 pixels
                new_array.append(idcts[x+i*length][c])

    return np.array(new_array).reshape(512, 512)
