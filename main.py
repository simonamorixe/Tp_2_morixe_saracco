from PIL import Image
import math
import numpy as np
import funciones
import random

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

def angulo_puntos(): # ver esta funcion porque se esta ejecutando antes que el codigo principal
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
    nueva_imagen = np.zeros(img.shape) # Crea una matriz vacía (con ceros) del mismo tamaño que la original
    
    #recorre tres veces para cada canal rojo, verde y azul
    for i in range(3):
        angulo_canal = angulos[i] 

        coordenadas_puntos = get_grid_coords(alto, ancho, tamaño_punto, angulo_canal)

        #img[:,:,i] sigue el formato de alto,ancho,canales
        tamaños_puntos = calculo_radios(img[:,:,i], coordenadas_puntos, tamaño_punto) 

        matriz_base = np.full((alto, ancho), 255) #crea matriz blanca (intensidad:255) del mismo tamaño que la imagen
        matriz_punteada = poner_puntosnegros(matriz_base, coordenadas_puntos, tamaños_puntos)
        nueva_imagen[:, : ,i] = matriz_punteada # imagen_resultante[todo el alto, todo el ancho, el canal especifico]

    imagen_final = Image.fromarray(nueva_imagen.astype(np.uint8)) #comvierte matriz Numpy a imagen real para poder ver la imagen final con los puntos
    imagen_final.save("resultado.png")



            
#-------------------------------- K-MEANS ---------------------------------------------
COLORES_DEFAULT_KMEANS = 8

#Función para pedir k 

def pedir_k():
   while True:
       #Se solicita al usuario la cantidad de colores deseados.
       k = input("Ingrese el numero de colores deseados: ")

       #Si no se ingresa nada, se utilizan por default 8 colores.
       if k == "":
           return COLORES_DEFAULT_KMEANS
       
       if k.isdigit():
           return int(k)
       else:
           print("La cantidad de colores debe ser un numero.")


#Función para crear centroides
def crear_centroides(img, k):
    #Se vuelve a pedir las medidas de la foto
    alto, ancho, canales = img.shape

    #Con una lista vacía se crean centroides
    centroides = []

    for i in range(k):
        #Se eligen puntos x,y random dentro del tamaño de la imagen
        x = random.randint(0, ancho-1)
        y = random.randint(0, alto-1)
        centroide = img[x:y: ] #Los canales ya estan definidos??????

        #Se agrega cada color como tupla de enteros por si el array tiene valores np.uint8 o diferentes a int
        centroides.append((int(centroide[0]), int(centroide[1]), int(centroide[2])))

    return centroides



#Ambas funciones distancia_colores y calcular_centroides_mas_cercanos
#Función del calculo de distancia de un color a otro
def distancia_colores(colorA, colorB):
    distancia = ( (int(colorA[0]) - int(colorB[0])) ** 2 + (int(colorA[1]) - int(colorB[1])) ** 2 + (int(colorA[2]) - int(colorB[2])) ) ** 0.5
    return distancia


#Función para calcular el centroide que le corresponde a cada pixel.
def calcular_centroide_mas_cercano(pixel, centroides):
    centroide_mas_cercano = centroides[0]

    for centroide in centroides:
        # Evalua las distancias del pixel seleccionado con cada centroide
        if distancia_colores(pixel, centroide) < distancia_colores(pixel, centroide_mas_cercano):
            #Si encuentra un pixel mas cercano al nuevo centroide, se reemplaza como el centroide mas cercano.
            centroide_mas_cercano = centroide
            
    return centroide_mas_cercano


       
#Función para calcular los grupos de centroides
def calcular_clusters(img, centroides):
    alto, ancho, canales = img.shape

    #Diccionario vacío. El resultado debe verse de la siguiente manera:
    # clusters = {centroide1: [pixel1, pixel2, pixel3, ...], centroide2: [pixel4, pixel5, pixel6, ...]}
    # clusters = {(1,2,3): [pixel1, pixel2, pixel3], ...}

    clusters = {}

    #Se recorre la foto completa
    for x in range(ancho):
        for y in range(alto):
            pixel = img[y, x, : ] #Pixel definido por el array de la imagen en las coordenadas(alto,ancho,canales)

            # comentar
            centroide_mas_cercano = tuple(calcular_centroide_mas_cercano(pixel, centroides))

            #Debo revisar si el centroide ya esta como clave del diccionario
            #Si el centroide ya esta como clave, agrego el pixel al diccionario
            if centroide_mas_cercano in clusters:
                clusters[centroide_mas_cercano].append(pixel)
            
            #Sino, creo una clave para el centroide y luego le agrego los pixeles 
            else:
                clusters[centroide_mas_cercano] = []
                clusters[centroide_mas_cercano].append(pixel)

    return clusters


#Función para promediar los grupos de pixeles para cada centroide (clusters) y buscar los centroides finales
def promediar_grupos(clusters):
    centroides = []

    #Recorro el diccionario de clusters
    for centroide_viejo, pixeles in clusters.items():
        suma_R = 0
        suma_G = 0
        suma_B = 0

        #Por cada pixel correspondiente al centroide, se suman las coordenadas para sacar un promedio 
        for pixel in pixeles:
            suma_R += pixel[0] # no se si deberia ser un int
            suma_G += pixel[1]
            suma_B += pixel[2]

        total = len(pixeles)

        #Se agrega el centroide mas preciso a la lista de centroides
        centroide_nuevo = (suma_R//total, suma_G//total, suma_B//total)
        centroides.append(centroide_nuevo)

    return centroides


#Funcion para pintar la imagen negra por grupos de colores
def pintar_por_grupos():
    return



#Definir función kmeans con lo que devuelven las funciones base
def kmeans(img):
    #.shape guarda los valores del filas, columnas y canales
    alto, ancho, canales = img.shape

    k = pedir_k()

    #Con k definido, se deben crear los centroides.
    centroides = crear_centroides(img, k)

    #Con los centroides, se deben juntar los centroides en grupos de pixeles, que son los clusters
    clusters = calcular_clusters(img, centroides)

    #Con los grupos de centroides calculados, se deben realizar las iteraciones

    for i in range(10): # voy a probarlo con 10 asi no tarda tanto
        nuevos_centroides = promediar_grupos(clusters)

        #Si los centroides no se mueven, cortar el ciclo.
        if centroides == nuevos_centroides:
            break

        clusters = calcular_clusters(img, centroides)

    #Se crea una imagen negra, con todos los pixeles en 0, del mismo tamaño que la original
    nueva_imagen = np.zeros((alto, ancho, canales))

    imagen_final = pintar_por_grupos()
        



#--------------------------------------------------------------------------------------


#Se solicita al usuario que ingrese la ruta de la imagen
ruta_imagen = input("Ingrese la ruta de la imagen: ")
img = abrir_imagen(ruta_imagen)

#Verificación de una imagen válida
if img is None:
    print("No se encontró la imagen. Por favor, verifique la ruta e intente nuevamente.")
   

opcion_elegida = elegir_opcion()
if opcion_elegida == "halftone":
    halftone(img)

elif opcion_elegida == "kmeans":
    kmeans(img) #la funcion kmeans recibirá la imagen ingresada y comenzará a trabajar con ese input
    

