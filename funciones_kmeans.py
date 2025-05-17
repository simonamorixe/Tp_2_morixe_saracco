from PIL import Image
import numpy as np
import random

#-------------------------------- K-MEANS ---------------------------------------------
COLORES_DEFAULT_KMEANS = 8

#Función para pedir k.
def pedir_k():
   """
   La función solicita al usuario la cantidad de colores deseados.
   Si no se ingresa nada, se utilizan por default 8 colores.
   La función devuelve el numero a utilizar.
   """
   while True:
       k = input("Ingrese el numero de colores deseados: ")

       if k == "":
           return COLORES_DEFAULT_KMEANS
       
       if k.isdigit():
           return int(k)
       else:
           print("La cantidad de colores debe ser un numero.")


#Función para crear centroides.
def crear_centroides(img, k):
    """
    La función recibe el array de la imagen y el numero de colores a utilizar.
    Se piden las medidas de la foto y se eligen centroides aleatorios.
    La función devuelve una lista de k centroides.
    """
    alto, ancho, canales = img.shape

    # Con una lista vacía se crean centroides.
    centroides = []

    for i in range(k):
        # Se eligen puntos x,y random dentro del tamaño de la imagen.
        x = random.randint(0, ancho-1)
        y = random.randint(0, alto-1)
        centroide = img[y, x, :] 

        # Se agrega cada color como tupla de enteros por si el array tiene valores diferentes a int.
        centroides.append((int(centroide[0]), int(centroide[1]), int(centroide[2])))

    return centroides



#Función del calculo de distancia de un color a otro.
def distancia_colores(colorA, colorB):
    """
    La función recibe 2 colores, calcula la distancia entre ambos y devuelve el resultado.
    """
    distancia = (
        (int(colorA[0]) - int(colorB[0])) ** 2 + 
        (int(colorA[1]) - int(colorB[1])) ** 2 + 
        (int(colorA[2]) - int(colorB[2])) ** 2
        ) ** 0.5
    return distancia


#Función para calcular el centroide que le corresponde a cada pixel.
def calcular_centroide_mas_cercano(pixel, centroides):
    """
    La función recibe un pixel y los centroides creados y evalua la cercanía del pixel a cada centroide.
    Se retorna el centroide al cual corresponde el pixel seleccionado.
    """
    centroide_mas_cercano = centroides[0]

    for centroide in centroides:
        # Evalua las distancias del pixel seleccionado con cada centroide.
        if distancia_colores(pixel, centroide) < distancia_colores(pixel, centroide_mas_cercano):
            # Si encuentra un pixel mas cercano al nuevo centroide, se reemplaza como el centroide mas cercano.
            centroide_mas_cercano = centroide
            
    return centroide_mas_cercano


       
#Función para calcular los grupos de centroides.
def calcular_clusters(img, centroides):
    """
    La función recibe el array de la imagen y los centroides.
    Calcula las medidas de la imagen y crea un diccionario vacío de grupos de colores.
    Se agregan como claves del diccionario todos los centroides y sus pixeles correspondientes.
    La función devuelve el diccionario completo luego de recorrer toda la imagen.
    """
    alto, ancho, canales = img.shape

    # Diccionario vacío. El resultado debe verse de la siguiente manera:
    # clusters = {centroide1: [pixel1, pixel2, pixel3, ...], centroide2: [pixel4, pixel5, pixel6, ...]}.
    # clusters = {(1,2,3): [pixel1, pixel2, pixel3], ...}.

    clusters = {}

    # Se recorre la foto completa.
    for x in range(ancho):
        for y in range(alto):
            pixel = img[y,x, : ] 
            centroide_mas_cercano = tuple(calcular_centroide_mas_cercano(pixel, centroides))

            # Analiza si el centroide ya esta como clave del diccionario.
            # Si la clave ya existe, se agrega el pixel al diccionario.
            if centroide_mas_cercano in clusters:
                clusters[centroide_mas_cercano].append(pixel)
            
            # Sino, se crea una clave para el centroide y luego se agregan los pixeles.
            else:
                clusters[centroide_mas_cercano] = []
                clusters[centroide_mas_cercano].append(pixel)

    return clusters


