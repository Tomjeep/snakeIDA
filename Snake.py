from libs.pymaze import maze

m=maze()
m.CreateMaze(loadMaze=r"D:\Dropbox\Maestria\IA\Proyecto\Codigo\Snake\mapa.csv")

MAX_STEPS = m.cols * m.rows


m.snakeDelay = 1000
m.caminoAleatorio = True
m.liberacion = False
m.steps = MAX_STEPS

m.configurarSnake()

m.run()