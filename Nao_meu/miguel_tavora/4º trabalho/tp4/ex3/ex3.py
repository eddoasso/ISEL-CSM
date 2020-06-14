from tp4 import escreverDiferencas, lerDiferencas, predicao, escreverPredita

import cv2
from time import time
from os import path
import numpy as np
import matplotlib.pyplot as plt

def CalcularSNR (pr, original):
	return (10 * np.log10 (np.sum(np.sum(np.power(pr.astype('float'),2)))/np.sum(np.sum(np.power((pr.astype('float')-original.astype('float')),2)))))

def ex3(obj):
    ex = None
    if obj == "bola":
        ex = ".tiff"
    else:
        ex = ".bmp"
    
    frames = []
    compressao = []
    descompressao = []
    taxasdeCompressao = []
    SNRs = []
    
    imagens = []
    for x in range(11):
       imagens.append(cv2.imread("../" + obj + "/" + obj + "_"+ str(x+1) + ex, cv2.IMREAD_GRAYSCALE))
    
    iFrame = imagens.pop(0)
    
    cv2.imwrite("i_frame" + obj + ".jpeg", iFrame, (cv2.IMWRITE_JPEG_QUALITY,50))
    iFrame = cv2.imread("i_frame" + obj + ".jpeg", cv2.IMREAD_GRAYSCALE)
    
    for i in range (len(imagens)):
        
        print ("#####################" , (i + 1), "#####################")
        frames.append(i + 1)
        
        time1 = time()
        frame_predita, vetor_mov = predicao(imagens[i], iFrame)
        cv2.imwrite("predicao/" + obj + "/predita" + str(i + 1) + ".jpeg", frame_predita)
        
        file = "diferencas/" + obj + "/diferenca" + str(i) + ".jpeg"
        escreverDiferencas (imagens[i], frame_predita, file)
        tempo = time() - time1
        print ("Tempo de Compressão:", tempo)
        compressao.append(tempo)
        
        
        time2 = time()
        frame_dif = lerDiferencas(file)
        
        frame_p = escreverPredita(iFrame, frame_dif, vetor_mov)
        cv2.imwrite("descodificados/" + obj + "/p_frame" + str(i + 1) + ".jpeg", frame_p, (cv2.IMWRITE_JPEG_QUALITY,50))
        tempo = time() - time2
        print ("Tempo de Descompressão:", tempo)
        descompressao.append(tempo)
        
        original = path.getsize("../" + obj + "/" + obj + "_" + str(i + 2) + ex)
        final = path.getsize("descodificados/" + obj + "/p_frame" + str(i + 1) + ".jpeg")      
        taxa = original*1. / final*1.
        print ("Taxa de Compressão:", taxa)   
        taxasdeCompressao.append(taxa)
        
        original = cv2.imread("../" + obj + "/" + obj + "_" + str(i + 2) + ex, cv2.IMREAD_GRAYSCALE)
        final = cv2.imread("descodificados/" + obj + "/p_frame" + str(i + 1) + ".jpeg", cv2.IMREAD_GRAYSCALE)
        
        SNR = CalcularSNR(final, original)
        
        print ("SNR:", SNR) 
        SNRs.append(SNR)

    plt.plot(frames, taxasdeCompressao)
    plt.xlabel("pFrames")
    plt.ylabel("Taxa de Compressao")
    plt.savefig("graficos/" + obj + "/Taxa de Compressão")
    plt.show()
    plt.close()
        
    plt.plot(frames, SNRs)
    plt.xlabel("pFrames")
    plt.ylabel("SNR")
    plt.savefig("graficos/" + obj + "/SNR")
    plt.show()
    plt.close()
    
    plt.plot(frames, compressao)
    plt.xlabel("pFrames")
    plt.ylabel("Tempo de Compressão")
    plt.savefig("graficos/" + obj + "/Tempo de Compressão") 
    plt.show()
    plt.close()
    
    plt.plot(frames, descompressao)
    plt.xlabel("pFrames")
    plt.ylabel("Tempo de Descompressão")
    plt.savefig("graficos/" + obj + "/Tempo de descompressão") 
    plt.show()
    plt.close()

ex3("bola")
