from libs.pymaze import maze

m=maze()
m.CreateMaze(loadMaze=r"D:\Dropbox\Maestria\IA\Proyecto\Codigo\Snake\mapa.csv")

MAX_STEPS = m.cols * m.rows


m.snakeDelay = 100
m.caminoAleatorio = True
m.liberacion = False
m.steps = 5#MAX_STEPS

m.configurarSnake()

m.run()