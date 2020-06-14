import numpy as np
import cv2


lenImagens = 11
imagens = []
for i in range (lenImagens):
   imagens.append(cv2.imread("../bola/bola_"+ str(i+1)+".tiff", cv2.IMREAD_GRAYSCALE))

def codifica (arr):
    imagens = arr.copy()
    iFrame = None
    for i in range (len (imagens)):
        if i != 0:
            cv2.imwrite("codificado/pFrame_" + str(i) + ".jpeg", imagens[i], (cv2.IMWRITE_JPEG_QUALITY,50))
            pFrame = cv2.imread("codificado/pFrame_" + str(i) + ".jpeg", cv2.IMREAD_GRAYSCALE)

            pFrame = pFrame.astype('float64')
            final = pFrame - iFrame
            
            final += 128
            
            cv2.imwrite("codificado/pFrame_" + str(i) + ".jpeg", final)
        else:
            cv2.imwrite("codificado/pFrame_" + str(i) + ".jpeg", imagens[i], (cv2.IMWRITE_JPEG_QUALITY,50))
            iFrame = cv2.imread("codificado/pFrame_" + str(i) + ".jpeg", cv2.IMREAD_GRAYSCALE)
            iFrame = iFrame.astype('float64')



def descodificador_ex2(): 
    elFinal = []

    for i in range(11):

        elFinal.append(cv2.imread("codificado/pFrame_" + str(i) + ".jpeg", cv2.IMREAD_GRAYSCALE))

        if i == 0:
            imagem_inicial = elFinal[i].astype('float64')
            cv2.imwrite("descodificado/pFrame_"+str(i)+ ".jpeg", imagem_inicial)

        else:
            valor = np.array(elFinal[i], np.float64) 
            
            valor -= 128
            valor += imagem_inicial
            
            


            valor = np.array(valor, np.uint8)
            cv2.imwrite("descodificado/pFrame_" + str(i) + ".jpeg", valor)

codifica (imagens)
descodificador_ex2()
