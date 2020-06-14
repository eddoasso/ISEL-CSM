import cv2
import numpy as np
import matplotlib.pyplot as plt
'''
my_string = "she sells sea shells"
print("Your message is:")
print(my_string)
print("Your data is " + str(len(my_string)*7) + " bits long")

# Create lista de caracteres e a sua frequencia
letters = []
only_letters = []

for letter in my_string:
	if (letter not in letters):
		freq = my_string.count(letter)
		letters.append(freq)
		letters.append(letter)
		only_letters.append(letter)

#print("letters: " + str(letters))
#print("only_letters: " + str(only_letters))

# Gerar base0level nodes

nodes = []
while len(letters)>0:
	nodes.append(letters[0:2])
	letters = letters[2:]
nodes.sort()
huffman_tree = []
huffman_tree.append(nodes)
#print("nodes: " + str(nodes))

def combine (nodes):
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
		combine(nodes)
	return huffman_tree

#print("NOS:", str(nodes))
newnodes = combine(nodes)
huffman_tree.sort(reverse=True)

checklist = []
for level in huffman_tree:
	for node in level:
		if (node not in checklist) and (type(node) is list):
			checklist.append(node)
		else:
			level.remove(node)
count = 0
for level in huffman_tree:
	print("Level",count,":",level)
	count += 1
print()

print(checklist)


letter_binary = []

if len(only_letters)==1:
	lettercode = [only_letters[0], "0"]
	letter_binary.append(lettercode*len(my_string))
else:
	for letter in only_letters:
		lettercode = ""
		for node in checklist:
			if (len(node)>2 and letter in node[1]):
				print(node)
				lettercode += node[2]
			lettercode = [letter, lettercode]
			letter_binary.append(lettercode)
#print(letter_binary)
'''

a =  [
  ['Dodge', 'Ferrari', 'Fiat', 'Ford'], 
  ['Geely', 'Honda', 'Hyundai', 'Infiniti'], 
  ['Bentley', 'Hyundai', 'Lamborghini'],
  ['Koenigsegg', 'Maserati']
 ]

print(type(a))