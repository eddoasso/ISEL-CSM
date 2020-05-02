import numpy as np
import copy
import cv2
import matplotlib.pyplot as plt
import time
from bitstring import BitArray
from os import path


#Ordena o dicionário por ordem decrescente
def sort_dic(dic):
    dic_output = {}
    sorted_keys = sorted(dic, key=dic.get, reverse=True)
    for key in sorted_keys:
        dic_output[key] = dic[key]
    return dic_output

#Testa e converte a mensagem para chars
def convert(message):
    return list(map(chr, message))

#Retorna um dicionário com as probabilidades de cada símbolo
def getProbDic(message):
    unique, counts = np.unique(message, return_counts=True)
    counts = counts/len(message)
    dic = dict(zip(unique, counts))

    return sort_dic(dic)

#Retorna um dicionário com os símbolos codificados
def gen_huff_table(word_dic):
    dic_bits = {}

    for i in list(word_dic.keys()):
        dic_bits[i] = ''

    dic_list = []

    dic_list.append(word_dic)

    #Cria uma arvore de letras e atribui o código a cada símbolo
    while (len(dic_list[len(dic_list)-1])!=1):
        previous_dic = dic_list[len(dic_list) - 1]

        keys = list(previous_dic.keys())
        key1 = keys[-1]
        val1 = previous_dic[key1]
        key2 = keys[-2]
        val2 = previous_dic[key2]

        for i in key1:
            dic_bits[i] = '1' + dic_bits[i]

        for i in key2:
            dic_bits[i] = '0' + dic_bits[i]


        newKey = key2 + key1
        newValue = val1 + val2

        new_dic = copy.deepcopy(previous_dic)
        new_dic.pop(key1)
        new_dic.pop(key2)
        new_dic[newKey] = newValue

        dic_list.append(sort_dic(new_dic))

    return dic_bits

#Retorna uma string com a mensagem codificada em 0's e 1's
def encode_huff(message, symbol_code_table):
    bit_sequence = ''

    for i in message:
        bit_sequence += symbol_code_table.get(i)

    return bit_sequence

#Retorna a mensagem em formato string descodificada
def decode_huff(message_encoded, bin_code, symbol_code_table):
    difference = len(bin_code) - len(message_encoded)
    if(difference != 0):
        bin_code = bin_code[:-difference]

    message = ""
    buffer = ""
    for i in bin_code:
        buffer += i
        for key, value in symbol_code_table.items():
            if value == buffer:
                message += key
                buffer = ""
                break

    print(message)
    return message

def writeArray2File(encoded):
    f = open('File.tif', 'wb')
    b = BitArray(bin=encoded)
    b.tofile(f)
    f.close()

def readFile2Array(filename):
    f = open(filename, 'rb')
    f = f.read()
    a = BitArray(f)
    a = a.bin
    return a


def messageToImage(message_decoded):
    array = np.zeros([512,512,3])
    a = 0
    for i in range(len(array)):
        for j in range(len(array[i])):
            array[i][j] = ord(message_decoded[a])
            a += 1

    print(len(array))
    cv2.imwrite('lenaZip.jpg', array)


word = ["p","a","l","a","v","r","a","s"]



t0 = time.time()

# Lê a imagem em níveis de cinzento
img_read = cv2.imread( "lena.tiff", cv2.IMREAD_GRAYSCALE )


# Converte a imagem (matriz) numa sequência de números (array)
img_array = img_read.ravel()
img_array = convert(img_array)


# código alínea a) - Gera o código de Huffman
message_prob = getProbDic(img_array)

#Alínea a)
t0 = time.time()
symbol_code_table = gen_huff_table(message_prob)
t1 = time.time()
print ("Huff table time: ", t1-t0)

#Alínea b)

#Alínea c)
t0 = time.time()
message_encoded = encode_huff(img_array, symbol_code_table)
t1 = time.time()
print("Encode message time: ", t1-t0)
#print("Message encoded: "+message_encoded)

#Alínea d)
#Escreve a mensagem em binário para um ficheiro
writeArray2File(message_encoded) #Original 257KB, Comprimida 239KB

#Alínea e)
#Lê a mensagem do ficheiro e retorna-a numa string
message_read = readFile2Array('File.tif')

#Alínea f)
#Descodifica a mensagem
t0 = time.time()
message_decoded = decode_huff(message_encoded, message_read, symbol_code_table)
t1 = time.time()
print("Decoded message time: ", t1-t0)
#print("Message decoded: "+message_decoded)

#Alínea g)
#Deteção de erro

#Converte a array de símbolos para uma string
message_string = ''
for i in img_array:
    message_string+=i

#Testa se a mensagem enviada (array de símbolos)
#é igual à mensagem recebida (descodificada)
print(message_decoded == message_string)

size_ini = path.getsize("lena.tiff")
size_end = path.getsize("File.tif")
print("taxa: ", 1.* size_ini / size_end)

messageToImage(message_decoded)



