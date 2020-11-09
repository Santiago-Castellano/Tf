import random
import time

class Interseccion():
    """
    Clase que contiene la informacion de una interseccion:
    Tiene las siguientes propiedades:
        - id: Identificador que se provee por parametro
        . cantidad_vehiculos: Metodo que te retornaria la cantidad de vehiculos en esa interseccion
        - nombre_imagen: Nombre de la imagen de donde debera ver la cantidad de vehiculos        
        - tiempo_inactivo: Cada ronda que no le toque activarse se va a incrementar en 1
        - prioridad: Prioridad que tiene la interseccion sobre el resto.
    """
    def __init__(self,id,nombre_imagen,prioridad):
        self.id = id
        self.tiempo_inactivo = 0
        self.nombre_imagen = nombre_imagen
        self.prioridad = prioridad
    
    def cantidad_vehiculos(self):
        return random.randint(1,10)


class Manejador():
    """
    Clase encargada de la logica de manejar los semaforos
    Paramentros de la clase:
        -Recibe como parametros una lista con las intersecciones que se van a manejar. 
            La lista debe contener los objetos de la clase Interseccion.
        -tiempo_asignado: tiempo que se le asigno a la interseccion para estar en verde
        -activo: interseccion que esta activa. 
        -asignacion_minima: valor minimo de tiempo que se le puede asignar a una interseccion.
        -asignacion_maxima: valor maximo de tiempo que se le puede asignar a una interseccion.
    """
    def __init__(self, intersecciones,asignacion_minima,asignacion_maxima):
        self.intersecciones = intersecciones
        self.tiempo_asignado = 0
        self.activo = None
        self.asignacion_minima = asignacion_minima
        self.asignacion_maxima = asignacion_maxima
    
    def seleccionar_interseccion(self):
        """
        Metodo encargado de la logica para seleccionar que interseccion continuara y cuanto tiempo.
        Retorna: (tiempo,interseccion)
        """
        return random.randint(self.asignacion_minima,self.asignacion_maxima), random.choice(self.intersecciones)
    
    def activar_semaforo(self):
        print(f"se activara el semaforo {self.activo.id} - durante {self.tiempo_asignado} s.-\n Tiempo inactivo: {self.activo.tiempo_inactivo}")
        self.activo.tiempo_inactivo = 0
        for inter in self.intersecciones:
            if inter.id != self.activo.id:
                inter.tiempo_inactivo += 1

        time.sleep(self.tiempo_asignado)

    def gestionar_transito(self):
        while True:
            self.tiempo_asignado, self.activo = self.seleccionar_interseccion()
            self.activar_semaforo()