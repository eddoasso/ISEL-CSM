import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


### EXERCICIO 1 ###
def gera_huffman(simbolo, ocorrencia):

    array = sorted(zip(ocorrencia, simbolo))
    
    #print(array)
    
    if(len(array) > 2 ):

        #soma de ocorrencias
        o1 = array[0][0]
        o2 = array[1][0]
        
        soma_ocorrencias = o1 + o2 

        #soma de simbolos
        s1 = array[0][1]
        s2 = array[1][1]
        
        soma_simbolos = s1 + s2

        #retirar os dois primeiros elementos
        del array[0]
        del array[0]

        #vai juntar esses novos valores ao conjunto
        array.append([soma_ocorrencias, soma_simbolos])

        #desimpacutar o array ou seja separar o simbolo e a ocorrencia
        o, s = zip(*array)
    
        codificados = gera_huffman(s,o)

        codificados = dict(codificados)

        #print(codificados)


        #vai buscar os simbolos
        huffman = codificados.get(soma_simbolos)

        #del codificados[soma_simbolos] #descomentar para testes
        
        
        #vai estar a dar o valor de 0 e 1 aos simbolos
        codificados[s1], codificados[s2] = str(huffman) + '0', str(huffman) + '1'
        
        codificados = list(zip(codificados.keys(), codificados.values()))
        
        return dict(codificados)
        
        
    return dict([(array[0][1],'1'),(array[1][1],'0')])


### EXERCICIO 2 ###
def codifica(mensagem, huffman):
    
    msg = ''
    
    for i in mensagem:

        msg += huffman[i]

    return msg  


### EXERCICIO 3 ###
def descodifica(mensagem, huffman):

    simbolos = []
    msg = ''
    values = huffman.values()
    keys = huffman.keys()

    for i in range(len(mensagem)):

        msg += mensagem[i]

        if(msg in values):

            x = list(keys)[list(values).index(msg)]
            simbolos.append(str(x))
            msg = ''
            
    return simbolos 
    
        
### EXERCICIO 4 ###
def escrever(mensagem, nome):
    
    file = open(nome, "w")
    #w para abrir um ficheiro para apenas escrever nele
    file.write(mensagem)
    #escreve a mensagem no ficheiro
    file.close()
    #fecha o ficheiro aberto
    

### EXERCICIO 5 ###
def ler(nome):
    
    file = open(nome, "r")
    #print(file.read()) #Descomentar para testes
    return file.read()


##simbolo = ['o','i','n','a','l','s','r','t','g']
##ocorrencia = [5,3,2,2,2,1,3,2,2]
##
##
##huffman = gera_huffman(simbolo,ocorrencia)
##print("Huffman: ")
##print(huffman)
##
##codifica = codifica("olstgggi", huffman)
##print("Codificação: " + str(codifica))
##
##descodifica = descodifica(codifica, huffman)
##print("Descodificação: " + str(descodifica))
##
##escrever = escrever("Ola", "teste.txt")
##print(escrever)
##
##ler = ler("teste.txt")
##print(ler)
