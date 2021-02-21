from clases import Manejador,Interseccion

if __name__ == "__main__":
    inter_1 = Interseccion(1,'images',1,10)
    inter_2 = Interseccion(2,'images',1,10)
    inter_3 = Interseccion(3,'images',1,10)
    inter_4 = Interseccion(4,'images',1,10)
    intersecciones = [inter_1,inter_2,inter_3,inter_4]
    manejador = Manejador(intersecciones)
    manejador.gestionar_transito()
