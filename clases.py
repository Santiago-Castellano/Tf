"""
    SUPERVISOR: para mantener servicios andando constantemente.
"""
import cv2 as cv
import tensorflow.compat.v1 as tf
import random
import time
import asyncio
from concurrent.futures import ProcessPoolExecutor
executor = ProcessPoolExecutor(1)


class Interseccion():
    """
    Clase que contiene la informacion de una interseccion:
    Tiene las siguientes propiedades:
        - id: Identificador que se provee por parametro
        . cantidad_vehiculos: Metodo que te retornaria la cantidad de vehiculos en esa interseccion
        - directorio: Nombre de la carpeta de donde estara la imagen
        - tiempo_inactivo: Cada ronda que no le toque activarse se va a incrementar en 1
        - prioridad: Prioridad que tiene la interseccion sobre el resto.
    """
    def __init__(self, id, directorio, prioridad, tiempo_activacion):
        self.id = id
        self.tiempo_activacion = tiempo_activacion
        self.directorio = directorio
        self.prioridad = prioridad
        self.tiempo_inactivo = 0
        self.vehiculos = 0
        self.f = tf.gfile.FastGFile('frozen_inference_graph.pb', 'rb')
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(self.f.read())
        self.sess = tf.Session()
        self.sess.graph.as_default()
        tf.import_graph_def(graph_def, name='')

    async def cantidad_vehiculos(self):
        while True:
            self._cantidad_vehiculos()
            print(f"contando vehiculos inter: {self.id} Total: {self.vehiculos}")
            await asyncio.sleep(6)
    
    def _cantidad_vehiculos(self):
        img = cv.imread(self.obtener_imagen())
        inp = cv.resize(img, (300, 300))
        inp = inp[:, :, [2, 1, 0]]  # BGR2RGB

        out = self.sess.run([self.sess.graph.get_tensor_by_name('num_detections:0'),
                        self.sess.graph.get_tensor_by_name('detection_scores:0'),
                        self.sess.graph.get_tensor_by_name('detection_boxes:0'),
                        self.sess.graph.get_tensor_by_name('detection_classes:0')],
                    feed_dict={'image_tensor:0': inp.reshape(1, inp.shape[0], inp.shape[1], 3)})

        num_detections = int(out[0][0])

        self.vehiculos = num_detections

    def obtener_imagen(self):
        nro = random.randint(0,100)
        return f"{self.directorio}/{nro}.jpeg"


class Manejador():
    """
    Clase encargada de la logica de manejar los semaforos
    Paramentros de la clase:
        -Recibe como parametros una lista con las intersecciones que se van a manejar.
            La lista debe contener los objetos de la clase Interseccion.
    """
    def __init__(self, intersecciones):
        self.intersecciones = intersecciones
        self.activo = None

    async def seleccionar_interseccion(self):
        """
        Metodo encargado de la logica para seleccionar que interseccion continuara.
        """
        print("seleccionando interseccion")
        inter_max = self.intersecciones[0]
        for inter in self.intersecciones:
            if inter_max.vehiculos < inter.vehiculos:
                inter_max = inter

        self.activo = inter_max

    async def activar_semaforo(self):
        print(f"se activara el semaforo {self.activo.id}-\nPor {self.activo.tiempo_activacion} s. -\n Tiempo inactivo: {self.activo.tiempo_inactivo}")
        self.activo.tiempo_inactivo = 0
        for inter in self.intersecciones:
            if inter.id != self.activo.id:
                inter.tiempo_inactivo += 1

        await asyncio.sleep(self.activo.tiempo_activacion)

    def gestionar_transito(self):
        """
            Ver log
        """
        loop = asyncio.get_event_loop()
        try:
            for inter in self.intersecciones:
                asyncio.ensure_future(inter.cantidad_vehiculos())

            asyncio.ensure_future(self.step())
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()

    async def step(self):
        while True:
            await self.seleccionar_interseccion()                
            await self.activar_semaforo()
        #activo = self.seleccionar_interseccion()
        #self.activar_semaforo(activo)
