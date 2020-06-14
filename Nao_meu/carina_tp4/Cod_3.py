import cv2
from Calculos import taxaCompressao, SNR, entropia, energia_media_pixel
from time import time
import matplotlib.pyplot as plt
import numpy as np



# define que pixeis podem ser incluidos na janela de pesquisa
# x e y são indices da imagem
def janela_pesquisa(x, y, size_x, size_y):
    '''
    :param x: primeiro indice em x do bloco (int)
    :param y: primeiro indice em y do bloco (int)
    :param size_x: largura da imagem = 352 (int)
    :param size_y: altura da imagem = 240 (int)
    :return: retorna as dimensoes mínimas e máximas
    da janela de pesquisa(em x e y) (int)
    '''

    x_min, x_max, y_min, y_max = 0, 0, 0, 0
    block_dim = 16 # dimensao dos blocos

    x_min = x - 15
    if x_min < 0: x_min = 0

    x_max = x + block_dim + 15
    if x_max > size_x: x_max = size_x

    y_min = y - 15
    if y_min < 0: y_min = 0

    y_max = y + block_dim + 15
    if y_max > size_y: y_max = size_y

    return x_min, x_max, y_min, y_max



def selecionar_pixels_janela_pesquisa(imagem, dimensoes):
    '''
    :param imagem: matriz de inteiros 2D
    :param dimensoes: tuplo com quatro posições(x_min, x_max, y_min, y_max)
    :return: os pixeis a considerar na janela de pesquisa
    '''

    x_min = dimensoes[0]
    x_max = dimensoes[1]
    y_min = dimensoes[2]
    y_max = dimensoes[3]

    janela_pesquisa = imagem[x_min : x_max + 1, y_min : y_max + 1]

    return janela_pesquisa


#a fazer a medição do erro absoluto médio entre dois blocos (tamanho 16 × 16)
def retornar_16x16(blocos, u, v):
    resultado = np.zeros((16,352)).astype("uint8") #preencher ate ultima coluna
    index =0
    linha = blocos[0]
    juntar = 0

    for n in range(15): #altura (240) a dividir pelo nr de blocos (16) = 15

        if index !=0 :
            linha = blocos[index]

        for i in range(index, 330): #total de blocos (352/16 * 240/16)
            index +=1
            if(index % 22 ==0 and index!=0): #22 = width da imagem/16

                break

            linha = np.concatenate((linha, blocos[index]), axis=1)


        if( juntar == 0):
            juntar += 1
            resultado[0:16] = linha
        else:
            resultado = np.concatenate((resultado, linha), axis=0)
    y = resultado.astype("uint8")
    x = cv2.merge((y, u, v))
    final = cv2.cvtColor(x , cv2.COLOR_YUV2RGB)

    gray = final.astype('float32')
    intensity_shift = -10
    gray += intensity_shift
    gray = np.clip(gray, 0, 255)
    gray = gray.astype('uint8')
    cv2.imwrite('imgEx3/estimar_movimento10.png', gray)

    return resultado


def divide_16x16(y):
    height = len(y)  # uma coluna - 512
    width = len(y[0])  # uma linha - 512
    array_16x16 = [np.zeros((16,16))] * int(width/16 * height/16)
    currY = 0
    index = 0
    for i in range(16, height + 1, 16):
        currX = 0
        for j in range(16, width + 1, 16):
            a = y[currY:i, currX:j]
            array_16x16[index] = a
            index +=1
            currX = j
        currY = i

    return np.array(array_16x16).astype(int)



def MAE(bloco_referencia, bloco):
    return np.sum(np.abs((bloco.astype("float") - bloco_referencia.astype("float"))))/256


def percorre_janela(arr, nr):
    height = len(arr)
    width = len(arr[0])
    array_2x2 = [np.zeros((nr,nr))] * int(height*width)

    index = 0
    varj = nr
    vari = nr
    for i in range(height):
        for j in range(width):

            varj = nr + j

            if vari > height or varj > width:
                   continue

            a = arr[i:i + nr, j: j + nr]
            if np.shape(a) == (nr,nr):
                   array_2x2[index] = a
                   index +=1

            if j == height - 1:
                   vari = nr + i

    return np.array(array_2x2[:index])




def comparar(Pframe, y):

    black = cv2.imread('black.png')
    yuv11 = cv2.cvtColor(black, cv2.COLOR_RGB2YUV)
    y11, u11, v11 = cv2.split(yuv11)
    novo = divide_16x16(y11)
    yy = 0
    for n in range(0, len(Pframe)):
        minimo = 3000
        bloco_p = Pframe[n]
        xx = n
        if n > 21:
            xx = 0
            yy +=1
        dimensoes = janela_pesquisa(xx, yy, 351, 239)
        window = selecionar_pixels_janela_pesquisa(y, dimensoes)
        blocoP = Pframe[n] #bloco 16x16
        array_blocos_janela = percorre_janela(window, 16)
        for i in range(len(array_blocos_janela)):
            bloco = array_blocos_janela[i]
            #print(bloco)
            mae = MAE(bloco, blocoP)
            if mae < minimo:
                minimo = mae
                bloco_p = bloco

        novo[n] = bloco_p
    retornar_16x16(novo, u11,v11)




if "__main__":
    Iframe = cv2.imread('bola_1.tiff')
    yuv = cv2.cvtColor(Iframe, cv2.COLOR_RGB2YUV)
    y, u, v = cv2.split(yuv)

    blocos = divide_16x16(y)

    img1 = cv2.imread('bola_11.tiff')
    yuv1 = cv2.cvtColor(img1, cv2.COLOR_RGB2YUV)
    y1, u1, v1 = cv2.split(yuv1)

    blocos1 = divide_16x16(y1)

    comparar(blocos1, y)

    sem_movimento = cv2.imread('imgEx3/estimar_movimento10.png').astype(float)
    diferenca = img1-sem_movimento


    gray = diferenca.astype('float32')
    intensity_shift = 17
    gray += intensity_shift
    gray = np.clip(gray, 0, 255)
    gray = gray.astype('uint8')


    cv2.imwrite('imgEx3/diferenca10.png', gray)

    img_diferenca = cv2.imread('imgEx3/diferenca10.png').astype(float)
    retornado = sem_movimento + img_diferenca

    cv2.imwrite('imgEx3/retornado10.png', retornado)




