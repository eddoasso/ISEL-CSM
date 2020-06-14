import cv2
from Calculos import taxaCompressao, SNR, entropia, energia_media_pixel
from time import time
import matplotlib.pyplot as plt
import numpy as np


original_images = ["bola_1.tiff","bola_2.tiff","bola_3.tiff","bola_4.tiff","bola_5.tiff",
               "bola_6.tiff","bola_7.tiff","bola_8.tiff","bola_9.tiff","bola_10.tiff",
               "bola_11.tiff"]
coded_images = ["bola_1x.jpeg","bola_2xx.jpeg","bola_3xx.jpeg","bola_4xx.jpeg","bola_5xx.jpeg",
               "bola_6xx.jpeg","bola_7xx.jpeg","bola_8xx.jpeg","bola_9xx.jpeg","bola_10xx.jpeg",
               "bola_11xx.jpeg"]



if "__main__":
    Iframe = cv2.imread(original_images[0])
    cv2.imwrite(coded_images[0], Iframe, (cv2.IMWRITE_JPEG_QUALITY, 80))
    array_taxas = []
    array_taxas.append(taxaCompressao(original_images[0], coded_images[0]))
    array_snr = []
    array_snr.append(SNR(original_images[0], coded_images[0]))
    array_entro = []
    array_entro.append(entropia(original_images[0]))
    array_energias = []
    array_energias.append(energia_media_pixel(original_images[0]))
    t0 = time()

    for i in range(1, len(original_images)):
        imagem_lida = cv2.imread(original_images[i])
        imagem_lida = imagem_lida.astype(float)
        subtracao = (imagem_lida - Iframe)
        cv2.imwrite("imgEx2/"+coded_images[i],subtracao,(cv2.IMWRITE_JPEG_QUALITY,80))

        # --------------------------- calculos e prints ---------------------------
        taxa = taxaCompressao(original_images[i], "imgEx2/"+coded_images[i])
        array_taxas.append(taxa)
        snr = SNR(original_images[i], "imgEx2/"+coded_images[i])
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
