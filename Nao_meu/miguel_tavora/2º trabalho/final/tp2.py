import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from time import time

def gerarDicionario (text):
    text = list (text)
    dicionario = []
    for i in set(text):
        dicionario.append([text.count(i)/len(text), i])
    return dicionario

#tabela = gerarDicionario("OLA MUNDO!!!")

def ordemCrescente (table):
	for i in range (len (table)):
		for j in range (i+1, len (table)):
			if (table[i][0] > table [j][0]):
				temp = table[i]
				table[i] = table [j]
				table[j] = temp
	return table
####################################################################################


def escrever (message, fileName):
    #print("--------------------------------------ESCREVER--------------------------------------\n")
	#file = open(str(fileName), 'w')
	np.packbits(list(map(int, message))).tofile("f.txt")
	print("Wrote: \"" + str(message) + "\" to \'" + str(fileName) + "\'\n")
	#file.close()

def ler (fileName, a=False):
    #print("--------------------------------------LER--------------------------------------\n")
    if(not a):
        file = open(str(fileName), 'r')
    else:
        file = open(str(fileName), 'rb')
    
    r = file.read()
    
    file.close()
    
    print("Read: \"" + str(r) + "\" from: \'" + str(fileName) + "\'\n")
    return str(r)
####################################################################################
#print("IMAGEM-----------------------")
# Lê a imagem em níveis de cinzento
#x = cv2.imread("lenac.tif",cv2.IMREAD_GRAYSCALE)
# Converte a imagem (matriz) numa sequência de números (array)
#xi = x.ravel()
#aa = ""
#for i in range(len(xi)):
#    aa+=str(xi[i])
#print(aa)
# Calcula o histogram
#h, bins, patches = plt.hist(xi,256,[0,256])
# Gera o código de Huffman
#t0 = time()

#print(np.concatenate(np.arange(0, 256), h))
#img = []
#for i in range(256):
#    img.append([h[i], str(i)])

#tabela = img
#print(tabela)
#tabela = np.arange(0,256),h


########## IMAGEM

#text = ler("HenryMancini-PinkPanther30s.mp3", True)
#text = ler("HenryMancini-PinkPanther.mid", True)
text = ler("ecg.txt")
#text = ler("ubuntu_server_guide.txt")
#t0 = time()
tabela = gerarDicionario(text)
huffman_tree = []
huffman_tree.append(tabela)

def gera_huffman (nodes):
	newnode = []
	#print("LEN")
	#print(len(nodes))
	if len(nodes)>1:
		#print("nodes:", str(nodes))
		nodes.sort()
		nodes[0].append("0")
		nodes[1].append("1")
		combined_node1 = (nodes[0][0] + nodes[1][0])
		combined_node2 = (nodes[0][1] + nodes[1][1])
		newnode.append(combined_node1)
		newnode.append(combined_node2)
		newnodes = []
		newnodes.append(newnode)
		newnodes = newnodes + nodes[2:]
		nodes = newnodes
		huffman_tree.append(nodes)
		gera_huffman (nodes)
	return huffman_tree
########## IMAGEM
    


def printLevels(huffmanTable):
    #huffmanTable = huffmanTable[::-1]
    print("--------------------------------------PRINT-LEVELS--------------------------------------\n")
    counter = 0
    for level in huffmanTable:
    	print("Level", counter, ":", level)
    	counter += 1
huffmanTable = gera_huffman(tabela)
huffmanTable = huffmanTable[::-1]
#t1 = time()
#print ("time:", t1-t0)
#print("--------------------------------------CODIFICA--------------------------------------\n")
def code (letter, table):
	ajuda = ""
	nodeBefore = []
	for level in table:
		for node in level:
			if letter in node[1] and len(node)>2 and node != nodeBefore:
				nodeBefore = node
				ajuda += node[2]
	return ajuda

def codifica (text, table):
	letters = list(text)
	elFinal = ""
	for letter in letters: elFinal += code(letter, table)
	return elFinal

def codificaverdadeiro(text, dicionario):
    s = ""
    for char in text:
        for values in dicionario:
            if char == values[0]:
                s += values[1]
    return s

def tabelaCodificacao(table, dicionario):
	print("TABELA DE CODIFICACAO")
	cod = []
	a = []
	for nome in dicionario:
		c = codifica(nome[1], table)
		print("Letter (" + str(nome[1]) + "): " + str(c))
		cod.append([nome[1], c])
		a.append(c)
	return cod, a
t0 = time()
codificacao, codigos = tabelaCodificacao(huffmanTable, tabela)
codificado = codificaverdadeiro(text, codificacao)
t1 = time()
print("TIME", str(t1-t0))
escrever(codificado, "ecgCODIFICADO.txt")
escrever(codificado, "ubuntu_server_guideCODIFICADO.txt")
#print("--------------------------------------DESCODIFICAR--------------------------------------\n")
def descodifica (message, dicionario):
    strfinal = ""
    s = ""

    for char in message:
        s += char
        for values in dicionario:
            if s == str(values[1]):
                strfinal += str(values[0])
                s = ""
                break
    return strfinal
t0 = time()
descodificado = descodifica(codificado, codificacao)
t1 = time()
print(descodificado)
print("TIME", str(t1-t0))

def entropia(p):
    elFinal = 0
    for i in range(len(p)):
        elFinal += (p[i][0]*np.log2(p[i][0]))

    return -1*elFinal
entrop = entropia(tabela)
print("ENTROPIA",entrop)
def numeroMedio(a):
    nmr = 0
    count = 0
    for i in range(len(a)):
        nmr += len(list(a[i]))
        count += 1
    return nmr/count
nm = numeroMedio(codigos)
print("NUMERO MEDIO",nm)
def eficiencia(e, n):
    return e/n
print("EFICIENCIA",eficiencia(entrop, nm))