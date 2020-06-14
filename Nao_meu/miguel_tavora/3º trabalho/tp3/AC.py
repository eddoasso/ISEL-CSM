import numpy as np

def codificadorAC (arr):
    # zig-zag order
    zigzag = np.zeros((8, 8))
    zigzag[0] = [ 0,  1,  5,  6, 14, 15, 27, 28]
    zigzag[1] = [ 2,  4,  7, 13, 16, 26, 29, 42]
    zigzag[2] = [ 3,  8, 12, 17, 25, 30, 41, 43]
    zigzag[3] = [ 9, 11, 18, 24, 31, 40, 44, 53]
    zigzag[4] = [10, 19, 23, 32, 39, 45, 52, 54]
    zigzag[5] = [20, 22, 33, 38, 46, 51, 55, 60]
    zigzag[6] = [21, 34, 37, 47, 50, 56, 59, 61]
    zigzag[7] = [35, 36, 48, 49, 57, 58, 62, 63]
    zigzag = zigzag.reshape(64,order='F').astype('int')
    
    length = len(arr)
    
    # Preencher o array ordenadamente
    sortedArray = np.zeros_like(arr).reshape(length ,64)
    sort = np.argsort(zigzag)
    
    for blocoPos in range(length):
        blocoFlat = arr[blocoPos].flatten(order='F')
        sortedArray[blocoPos] = blocoFlat[sort]
    
    #print(sortedArray)
    
    zeros = 0
    tuplos = []
    for x in range(length):
        for y in range(64):
            # Se for a primeira posicao do bloco
            if y != 0:
                if int(sortedArray[x][y]) != 0:
                    tuplos.append((int(zeros),int(sortedArray[x][y])))                
                    zeros = 0
                else:
                    zeros +=1
                    if y == 63 or zeros == 15:
                        tuplos.append((int(zeros),int(sortedArray[x][y])))
                        zeros = 0
            else:
                # Guardar os DC
                tuplos.append(int(sortedArray[x][y]))
        tuplos.append((0,0))
    
    # Retirar os zeros a mais
    tuplos = tuplos[::-1]
    
    i = 0
    while i < len(tuplos) - 1:
        tuplo = tuplos[i]
        if isinstance(tuplo, tuple) and tuplo == (0, 0):
            bfrTuplo = tuplos[i + 1]
            if type(bfrTuplo) == tuple and bfrTuplo [1] == 0:
                tuplos.pop(i + 1)
                i -=1 
        i += 1
    
    tuplos =  tuplos[::-1]
    
    return tuplos
    


def descodificadorAC(arr):
    
    # zig-zag order
    zigzag = np.zeros((8, 8))
    zigzag[0] = [ 0,  1,  5,  6, 14, 15, 27, 28]
    zigzag[1] = [ 2,  4,  7, 13, 16, 26, 29, 42]
    zigzag[2] = [ 3,  8, 12, 17, 25, 30, 41, 43]
    zigzag[3] = [ 9, 11, 18, 24, 31, 40, 44, 53]
    zigzag[4] = [10, 19, 23, 32, 39, 45, 52, 54]
    zigzag[5] = [20, 22, 33, 38, 46, 51, 55, 60]
    zigzag[6] = [21, 34, 37, 47, 50, 56, 59, 61]
    zigzag[7] = [35, 36, 48, 49, 57, 58, 62, 63]
       
    ind_O = zigzag.reshape(64,order='F').astype('int')
    
    zigzag = []
    bloco8x8 = []
    
    for valor in arr:
        
        if isinstance(valor, tuple):
            
            if valor[0] == 0 and valor[1] == 0:
                
                resto = 64 - len(bloco8x8)
                
                for i in range(resto):
                    bloco8x8.append(0)
                
                bloco8x8 = np.array(bloco8x8)            
                
                zigzag.append(bloco8x8[ind_O].reshape((8,8),order='F'))
                
                bloco8x8 = []
                
            else:
                zeros = valor[0]
                
                for i in range(zeros):
                    bloco8x8.append(0.)
                
                if valor[1] != 0:
                    bloco8x8.append(valor[1])
        else:
            bloco8x8.append(valor)
    
    return zigzag
