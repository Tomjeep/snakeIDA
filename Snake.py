from libs.pymaze import maze

m=maze()
m.CreateMaze(loadMaze=r"D:\Dropbox\Maestria\IA\Proyecto\Codigo\Snake\mapa.csv")

m.snakeDelay = 1
m.liberacion = False

m.configurarSnake()

m.run()