#Función para promediar los grupos de pixeles para cada centroide (clusters).
def promediar_grupos(clusters):
    """
    La función recibe el diccionario de grupos de colores y calcula un promedio para cada coordenada.
    Se crea un nuevo centroide con el promedio calculado y se agrega a una lista de centroides.
    La función devuelve la lista con los nuevos centroides.
    """
    centroides = []

    # Se recorre el diccionario de clusters.
    for centroide_viejo, pixeles in clusters.items():
        suma_R = 0
        suma_G = 0
        suma_B = 0

        # Por cada pixel del cluster se suman los valores de cada componente de color.
        for pixel in pixeles:
            suma_R += int(pixel[0]) 
            suma_G += int(pixel[1])
            suma_B += int(pixel[2])

        total = len(pixeles)

        # Se realiza el promedio y se guarda como nuevo centroide.
        centroide_nuevo = (suma_R//total, suma_G//total, suma_B//total)
        centroides.append(centroide_nuevo)

    return centroides


#Funcion para pintar la imagen negra por grupos de colores.
def pintar_por_grupos(imagen_vieja, nueva_imagen, clusters):
    """
    La función recibe la imagen original, una imagen vacía (o negra) y el diccionario de clusters.
    Se recorre la imagen original y se pinta pixel de la nueva imagen con el color del centroide mas cercano.
    La función devuelve la nueva imagen pintada con los colores correspondientes.
    """
    alto, ancho, canales = imagen_vieja.shape

    for x in range(ancho):
        for y in range(alto):
            # Se obtiene el valor del pixel en la imagen original.
            pixel = imagen_vieja[y,x, : ]

            # Se calcula el centroide mas cercano a ese pixel.
            color_representativo = calcular_centroide_mas_cercano(pixel, list(clusters.keys()))

            # Se colorea el pixel en la nueva imagen con el color de su centroide mas cercano.
            nueva_imagen[y, x, : ] = color_representativo

    return nueva_imagen



#Definir función kmeans con lo que devuelven las funciones base.
def kmeans(img):
    """
    La función recibe la imagen como array y aplica el algoritmo para reducir la cantidad de colores.
    Se solicita un valor de k, para generar centroides iniciales y agrupar los pixeles en clusters. 
    Se itera 100 veces y se actualizan los centroides.
    Se genera una nueva imagen con los colores representativos.
    La función no retorna nada, pero guarda la imagen como un archivo nuevo.
    """
    # Se obtienen las dimensiones de la imagen.
    alto, ancho, canales = img.shape

    # Se solicita la cantidad de colores.
    k = pedir_k()

    # Con k definido, se crean los centroides iniciales.
    centroides = crear_centroides(img, k)

    # Se asignan los pixeles a los centroides mas cercanos.
    clusters = calcular_clusters(img, centroides)

    # Se itera en un maximo de 100 veces para ajustar los centroides hasta que estabilicen.
    for i in range(100): 
        print(f"{i + 1}%")
        nuevos_centroides = promediar_grupos(clusters)

        # Si los centroides no se mueven, se corta el ciclo.
        if centroides == nuevos_centroides:
            break

        centroides = nuevos_centroides # ver esto
        clusters = calcular_clusters(img, centroides)

    # Se crea una imagen negra, con todos los pixeles en 0, del mismo tamaño que la original.
    nueva_imagen = np.zeros((alto, ancho, canales))

    # Se pinta la imagen con los colores promedio de cada cluster.
    imagen_final = Image.fromarray(pintar_por_grupos(img, nueva_imagen, clusters).astype(np.uint8))

    # Se guarda la imagen para mostrar el resultado.
    imagen_final.save("resultado.png")