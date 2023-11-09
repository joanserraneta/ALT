import numpy as np
import math

def levenshtein_matriz(x, y, threshold=None):
    # esta versión no utiliza threshold, se pone porque se puede
    # invocar con él, en cuyo caso se ignora
    lenX, lenY = len(x), len(y)
    D = np.zeros((lenX + 1, lenY + 1), dtype=np.int32)
    for i in range(1, lenX + 1):
        D[i][0] = D[i - 1][0] + 1
    for j in range(1, lenY + 1):
        D[0][j] = D[0][j - 1] + 1
        for i in range(1, lenX + 1):
            D[i][j] = min(
                D[i - 1][j] + 1,
                D[i][j - 1] + 1,
                D[i - 1][j - 1] + (x[i - 1] != y[j - 1]),
            )

    return D[lenX, lenY]

def levenshtein_edicion(x, y, threshold=None):
    # a partir de la versión levenshtein_matriz
    lenX, lenY = len(x), len(y)
    D = np.zeros((lenX + 1, lenY + 1), dtype=np.int32)
    for i in range(1, lenX + 1):
        D[i][0] = D[i - 1][0] + 1
    for j in range(1, lenY + 1):
        D[0][j] = D[0][j - 1] + 1
        for i in range(1, lenX + 1):
            D[i][j] = min(
                D[i - 1][j] + 1,
                D[i][j - 1] + 1,
                D[i - 1][j - 1] + (x[i - 1] != y[j - 1]),
            )

    posicion_x = lenX
    posicion_y = lenY
    camino = []

    while posicion_x != 0 and posicion_y != 0:
        if D[posicion_x, posicion_y] == D[posicion_x-1, posicion_y] + 1:
            camino.append((x[posicion_x-1],''))
            posicion_x -= 1
        elif D[posicion_x, posicion_y] == D[posicion_x, posicion_y-1] + 1 :
            camino.append(('', y[posicion_y-1]))
            posicion_y -= 1
        else:
            camino.append((x[posicion_x-1], y[posicion_y-1]))
            posicion_x -= 1
            posicion_y -= 1
            
    
    while posicion_x != 0:
        camino.append((x[posicion_x-1], ''))
        posicion_x -= 1
    
    while posicion_y != 0:
        camino.append(('', y[posicion_y-1]))
        posicion_y -= 1

    camino.reverse()

    return D[lenX, lenY],camino 

def levenshtein_reduccion(x, y, threshold=None):
    # completar versión con reducción coste espacial

    lenX = len(x) + 1
    lenY = len(y) + 1

    vcurrent = [(1) for i in range(lenY)]
    vprev = [(i) for i in range(lenY)]


    for i in range(1, lenX):
        for j in range(1, lenY):
            vcurrent[j] = min(
                vprev[j] + 1,
                vprev[j-1] if x[i - 1] == y[j - 1] else  vprev[j-1] + 1,
                vcurrent[j-1] + 1
            )

        vprev = vcurrent
        vcurrent = [(i + 1) for _ in range(lenY)]

    return vprev[lenY - 1]

def levenshtein(x, y, threshold):
    # completar versión reducción coste espacial y parada por threshold
    lenX = len(x) + 1
    lenY = len(y) + 1 
    
    vcurrent = [(1) for i in range(lenY)]
    vprev = [(i) for i in range(lenY)]
    
    
    for i in range(1, lenX):
        for j in range(1, lenY):
            vcurrent[j] = min(
                vprev[j] + 1, 
                vprev[j-1] if x[i - 1] == y[j - 1] else  vprev[j-1] + 1, 
                vcurrent[j-1] + 1 
            )
            
        vprev = vcurrent
        vcurrent = [(i + 1) for _ in range(lenY)]

    return min(vprev[lenY - 1], threshold+1)

def levenshtein_cota_optimista(x, y, threshold):
    return 0 # COMPLETAR Y REEMPLAZAR ESTA PARTE

