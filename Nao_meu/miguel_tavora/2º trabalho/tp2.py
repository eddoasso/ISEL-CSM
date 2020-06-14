import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def geraDicionario (text):
	text = list (text)
	dicionario = []
	rep = []
	for i in range (len(text)) :
		if text[i] not in rep : dicionario.append([text.count(text[i]), text[i]])
		if i != len(text) - 1:
			for j in range (i + 1, len(text)):
				if text[i] == text[j]:
					rep.append(text[j])

	return dicionario

tabela = geraDicionario ("HELLO")

def ordemCrescente (table):
	for i in range (len (table)):
		for j in range (i+1, len (table)):
			if (table[i][0] > table [j][0]):
				temp = table[i]
				table[i] = table [j]
				table[j] = temp
	return table

huffmanTable = []

def gera_huffman (level):
	global huffmanTable
	if len(level) > 1:
		level = ordemCrescente(level)
		level[0].append('0')
		level[1].append('1')
		huffmanTable.append(level)
		level = [[level[0][0] + level[1][0], level[0][1] + level[1][1]]] + level[2::]
		return gera_huffman(level)
	huffmanTable.append(level)
	return

gera_huffman(tabela)

huffmanTable = huffmanTable[::-1]

print("--------------------------------------PRINT-LEVELS--------------------------------------\n")
counter = 0
for level in huffmanTable:
	print("Level", counter, ":", level)
	counter += 1

print("--------------------------------------CODIFICA--------------------------------------\n")
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
	for letter in letters: elFinal += code(letter, huffmanTable)
	return elFinal

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

codificacao, codigos = tabelaCodificacao(huffmanTable, tabela)
print("--------------------------------------DESCODIFICA--------------------------------------\n")

def findWithBits (bits, coded):
	for a in coded:
		if a[1] == bits: return a[0]

def descodifica (message, coded, codes, elFinal=""):
	msg = message
	bits = msg[0]
	found = False
	if len(bits) > 0:
		for i in range(len(msg)):
			if bits in codes:
				found = True
				#print("MENSAGEM",findWithBits(bits, coded)
				
				elFinal += findWithBits(bits, coded)
				break
			else:
				bits += msg[i+1]
		if found:
			if len(msg[len(list(bits))::]) > 0 : return descodifica(msg[len(list(bits))::], coded, codes, elFinal)
	return elFinal

descodificado = descodifica(list("110111001010"), codificacao, codigos)
print(descodificado)
print("--------------------------------------ESCREVER--------------------------------------\n")

def escrever (message, fileName):
	file = open(str(fileName) + '.txt', 'w')
	file.write(message)
	print("Wrote: \"" + str(message) + "\" to \'" + str(fileName) + ".txt\'\n")
	file.close()

escrever("010010101", "escrever")

print("--------------------------------------LER--------------------------------------\n")

def ler (fileName):
	file = open(str(fileName) + '.txt', 'r')
	r = file.read()
	file.close()
	print("Read: \"" + str(r) + "\" from: \'" + str(fileName) + ".txt\'")
	return r

ler("escrever")