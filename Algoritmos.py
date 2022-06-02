from queue import PriorityQueue

#Heurística del algoritmo
#Usando la distancia Manhattan
def heuristica(celdaA, celdaB):
    x1, y1 = celdaA
    x2, y2 = celdaB
    return (abs(x1 - x2) + abs(y1 - y2))

def ida_star(mapa, objetivo,inicio):
    if objetivo == (21, 20):
        print("llegamos")    
    
    bound = heuristica(inicio, objetivo)
    path = [inicio]
    
    while(True):
        t = search(mapa, objetivo, path, 0, bound)
        
        if t == True:
            break
        if t == float("inf"):
            return
        
        bound = t
    
    path.reverse()
    return path

def search(mapa, objetivo, path, g, bound):
    node = path[0]
    f = g + heuristica(node, objetivo)
    if f > bound:
        return f
    if node == objetivo:
        return True
    min = float("inf")

    for d in 'ESNW':
        if mapa.maze_map[node][d]==True:
            if d=='E':
                succ =(node[0],node[1]+1)
            elif d=='W':
                succ =(node[0],node[1]-1)
            elif d=='S':
                succ =(node[0]+1,node[1])
            elif d=='N':
                succ =(node[0]-1,node[1])
            
            if succ not in path and succ not in mapa.snakeCeldas:
                path.insert(0,succ)
                t = search(mapa, objetivo, path, g+1, bound)
                if t == True:
                    return True
                if t < min:
                    min = t
                path.pop(0)
    
    return min

def DFS(mapa,objetivo,inicio):    
    explored=[inicio]
    frontier=[inicio]
    dfsPath={}
    while len(frontier)>0:
        currCell=frontier.pop()
        if currCell==objetivo:
            break
        for d in 'ESNW':
            if mapa.maze_map[currCell][d]==True:
                if d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                elif d=='W':
                    childCell=(currCell[0],currCell[1]-1)
                elif d=='S':
                    childCell=(currCell[0]+1,currCell[1])
                elif d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                if childCell in explored:
                    continue                
                explored.append(childCell)
                frontier.append(childCell)
                
                dfsPath[childCell]=currCell
    fwdPath={}
    cell=objetivo
    while cell!=inicio:
        fwdPath[dfsPath[cell]]=cell
        cell=dfsPath[cell]
    return convertirLista(inicio, objetivo, fwdPath)

def aEstrella(mapa,objetivo,inicio):
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
    camino = camino[:mapa.steps]
    largoFinal = len(camino)

    mapa.stepsFaltantes = largoInicial != largoFinal
    print("steps faltantes= ", mapa.stepsFaltantes)

    return camino

def calcularCamino(mapa,objetivo,inicio, crece):
    print("inicio", inicio, "objetivo", objetivo)    
    #camino = aEstrella(mapa,objetivo,inicio)
    #camino = DFS(mapa,objetivo,inicio)    
    camino = ida_star(mapa, objetivo, inicio)

    if not mapa.crece:
        crece = False
    
    if camino is not None:        

        if mapa.ejecucionInicial:
            mapa.ejecucionInicial=False
        else:
            camino = recortarCamino(mapa, camino)

        calcularCeldas(mapa,objetivo,inicio, crece, camino)
        
        mapa.snakeSize += 1 if crece else 0
        return convertirDiccionario(camino)
    
    print("NO HAY CAMINO")