import numpy as np
import array as arr
from tab_jpeg import K3, K5

def codificarImagem (lista, filename):
    
    bits = []
    for valor in lista:
        if isinstance(valor, tuple):
            if (valor[0] == 0 and valor[1] == 0):
                bits.append('1010')
            else:
                if valor[1] > 0:
                    val = valor[0]
                    binario = bin(valor[1])[2:]
                    size = len(binario)
                elif valor[1] < 0:
                    val = valor[0]
                    binario_aux = bin(valor[1])[3:]
                    binario = ''.join('1' if i == '0' else '0' for i in binario_aux)
                    size = len(binario)
                else:
                    val = valor[0]
                    size = 0
                    binario = ""
                
                bits.append(K5[(val, size)])
                bits.append(binario)
        else:
            if valor > 0:
                a = bin(valor)[2:]
                size = K3[len(a)]
            elif valor < 0:
                bin_aux = bin(valor)[3:]
                a = ''.join('1' if i == '0' else '0' for i in bin_aux)
                size = K3[len(a)]
            else:
                size = K3[valor]
                a = ""
            
            bits.append(size)
            bits.append(a)
    
    mensagem = ''.join(bits)
    escreverFicheiro(mensagem, filename)
    return mensagem

def descodificarImagem (filename):
    mensagem = lerFicheiro(filename)
    iK3 = {}
    for key, value in K3.items():
        iK3[value] = key
    
    iK5 = {}
    for key, value in K5.items():
        iK5[value] = key
    
    elFinal = []
    codigo = ""
    EOF = True
    
    while len(mensagem) != 0:
        codigo += mensagem[0]
        mensagem = mensagem[1:]
                
        if codigo in iK3 and EOF:
            length = iK3[codigo]
            value = mensagem[0: length]
            if len(value) != 0:
                if value[0] == '0':# Negativo
                    value = ''.join('1' if i == '0' else '0' for i in value) # Complemento
                    value = -int(value, 2)
                else:
                    value = int(value, 2)
            else: 
                value = 0
            
            elFinal.append(value)
            codigo = ''
            mensagem = mensagem[length:]
            EOF = False
            
        if codigo in iK5 and not EOF:
            
            tuplo = iK5[codigo]
            
            if tuplo == (0, 0):
                elFinal.append((0, 0))
                EOF = True
            else:
                length = tuplo[1]
                nmr = 0
                if length != 0:
                    nmr = mensagem[0:length]
                    # Negativo
                    if nmr[0] == '0':
                        nmr = ''.join('1' if i == '0' else '0' for i in nmr) # Complemento
                        nmr = -int(nmr, 2)
                    else:
                        nmr = int(nmr, 2)
                zeros = tuplo[0]
                elFinal.append((zeros, nmr))
                mensagem = mensagem[length:]
            codigo = ''
    return elFinal

def escreverFicheiro (text, nome):
    colocar = len(text)%8
    valor = 0
    if colocar != 0:
        valor = 8 - colocar
        for i in range(valor):
            text += "0"
    
    binarios = np.array(list(text))
    a = int(len(binarios)/8)
    binarios = binarios.reshape(a,8) 
    ficheiro = arr.array('B')
    ficheiro.append(valor)
    
    for numeroBits in range (len(binarios)):
        stringInt = ''.join(map(str, binarios[numeroBits]))
        inteiro = int(stringInt,2)
        ficheiro.append(inteiro)
                     
    f = open(nome, 'wb')
    ficheiro.tofile(f)

def lerFicheiro(nomeFicheiro):
    ficheiro = np.fromfile(nomeFicheiro, dtype='B')
    remover = ficheiro[0]
    ficheiro = ficheiro[1:]
    arr_ = []
    
    for char in ficheiro:
        arr_.append(bin(char)[2:].zfill(8))
    
    binario = ''.join(arr_)
    binario = binario[:len(binario) - remover]
    
    return binario