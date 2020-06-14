import cv2
from Calculos import taxaCompressao, SNR, entropia, energia_media_pixel
from time import time
import matplotlib.pyplot as plt
import numpy as np


original_images = ["bola_1.tiff","bola_2.tiff","bola_3.tiff","bola_4.tiff","bola_5.tiff",
               "bola_6.tiff","bola_7.tiff","bola_8.tiff","bola_9.tiff","bola_10.tiff",
               "bola_11.tiff"]
coded_images = ["bola_1x.jpeg","bola_2x.jpeg","bola_3x.jpeg","bola_4x.jpeg","bola_5x.jpeg",
               "bola_6x.jpeg","bola_7x.jpeg","bola_8x.jpeg","bola_9x.jpeg","bola_10x.jpeg",
               "bola_11x.jpeg"]

if "__main__":
    array_taxas = []
    array_snr = []
    array_entro = []
    array_energias = []
    t0 = time()
    for i in range(len(original_images)):
        imagem_original = cv2.imread(original_images[i]) #open da imagem original
        imagem_lida = imagem_original.astype(float)
        # codifacao com fator 80
        cv2.imwrite("imgEx1/"+coded_images[i],imagem_original,(cv2.IMWRITE_JPEG_QUALITY,80))

        # --------------------------- calculos e prints ---------------------------
        taxa = taxaCompressao(original_images[i], coded_images[i])
        array_taxas.append(taxa)
        snr = SNR(original_images[i], coded_images[i])
        array_snr.append(snr)
        entro = entropia(original_images[i])
        array_entro.append(entro)
        energia = energia_media_pixel(original_images[i])
        array_energias.append(energia)

        print("\n -------------- FRAME ", i+1, " ---------------" )
        print("Taxa compressao: ", taxa)
        print("SNR da imagem: ", snr)
        print("Entropia: ", entro)
        print("Energia média p/ pixel: ", energia)

    t1 = time()
    print("\nTempo compressão/descompressão: ", t1-t0)




    # ------------------ Construcao dos graficos --------------------
    array_indices = [0,1,2,3,4,5,6,7,8,9,10]
    plt.xlabel('Frames')
    plt.ylabel('Taxa compressão')
    plt.title('Taxa de compressão em função das Frames')
    plt.plot(array_indices, array_taxas, marker='o', linewidth=2)
    plt.show()

    plt.xlabel('Frames')
    plt.ylabel('SNR')
    plt.title('SNR em função das Frames')
    plt.plot(array_indices, array_snr, marker='o', linewidth=2)
    plt.show()

    plt.xlabel('Frames')
    plt.ylabel('Entropia')
    plt.title('Entropia em função das Frames')
    plt.plot(array_indices, array_entro, marker='o', linewidth=2)
    plt.show()

    plt.xlabel('Frames')
    plt.ylabel('Energia')
    plt.title('Energia média por pixel em função das Frames')
    plt.plot(array_indices, array_energias, marker='o', linewidth=2)
    plt.show()
