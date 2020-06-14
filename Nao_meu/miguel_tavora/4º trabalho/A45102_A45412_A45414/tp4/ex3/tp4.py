import numpy as np
import cv2

def erroAbsolutoMedio(a, b):
    l = len(a)
    c = len(a[0])
    return np.sum(np.abs(a.astype('float64') - b.astype('float64'))) / (l*c)


def escreverDiferencas (p_frame, predita, filename):
    elFinal = p_frame.astype('float64') - predita.astype('float64')
    elFinal += 128
    cv2.imwrite(filename, elFinal, (cv2.IMWRITE_JPEG_QUALITY,50))

def lerDiferencas (filename):
    elFinal = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    elFinal -= 128
    return elFinal


def fullSearch (bloco, iFrame, pos):
    
    minimo = 9999999
    posicao = blocoFinal = None
    
    for i in range(15 * 2 + 1):
        i += pos[0]
        if i > len(iFrame) - len(bloco):
            continue

        for j in range(15 * 2 + 1):
            j += pos[1]

            if j > len(iFrame[0]) - len(bloco):
                break

            blocoI = iFrame[i:i+len(bloco), j:j+len(bloco)]

            erro = erroAbsolutoMedio(blocoI, bloco)

            if erro < minimo:
                minimo = erro
                posicao = (i, j)
                blocoFinal = blocoI
    
    return posicao, blocoFinal


def predicao(pFrame, iFrame):
    
    p_frame = np.zeros_like(pFrame)
    l = 0
    c = 0
    vetores = []
    
    for x in range (int(len(pFrame) / 16)):
        for y in range (int(len(pFrame[0]) / 16)):
            
            bloco16x16 = pFrame[l: l + 16, c: c + 16]
            nPos, blocoSem = fullSearch(bloco16x16, iFrame, (l, c))
            
            # Calcular cada vetor de movimento
            vetor = (nPos[0] - l, nPos[1] - c)
            p_frame[l: l + 16, c: c + 16] = blocoSem
            vetores.append(vetor)
            c += 16
        l += 16
        c = 0
    
    return p_frame, vetores



def escreverPredita(i_frame, diferenca, vetores):
    
    l = c = vIndex = 0
    
    predita = np.zeros_like(i_frame)
    
    for x in range(int(len(i_frame) / 16)):
        for y in range(int(len(i_frame[0]) / 16)):
            
            posX = vetores[vIndex][0] + l
            posY = vetores[vIndex][1] + c
            
            predita[l: l + 16, c: c + 16] = \
                                i_frame[posX: posX + 16, posY: posY + 16]
            vIndex += 1
            c += 16
        l += 16
        c = 0
    elFinal = predita + diferenca
    return elFinal
    
