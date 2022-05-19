from libs.agent import agent,textLabel
from libs.color import COLOR
from AEstrella import *
from random import randrange

def cicloSnake(maze, cabeza):
    tempx = maze.snakeCeldas[0][0]#maze._objetivo.x
    tempy = maze.snakeCeldas[0][1]#maze._objetivo.y
    
    if not maze.respaldoObjetivo:
        maze._canvas.delete(maze._objetivo._head)
        objetivo = crearObjetivo(maze)
    else:
        maze._objetivo = maze.respaldoObjetivo
        maze._goal = maze.respaldoGoal
        objetivo = maze._goal
        maze.respaldoObjetivo = ()
        maze.respaldoGoal = ()   
    
    camino = aEstrella(maze, objetivo, (tempx,tempy), True)    
    if camino == None:
        encerrado(maze)      
        return 
    
    maze.snakeSize += 1
    maze._canvas.delete(cabeza)
    c=agent(maze,tempx,tempy,color='red',footprints=True)
                        
    maze.tracePath({c:camino},delay=maze.snakeDelay,kill=True)

def encerrado(maze):
    if maze.liberacion:
        maze.respaldoObjetivo = maze._objetivo
        maze.respaldoGoal = maze._goal
        maze.snakeDelay = 500       
        algoritmoLiberacion(maze, maze.snakeCeldas[0][0], maze.snakeCeldas[0][1]) 
    else: 
        textLabel(maze,'¡AY CARAMBA! ¡NO HAY CAMINO! - FIN DEL JUEGO - PUNTAJE TOTAL', maze.snakeSize)
        
def crearObjetivo(maze):
    defaultPath = [(22,25),(),(22,20),(25,20),(25,25),(22,25),(22,20),(25,20),(25,25),(22,25),(22,20),(25,20),(25,22),(10,10)]
    if maze.caminoAleatorio:
        notValid = True
        while notValid:
            x = randrange(1,25,1)
            y = randrange(1,25,1)
            notValid = (x,y) in maze.snakeCeldas
    else :
        x = defaultPath[maze.getSnakeSize()][0]
        y = defaultPath[maze.getSnakeSize()][1]
    
    maze._objetivo= agent(maze,x,y,color=COLOR.green)    
    maze._goal = (x,y)    
    return (x, y)


def algoritmoLiberacion(maze, x, y):    
    objetivo = objetivoLiberacion(maze, x, y)
    maze._goal = objetivo
    
    c=agent(maze,x,y,color='red',footprints=True)

    print("snakeSize antes ALG", maze.getSnakeSize())
    camino = aEstrella(maze, objetivo, (x,y), False)
    print("snakeSize despues ALG", maze.getSnakeSize())
                            
    maze.tracePath({c:camino},delay=maze.snakeDelay,kill=True)

def objetivoLiberacion(maze, x, y):
    celdaActual = (x, y)
    for d in 'ENWS':
        if maze.maze_map[celdaActual][d]==True:            
            if d=='E':
                celdaVecina=(celdaActual[0],celdaActual[1]+1)                
            elif d=='W':
                celdaVecina=(celdaActual[0],celdaActual[1]-1)
            elif d=='N':
                celdaVecina=(celdaActual[0]-1,celdaActual[1])
            elif d=='S':
                celdaVecina=(celdaActual[0]+1,celdaActual[1])
            if celdaVecina not in maze.snakeCeldas:
                print(f"Yendo para la {d}")
                break
    if celdaVecina not in maze.snakeCeldas:
        return celdaVecina
    return