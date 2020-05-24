import cv2
import numpy as np


#Tabelas dadas no enunciado
Q = np.zeros((8, 8))
Q[0] = [ 16,  11,  10,  16,  24,  40,  51,  61]
Q[1] = [ 12,  12,  14,  19,  26,  58,  60,  55]
Q[2] = [ 14,  13,  16,  24,  40,  57,  69,  56]
Q[3] = [ 14,  17,  22,  29,  51,  87,  80,  62]
Q[4] = [ 18,  22,  37,  56,  68, 109, 103,  77]
Q[5] = [ 24,  35,  55,  64,  81, 104, 113,  92]
Q[6] = [ 49,  64,  78,  87, 103, 121, 120, 101]
Q[7] = [ 72,  92,  95,  98, 112, 100, 103,  99]

zigzag = np.zeros((8, 8))
zigzag[0] = [ 0,  1,  5,  6, 14, 15, 27, 28]
zigzag[1] = [ 2,  4,  7, 13, 16, 26, 29, 42]
zigzag[2] = [ 3,  8, 12, 17, 25, 30, 41, 43]
zigzag[3] = [ 9, 11, 18, 24, 31, 40, 44, 53]
zigzag[4] = [10, 19, 23, 32, 39, 45, 52, 54]
zigzag[5] = [20, 22, 33, 38, 46, 51, 55, 60]
zigzag[6] = [21, 34, 37, 47, 50, 56, 59, 61]
zigzag[7] = [35, 36, 48, 49, 57, 58, 62, 63]
ind_zz = zigzag.reshape((64),order='F').astype('int16')

def quality_factor(q):
    if(q <= 50):
        factor = 50.0 / q
    else:
        factor = 2.0 - (q * 2.0)/100.0
    return factor

#----------------------------------------------

#Funções auxiliares----------------------------

#Como o valor rgb é igual para r,g e b, por ser cinzento
#converteu-se a array de [[13,13,13],[50,50,50],...] para
#[13,50,...]
def convert(array):
    arrayOutput = np.zeros(int(len(array)/3))
    if(len(arrayOutput)<64):
        raise ValueError('Array te menos que 64 elementos.')
        
    idx = 0
    for i in range(0,len(array), 3):
        arrayOutput[idx] = array[i]
        idx += 1



    if(len(arrayOutput)%8 != 0):
        remove_num = len(arrayOutput)%8
        arrayOutput = arrayOutput[:-remove_num]

    return arrayOutput.astype(np.uint8)-128

def SNR(imgAmostrada,imgOriginal):
    try:
        k = np.sum(np.sum((imgAmostrada*1.0)**2))/(np.sum(np.sum(((imgAmostrada*1.0)-(imgOriginal*1.0))**2)))
        return 10*np.log10(k)
    except ZeroDivisionError:
        return "Infinito, ficheiro recebido igual ao emitido"

#Guarda a imagem no formato (numero_quadrados)*8*8
#retorna uma array de 3 dimensoes [[8x8], [8x8],...]
def convertTo8x8(array):

    #Só são aceites imagens com quadrados 1, 2x2, 3x3, 4x4...
    num_squares = np.power(int(np.sqrt(len(array))/8), 2)

    print(num_squares)
    array_8x8 = np.zeros((num_squares, 8, 8))

    num_elements = array_8x8.shape[0]*array_8x8.shape[1]*array_8x8.shape[2]

    z = 0
    y = 0
    idx = 0
    width = np.sqrt(num_squares)
    line = 0
    while(idx < num_elements):

        for x in range(8):
            array_8x8[z, y, x] = array[idx]
            idx += 1

        z += 1

        if(z%width==0):
            if(y==7):
                y = 0
                line = z
            else:
                z = line
                y += 1

    return array_8x8.astype(int)

def convertFrom8x8(array_8x8):

    num_elements = array_8x8.shape[0] * array_8x8.shape[1] * array_8x8.shape[2]*3 # array 3D

    img_array = np.zeros(num_elements)


    z = 0
    y = 0
    idx = 0
    width = np.sqrt(array_8x8.shape[0])
    line = 0
    while (idx < num_elements):

        for x in range(8):
            for i in range(3):
                img_array[idx] = array_8x8[z, y, x]
                idx += 1

        z += 1

        if (z % width == 0):
            if (y == 7):
                y = 0
                line = z
            else:
                z = line
                y += 1

    return img_array.astype(int)

def join_DC_AC(arrayDC, arrayAC8x8):
    arrayOutput = arrayAC8x8

    for i in range(len(arrayDC)):
        arrayOutput[i][0][0] = arrayDC[i]

    return arrayOutput

def save_image_toFile(img_array_jpg):
    imgWidth = int(np.sqrt(len(img_array_jpg) / 3))
    img_array_jpg = img_array_jpg.reshape(imgWidth, imgWidth, 3)

    imgname = "LenaGrayJPG" + str(QUALITY) + ".jpg"
    cv2.imwrite(imgname, img_array_jpg)




#Ex1-------------------------------------------
def encodeDCT(array8x8):
    arr_dct = np.zeros(array8x8.shape)

    for i in range(len(array8x8)):
        arr_dct[i] = cv2.dct(np.float32(array8x8[i]))

    return np.rint(arr_dct).astype(int)

def decodeDCT(arr_dct):
    arr_dct_decoded = np.zeros(arr_dct.shape)

    for i in range(len(arr_dct)):
        arr_dct_decoded[i] = cv2.dct(np.float32(arr_dct[i]),arr_dct_decoded, cv2.DCT_INVERSE)

    return np.rint(arr_dct_decoded).astype(int)+128

#Ex2----------------------------------------------
def encode_quantizeDCT(arr_dct_encoded):
    return np.rint(arr_dct_encoded/Q).astype(int)