def damerau_restricted_matriz(x, y, threshold=None):
    # completar versión Damerau-Levenstein restringida con matriz
    lenX, lenY = len(x), len(y)
    D = np.zeros((lenX + 1, lenY + 1), dtype=np.int32)
    for i in range(1, lenX + 1):
        D[i][0] = D[i - 1][0] + 1
    for j in range(1, lenY + 1):
        D[0][j] = D[0][j - 1] + 1

    for i in range(1, lenX + 1):
        for j in range(1, lenY + 1):
            if i > 1 and j > 1:
                if x[i - 2] == y[j - 1] and x[i - 1] == y[j - 2]:
                    D[i][j] = min(D[i][j - 1] + 1,
                                  D[i - 1][j] + 1,
                                  D[i - 1][j - 1] + 1,
                                  D[i - 2][j - 2] + (x[i - 1] != y[j - 1]))
                    continue
            D[i][j] = min(D[i - 1][j] + 1,
                          D[i][j - 1] + 1,
                          D[i - 1][j - 1] + (x[i - 1] != y[j - 1]))

    return D[len(x), len(y)]

def damerau_restricted_edicion(x, y, threshold=None):
    # partiendo de damerau_restricted_matriz añadir recuperar
    # secuencia de operaciones de edición
    lenX, lenY = len(x), len(y)
    D = np.zeros((lenX + 1, lenY + 1), dtype=np.int32)
    for i in range(1, lenX + 1):
        D[i][0] = D[i - 1][0] + 1
    for j in range(1, lenY + 1):
        D[0][j] = D[0][j - 1] + 1

    for i in range(1, lenX + 1):
        for j in range(1, lenY + 1):
            if i > 1 and j > 1:
                if x[i - 2] == y[j - 1] and x[i - 1] == y[j - 2]:
                    D[i][j] = min(D[i][j - 1] + 1,
                                  D[i - 1][j] + 1,
                                  D[i - 1][j - 1] + 1,
                                  D[i - 2][j - 2] + (x[i - 1] != y[j - 1]))
                    continue
            D[i][j] = min(D[i - 1][j] + 1,
                          D[i][j - 1] + 1,
                          D[i - 1][j - 1] + (x[i - 1] != y[j - 1]))

    posicion_x = lenX
    posicion_y = lenY
    camino = []

    while posicion_x != 0 and posicion_y != 0:
        # compuebo si hay transposicion
        if x[posicion_x-2]==y[posicion_y-1] and x[posicion_x-1]==y[posicion_y-2]:
            camino.append((x[posicion_x - 2] + ''+x[posicion_x - 1],x[posicion_x - 1] +''+ x[posicion_x - 2]))
            posicion_x -= 2
            posicion_y -= 2
        else:
            if D[posicion_x, posicion_y] == D[posicion_x-1, posicion_y] + 1:
                camino.append((x[posicion_x-1],''))
                posicion_x -= 1
            elif D[posicion_x, posicion_y] == D[posicion_x, posicion_y-1] + 1 :
                camino.append(('', y[posicion_y-1]))
                posicion_y -= 1
            else:
                camino.append((x[posicion_x-1], y[posicion_y-1]))
                posicion_x -= 1
                posicion_y -= 1


    while posicion_x != 0:
        camino.append((x[posicion_x - 1], ''))
        posicion_x -= 1

    while posicion_y != 0:
        camino.append(('', y[posicion_y - 1]))
        posicion_y -= 1

    camino.reverse()

    return D[lenX, lenY], camino


def damerau_restricted(x, y, threshold=None):
    # versión con reducción coste espacial y parada por threshold
    return []


def damerau_intermediate_matriz(x, y, threshold=None):
    # completar versión Damerau-Levenstein intermedia con matriz
    return[]

def damerau_intermediate_edicion(x, y, threshold=None):
    # partiendo de matrix_intermediate_damerau añadir recuperar
    # secuencia de operaciones de edición
    # completar versión Damerau-Levenstein intermedia con matriz
    return 0,[] # COMPLETAR Y REEMPLAZAR ESTA PARTE
    
def damerau_intermediate(x, y, threshold=None):
    # versión con reductam_x = len(x) + 1
    return [] 
    

opcionesSpell = {
    'levenshtein_m': levenshtein_matriz,
    'levenshtein_r': levenshtein_reduccion,
    'levenshtein':   levenshtein,
   # 'levenshtein_o': levenshtein_cota_optimista,
    'damerau_rm':    damerau_restricted_matriz,
  #  'damerau_r':     damerau_restricted,
   # 'damerau_im':    damerau_intermediate_matriz,
  #   'damerau_i':     damerau_intermediate
}

opcionesEdicion = {
    'levenshtein': levenshtein_edicion,
    'damerau_r':   damerau_restricted_edicion,
   # 'damerau_i':   damerau_intermediate_edicion
}

