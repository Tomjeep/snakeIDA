from libs.agent import agent,textLabel
from libs.color import COLOR
from AEstrella import *
from random import randrange

def cicloSnake(mapa, cabeza):
    tempx = mapa.snakeCeldas[0][0]#mapa._objetivo.x
    tempy = mapa.snakeCeldas[0][1]#mapa._objetivo.y
    mapa._canvas.delete(cabeza)
        
    if not mapa.respaldoObjetivo:
        mapa._canvas.delete(mapa._objetivo._head)
        objetivo = crearObjetivo(mapa)
    else:        
        mapa._objetivo = mapa.respaldoObjetivo
        mapa._goal = mapa.respaldoGoal
        objetivo = mapa._goal
        mapa.respaldoObjetivo = ()
        mapa.respaldoGoal = ()   
    
    camino = calcularCamino(mapa, objetivo, (tempx,tempy), True)    
    if camino == None:        
        encerrado(mapa)      
        return 
    
    ejecutarCaminoValido(mapa, camino, (tempx,tempy)) 
     
    #mapa.snakeSize += 1    
    #c=agent(mapa,tempx,tempy,color='red',footprints=True) 
                         
    #mapa.tracePath({c:camino},delay=mapa.snakeDelay,kill=True)

def recorrerRestantes(mapa, cabeza):
    mapa._canvas.delete(cabeza)
    print("restantes Objetivo original", mapa.respaldoGoal) 
    print("restantes inicio", mapa.inicioRestante) 
    print("restantes snakeCeldas ", mapa.snakeCeldas)
    mapa._goal = mapa.respaldoGoal
    camino = calcularCamino(mapa, mapa.respaldoGoal, mapa.inicioRestante, False)

    ejecutarCaminoValido(mapa, camino, mapa.inicioRestante)

def ejecutarCaminoValido(mapa, camino, start): 
             
    if mapa.stepsFaltantes:  
        print ("FALTAN STEPS POR RECORRER!")
        mapa.respaldoGoal = mapa._goal 
        mapa._goal = mapa.inicioRestante = mapa.snakeCeldas[0]        
        print ("El inicio restante es", mapa.inicioRestante)
     
    c=agent(mapa,start[0],start[1],color='red',footprints=True) 
                         
    mapa.tracePath({c:camino},delay=mapa.snakeDelay,kill=True) 

def encerrado(mapa):
    if mapa.liberacion:
        mapa.respaldoObjetivo = mapa._objetivo
        mapa.respaldoGoal = mapa._goal
        #mapa.snakeDelay = 500       
        algoritmoLiberacion(mapa, mapa.snakeCeldas[0][0], mapa.snakeCeldas[0][1]) 
    else: 
        textLabel(mapa,'¡AY CARAMBA! ¡NO HAY CAMINO! - FIN DEL JUEGO - PUNTAJE TOTAL', mapa.snakeSize)
        
def crearObjetivo(mapa):
    defaultPath = [(22,25),(),(22,20),(25,20),(25,25),(22,25),(22,20),(25,20),(25,25),(22,25),(22,20),(25,20),(25,22),(10,10)]
    if mapa.caminoAleatorio:
        notValid = True
        while notValid:
            x = randrange(1,25,1)
            y = randrange(1,25,1)
            notValid = (x,y) in mapa.snakeCeldas
    else :
        x = defaultPath[mapa.getSnakeSize()][0]
        y = defaultPath[mapa.getSnakeSize()][1]
    
    mapa._objetivo= agent(mapa,x,y,color=COLOR.green)    
    mapa._goal = (x,y)    
    return (x, y)


def algoritmoLiberacion(mapa, x, y):    
    objetivo = objetivoLiberacion(mapa, x, y)
    mapa._goal = objetivo
    
    c=agent(mapa,x,y,color='red',footprints=True)

    print("snakeSize antes ALG", mapa.getSnakeSize())
    camino = calcularCamino(mapa, objetivo, (x,y), False)
    print("snakeSize despues ALG", mapa.getSnakeSize())
                            
    mapa.tracePath({c:camino},delay=mapa.snakeDelay,kill=True)

def objetivoLiberacion(mapa, x, y):
    celdaActual = (x, y)
    for d in 'ENWS':
        if mapa.maze_map[celdaActual][d]==True:            
            if d=='E':
                celdaVecina=(celdaActual[0],celdaActual[1]+1)                
            elif d=='W':
                celdaVecina=(celdaActual[0],celdaActual[1]-1)
            elif d=='N':
                celdaVecina=(celdaActual[0]-1,celdaActual[1])
            elif d=='S':
                celdaVecina=(celdaActual[0]+1,celdaActual[1])
            if celdaVecina not in mapa.snakeCeldas:
                print(f"Yendo para la {d}")
                break
    if celdaVecina not in mapa.snakeCeldas:
        return celdaVecina
    return