def decode_quantizeDCT(arr_dct_quantized):
    return np.rint(arr_dct_quantized * Q).astype(int)

#Ex3----------------------------------------------
def encode_DC(arr_dct_quantized):
    arrayDC = np.zeros(len(arr_dct_quantized))

    arrayDC[0] = int(arr_dct_quantized[0,0,0]) #Primeiro DC

    for i in range(1, len(arr_dct_quantized)):
        dc_difference = int(arr_dct_quantized[i,0,0] - arr_dct_quantized[i-1,0,0])
        arrayDC[i] = dc_difference

    return arrayDC.astype(int)

def decode_DC(arrayDC_encoded):
    arrayDC = np.zeros(len(arrayDC_encoded))

    arrayDC[0] = int(arrayDC_encoded[0]) #Primeiro DC

    for i in range(1, len(arrayDC)):
        arrayDC[i] = arrayDC[i-1] + arrayDC_encoded[i]

    return arrayDC.astype(int)

#Ex4----------------------------------------------
def encode_AC(arr_dct_quantized):
    arrayAC_Output = []

    num_blocks = int(arr_dct_quantized.shape[0])

    for z in range(num_blocks):
        arrayAC_zigzag = np.zeros(8 * 8)
        for y in range(8):
            for x in range(8):
                idx = int(zigzag[y][x])
                arrayAC_zigzag[idx] = arr_dct_quantized[z][y][x]

        arrayAC_tuples = []
        num_zeros = 0
        for i in range(1, len(arrayAC_zigzag)):
            if(arrayAC_zigzag[i]==0):
                num_zeros += 1
            else:
                arrayAC_tuples.append((num_zeros, arrayAC_zigzag[i]))
                num_zeros = 0

        arrayAC_tuples.append((0,0))
        arrayAC_tuples = np.asarray(arrayAC_tuples).astype(int)
        arrayAC_Output.append(arrayAC_tuples)

    return np.asarray(arrayAC_Output)

def decode_AC(encoded_AC):
    arrayOutput = np.zeros([encoded_AC.shape[0],8*8])
    zigzag_64 = zigzag
    zigzag_64 = zigzag_64.reshape(64)

    for z in range(len(encoded_AC)):
        idx = 1
        for y in range(len(encoded_AC[z])):
            num0 = encoded_AC[z][y][0]
            num1 = encoded_AC[z][y][1]
            if(num0 == 0 and num1 == 0):
                break
            idx += encoded_AC[z][y][0]
            zzIDX = np.where(zigzag_64==idx)
            arrayOutput[z][zzIDX[0]] = num1
            idx+=1

    arrayOutput = arrayOutput.reshape(encoded_AC.shape[0],8,8)

    return arrayOutput.astype(int)

#Ex5 está a funcionar, dá a imagem certa

#Ex6----------------------------------------------
# TODO
def encode_ACDC_toFile(encoded_DC, encoded_AC):
    TODO


#Ex7----------------------------------------------
# TODO
def decode_DCAC_fromFile(filePath):
    TODO
    return decoded_DC, decoded_AC

#Ex8----------------------------------------------
# TODO

#Ex9----------------------------------------------
# TODO

#Ex10----------------------------------------------
# TODO






#Testes--------------------------

QUALITY = 50

imgPath = "LenaGray.tif"

factor = quality_factor(QUALITY)
Q = Q * factor

img = cv2.imread(imgPath)
img_array_original = np.ravel(img)

img_array_converted = convert(img_array_original)
print(img_array_original[0], len(img_array_converted))

img_8x8 = convertTo8x8(img_array_converted)
print("Original8x8\n",img_8x8[0])




#Ex1 encode--------------------------------------
img_dct_encoded = encodeDCT(img_8x8)
print("Encode DTC\n",img_dct_encoded[0])

#Ex2 encode--------------------------------------
img_dct_quantized_encoded = encode_quantizeDCT(img_dct_encoded)
print("Encode quantized DCT\n", img_dct_quantized_encoded[3])

#Ex3 encode--------------------------------------
img_encoded_DC = encode_DC(img_dct_quantized_encoded)
print("Encode DC\n", img_encoded_DC)

#Ex4 encode--------------------------------------
img_encoded_AC = encode_AC(img_dct_quantized_encoded)
print("Encode AC\n", img_encoded_AC)

#Ex6 encode--------------------------------------
#encode_ACDC_toFile(img_encoded_DC, img_encoded_AC)

#Ex7 (Ex6 decode)--------------------------------
#img_encoded_AC, img_encoded_DC, = img_decode_DCAC_fromFile(filePath)

#Ex4 decode--------------------------------------
img_decoded_AC = decode_AC(img_encoded_AC)
print("Decode AC\n", img_decoded_AC)

#Ex3 decode--------------------------------------
img_decoded_DC = decode_DC(img_encoded_DC)
print("Decode DC\n", img_decoded_DC)

#Junta as tabelas DC e AC
img_joined_DC_AC = join_DC_AC(img_decoded_DC, img_decoded_AC)
print("DC AC joined\n ", img_joined_DC_AC[3])

#Ex2 decode--------------------------------------
img_dct_quantized_decoded = decode_quantizeDCT(img_joined_DC_AC)
print("Decode quantized DCT\n", img_dct_quantized_decoded[0])

#Ex1 decode--------------------------------------
img_dct_decoded = decodeDCT(img_dct_quantized_decoded)
print("Decoded DCT\n", img_dct_decoded[0])

#Converte para o formato rgb e calcula snr
img_array_jpg = convertFrom8x8(img_dct_decoded)
print("SNR: ", SNR(img_array_jpg, img_array_original))

#Guarda a imagem em formato jpg
save_image_toFile(img_array_jpg)







