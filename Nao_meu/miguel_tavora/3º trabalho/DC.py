
def codificadorDC(arr):
    
    delta = 0
    for i in range(len(arr)):
        arr[i][0][0] -= delta
        delta = arr[i][0][0] + delta
    
    return arr


def descodificadorDC(arr):
    
    delta = 0
    for i in range(len(arr)):
        arr[i][0][0] += delta
        delta = arr[i][0][0]
    
    return arr