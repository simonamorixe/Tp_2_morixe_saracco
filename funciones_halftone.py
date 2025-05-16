from PIL import Image
import math
import numpy as np

def tamaño_puntos():
    while True:
        tamaño=input("Ingrese el tamaño del punto:")
        if tamaño=="":
            return 5 #tamaño por default
        elif tamaño.isdigit():
            return int(tamaño) #lo paso de str a int
        else:
            print("Ingrese un numero entero")

def angulo_puntos(): # ver esta funcion porque se esta ejecutando antes que el codigo principal, esta puesta 2 veces en las funcioones
     while True:
         angulos=input("Ingrese los angulos separados por comas:").split(",") 
         if angulos==[""]:
            #angulos por default
            return [15,45,0] 
        
         lista_angulos=[]

         #recorre lista que me devuelve el input con el split 
         for angulo in angulos: 
            if angulo.isdigit():
                #paso str a int para que quede como un valor numerico y despues poder utilizarlo
                lista_angulos.append(int(angulo)) 

         if len(lista_angulos)!=3:
            print("Tiene que ingresar 3 angulos")
         else:
            return lista_angulos
         
def get_grid_coords(h, w, dot_size, angle_deg):
    positions = []
    angle_rad = math.radians(angle_deg)
    cx, cy = w / 2, h / 2 # centro de la imagen

    # calcular la dimension de la grilla
    diag = int(math.hypot(w, h))
    num_x = diag // dot_size + 3
    num_y = diag // dot_size + 3

    # alinear el centro de la grilla con el centro de la imagen
    offset_x = cx - (num_x * dot_size) / 2
    offset_y = cy - (num_y * dot_size) / 2

    # recorrer la grilla y calcular las posiciones 
    for i in range(num_y):
        for j in range(num_x):
            gx = offset_x + j * dot_size + dot_size / 2 - cx
            gy = offset_y + i * dot_size + dot_size / 2 - cy
            rx = gx * math.cos(angle_rad) - gy * math.sin(angle_rad) + cx
            ry = gx * math.sin(angle_rad) + gy * math.cos(angle_rad) + cy

            ix, iy = int(round(rx)), int(round(ry))
            if 0 <= iy < h and 0 <= ix < w:
                positions.append((ix, iy))
    return positions


def calculo_radios(canales,positions,tamaño):
   lista_radios = []
   for coordenada in positions: #recorre la lista de tuplas
        x = coordenada[0] #asigno la variable a partir de la posicon 0 de la tupla
        y = coordenada[1] #idem x
        intensidad = canales[y, x] #busco la intensidad a partir de la posicion en la matriz con los canales
        radio = (1 - intensidad / 255) * tamaño * 0.7 #calculo de radio dado por el enunciado
        lista_radios.append(radio) 

   return lista_radios

def poner_puntosnegros(matriz_base, positions, lista_radios):
    alto,ancho = matriz_base.shape 

    #recorro posiciones y radios a la vez
    for coordenada,radio in zip(positions, lista_radios): 
        x = coordenada[0]
        y = coordenada[1]

        #funcion de math que redondea hacia arriba
        radio_int = math.ceil(radio) 
        
        for coord_x in range(x - radio_int - 1, x + radio_int + 1): 
            for coord_y in range(y - radio_int - 1, y + radio_int + 1):
                if 0 <= coord_x < ancho and 0 <= coord_y < alto:
                    if ((coord_x - x) ** 2) + ((coord_y - y) ** 2) <= radio ** 2:
                        matriz_base[coord_y, coord_x] = 0

    return matriz_base
    
def halftone(img):
    """
    Por cada canal, 
        Hacer la matriz blanca
        Hacer los puntos negros
        Guardar la imagen en el canal correcto
    """
    #llamo funciones para luego usar las variables como argumento de las demas funciones
    alto,ancho,canales = img.shape
    tamaño_punto = tamaño_puntos()
    angulos = angulo_puntos() 

   #Crea una matriz vacía (con ceros) del mismo tamaño que la original
    nueva_imagen = np.zeros(img.shape)
    
    #recorre tres veces para cada canal rojo, verde y azul
    for i in range(3):

      #toma el angulo en determinada posicion para el canal i 
      angulo_canal = angulos[i] 

      coordenadas_puntos = get_grid_coords(alto, ancho, tamaño_punto, angulo_canal)

      #img[:,:,i] sigue el formato de alto,ancho,canales
      tamaños_puntos = calculo_radios(img[:,:,i], coordenadas_puntos, tamaño_punto) 

      #crea matriz blanca (intensidad:255) del mismo tamaño que la imagen
      matriz_base = np.full((alto, ancho), 255) 

      matriz_punteada = poner_puntosnegros(matriz_base, coordenadas_puntos, tamaños_puntos)

      #inserta matriz_punteada en el canal i de la imagen final [todo el alto, todo el ancho, el canal especifico]
      nueva_imagen[:, : ,i] = matriz_punteada 

   #convierte matriz Numpy a imagen real para poder ver la imagen final con los puntos
    imagen_final = Image.fromarray(nueva_imagen.astype(np.uint8)) 
    imagen_final.save("resultado.png")


