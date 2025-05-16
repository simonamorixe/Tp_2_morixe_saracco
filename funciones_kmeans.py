from PIL import Image
import math
import numpy as np
import random

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
        centroide = img[y, x, :] 

        #Se agrega cada color como tupla de enteros por si el array tiene valores diferentes a int
        centroides.append((int(centroide[0]), int(centroide[1]), int(centroide[2])))

    return centroides



#Función del calculo de distancia de un color a otro
def distancia_colores(colorA, colorB):
    distancia = (
        (int(colorA[0]) - int(colorB[0])) ** 2 + 
        (int(colorA[1]) - int(colorB[1])) ** 2 + 
        (int(colorA[2]) - int(colorB[2])) ** 2
        ) ** 0.5
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
            pixel = img[y,x, : ] 
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
            suma_R += int(pixel[0]) 
            suma_G += int(pixel[1])
            suma_B += int(pixel[2])

        total = len(pixeles)

        #Se agrega el centroide mas preciso a la lista de centroides
        centroide_nuevo = (suma_R//total, suma_G//total, suma_B//total)
        centroides.append(centroide_nuevo)

    return centroides


#Funcion para pintar la imagen negra por grupos de colores
def pintar_por_grupos(imagen_vieja, nueva_imagen, clusters):
    alto, ancho, canales = imagen_vieja.shape

    for x in range(ancho):
        for y in range(alto):
            #Se toma cada pixel y se lo compara con todos los centroides
            pixel = imagen_vieja[y,x, : ]
            color_representativo = calcular_centroide_mas_cercano(pixel, list(clusters.keys()))

            #Se colorea el pixel con el color correspondiente de su centroide
            nueva_imagen[y, x, : ] = color_representativo

    return nueva_imagen



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
        print(f"{i + 1}%")
        nuevos_centroides = promediar_grupos(clusters)

        #Si los centroides no se mueven, cortar el ciclo.
        if centroides == nuevos_centroides:
            break

        clusters = calcular_clusters(img, centroides)

    #Se crea una imagen negra, con todos los pixeles en 0, del mismo tamaño que la original
    nueva_imagen = np.zeros((alto, ancho, canales))

    imagen_final = Image.fromarray(pintar_por_grupos(img, nueva_imagen, clusters).astype(np.uint8))
    imagen_final.save("resultado.png")

    
        

