from libs.pymaze import maze

mapa=maze()
mapa.CreateMaze(loadMaze=r"D:\Dropbox\Maestria\IA\Proyecto\Codigo\Snake\mapa.csv")

MAX_STEPS = mapa.cols * mapa.rows


mapa.snakeDelay = 50
mapa.crece = True
mapa.caminoAleatorio = True
mapa.liberacion = False
mapa.steps = MAX_STEPS


mapa.configurarSnake()

mapa.run()