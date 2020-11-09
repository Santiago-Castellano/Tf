from clases import Manejador,Interseccion

if __name__ == "__main__":
    inter_1 = Interseccion(1,'nombre_1',1)
    inter_2 = Interseccion(2,'nombre_2',1)
    inter_3 = Interseccion(3,'nombre_3',1)
    inter_4 = Interseccion(4,'nombre_4',1)
    intersecciones = [inter_1,inter_2,inter_3,inter_4]
    manejador = Manejador(intersecciones,5,10)
    manejador.gestionar_transito()
