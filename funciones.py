from PIL import Image
import math
import numpy as np



#-------------------------------- GENERAL ---------------------------------------------
#Función que abre la imagen - completar docstrings
def abrir_imagen(ruta_imagen):
    try:
        imagen = Image.open(ruta_imagen)
        return np.array(imagen)
        #Usamos la imagen como un array de datos
    
    except FileNotFoundError: 
        return None
        #devuelve un None para que luego imprima el Error


#Función en la que el usuario selecciona que estilo de imagen quiere 
def elegir_opcion():
    #Imprime las opciones posibles
    print("1. Halftone")
    print("2. K-means")
    
    while True:
        entrada = input("Seleccione el método de cuantización [1-2]: ")

        if entrada == "1":
            return "halftone"
        elif entrada == "2":
            return "kmeans"
        else:
            print("Opción inválida, intente de nuevo.")

#-------------------------------- HALFTONE ---------------------------------------------
def tamaño_puntos():
    while True:
        tamaño=input("Ingrese el tamaño del punto:")
        if tamaño=="":
            return 5 #tamaño por default
        elif tamaño.isdigit():
            return int(tamaño) #lo paso de str a int
        else:
            print("Ingrese un numero entero")

def angulo_puntos():
     while True:
         angulos=input("Ingrese los angulos separados por comas:").split(",") 
         if angulos==[""]:
            return [15,45,0] #angulos por default
        
         lista_angulos=[]
         for angulo in angulos: #recorro la "listita" que me devuelve el input con el split (borrar comentario dsp)
            if angulo.isdigit():
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

    # recorrer la grilla y calcular las posiciones (geometría 👻) 
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
    for coordenada,radio in zip(positions, lista_radios): #recorro posiciones y radios a la vez
        x = coordenada[0]
        y = coordenada[1]
        radio_int = math.ceil(radio) #funcion de math que redondea hacia arriba
        
        for coord_x in range(x - radio_int - 1, x + radio_int + 1): 
            for coord_y in range(y - radio_int - 1, y + radio_int + 1):
                if 0 <= coord_x < ancho and 0 <= coord_y < alto:
                    if ((coord_x - x) ** 2) + ((coord_y - y) ** 2) <= radio ** 2:
                        matriz_base[coord_y, coord_x] = 0

    return matriz_base
    


 
def medidas(imagen):
    """
    La funcion medidias busca el ancho y el alto de la imagen a partir de una funcion de la libreria pillow
    Retorna estos parametros para luego usarlos en otras funciones
    """
    ancho, alto= imagen.size()
    return ancho, alto 


#--------------------------------------------------------------------------------------

"""
tenemos que crear funcion que analice la imagen y saque el ancho y alto para meterlo despues en la funcion de halftone
el dot_size y el angle_deg te lo da el usuario como input.
el usuario tambien nos dice que tipo de filtro le quiere poner
"""


#FILTRO HALFTONE
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

    # recorrer la grilla y calcular las posiciones (geometría 👻) 
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


