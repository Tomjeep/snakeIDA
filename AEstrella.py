from queue import PriorityQueue

#Heurística del algoritmo
#Usando la distancia Manhattan
def heuristica(celdaA, celdaB):
    x1, y1 = celdaA
    x2, y2 = celdaB
    return (abs(x1 - x2) + abs(y1 - y2))

def aEstrella(mapa,objetivo,inicio):
    print("objetivo", objetivo)
    print("inicio", inicio)
    cola = PriorityQueue()
    cola.put((heuristica(inicio, objetivo), heuristica(inicio, objetivo), inicio))
    camino = {}

    pesoG = {celda: float("inf") for celda in mapa.grid}
    pesoG[inicio] = 0
    pesoF = {celda: float("inf") for celda in mapa.grid}
    pesoF[inicio] = heuristica(inicio, objetivo)
        
    while not cola.empty():
        celdaActual = cola.get()[2]
        if celdaActual == objetivo:
            break        
        
        for d in 'ESNW':
            if mapa.maze_map[celdaActual][d]==True:
                if d=='E':
                    celdaVecina=(celdaActual[0],celdaActual[1]+1)
                elif d=='W':
                    celdaVecina=(celdaActual[0],celdaActual[1]-1)
                elif d=='N':
                    celdaVecina=(celdaActual[0]-1,celdaActual[1])
                elif d=='S':
                    celdaVecina=(celdaActual[0]+1,celdaActual[1])

                gTemp = pesoG[celdaActual] + 1
                fTemp = gTemp + heuristica(celdaVecina, objetivo)

                if fTemp < pesoF[celdaVecina] and celdaVecina not in mapa.snakeCeldas:   
                    camino[celdaVecina] = celdaActual
                    pesoG[celdaVecina] = gTemp
                    pesoF[celdaVecina] = gTemp + heuristica(celdaVecina, objetivo)
                    cola.put((pesoF[celdaVecina], heuristica(celdaVecina, objetivo), celdaVecina))
    
    if objetivo in camino:

        caminoInvertido={}
        celda=objetivo
                        
        while celda!=inicio:            
            caminoInvertido[camino[celda]]=celda
            celda=camino[celda]                  
        
        return convertirLista(inicio, objetivo, caminoInvertido)

def convertirLista(inicio, objetivo, camino):    
    celda=inicio
    celdas = [celda]
                    
    while celda!=objetivo:            
        celda=camino[celda]
        celdas.append(celda)

    return celdas

def convertirDiccionario(camino):
    inicio = camino.pop(0)
    celda = camino.pop(0)
    diccionario = {inicio:celda}

    for x in camino:
        diccionario[celda] = x
        celda = x

    return diccionario


def calcularCeldas(mapa,objetivo,inicio, crece, camino):
    snakeLargo = mapa.getSnakeSize() if crece else mapa.getSnakeSize() - 1
    if (snakeLargo == 0): 
        snakeLargo += 1
    
    snakeCeldas = camino[-(snakeLargo+1):]
    snakeCeldas.reverse()
    
    while len(snakeCeldas) <= snakeLargo:
        snakeCeldas.append(mapa.snakeCeldas.pop(1))

    mapa.snakeCeldas = snakeCeldas

def recortarCamino(mapa, camino):
    largoInicial = len(camino)
    camino = camino[-mapa.steps:]
    largoFinal = len(camino)

    mapa.stepsFaltantes = largoInicial != largoFinal
    print("steps faltantes= ", mapa.stepsFaltantes)

    return camino

def calcularCamino(mapa,objetivo,inicio, crece):
    camino = aEstrella(mapa,objetivo,inicio)        

    if camino is not None:        

        camino = recortarCamino(mapa, camino)

        calcularCeldas(mapa,objetivo,inicio, crece, camino)
        
        return convertirDiccionario(camino)
    
    print("NO HAY CAMINO")