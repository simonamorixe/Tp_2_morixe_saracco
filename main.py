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

#Función para calcular el centroide que le corresponde a cada pixel.
def calcular_centroide_mas_cercano(pixel, centroides):

    

       
#Función para calcular los grupos de centroides
def calcular_grupos(img, centroides):
    alto, ancho, canales = img.shape

    #Diccionario vacío. El resultado debe verse de la siguiente manera:
    # grupos = {centroide1: [pixel1, pixel2, pixel3, ...], centroide2: [pixel4, pixel5, pixel6, ...]}
    grupos = {}

    #Se recorre la foto completa
    for x in range(ancho):
        for y in range(alto):
            pixel = img[x:y: ] #Pixel definido por el array de la imagen en las coordenadas(x,y,todo)

            centroide_mas_cercano = calcular_centroide_mas_cercano(pixel, centroides)


    return grupos



#Definir función kmeans con lo que devuelven las funciones base
def kmeans(img):
    #.shape guarda los valores del filas, columnas y canales
    alto, ancho, canales = img.shape

    k = pedir_k()

    #Con k definido, se deben crear los centroides.
    centroides = crear_centroides(img, k)

    #Con los centroides, se deben juntar los centroides en grupos, creo que son los clusters
    grupos_centroides = calcular_grupos(img, centroides)


    return


#--------------------------------------------------------------------------------------

def main():
   #Se solicita al usuario que ingrese la ruta de la imagen
   ruta_imagen = input("Ingrese la ruta de la imagen: ")
   img = abrir_imagen(ruta_imagen)
   
   #Verificación de una imagen válida
   if img is None:
      print("No se encontró la imagen. Por favor, verifique la ruta e intente nuevamente.")
      return #que devuelvo?
   
   opcion_elegida = elegir_opcion()
   if opcion_elegida == "halftone":
        
        pass #chequear si se puede usar el pass
   
   elif opcion_elegida == "kmeans":
        kmeans(img) #la funcion kmeans recibirá la imagen ingresada y comenzará a trabajar con ese input
        


#llama a la funcion main
if __name__ == '__main__':
    main()