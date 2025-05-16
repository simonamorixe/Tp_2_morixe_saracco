from PIL import Image
import math
import numpy as np
from funciones_kmeans import kmeans

import random

#-------------------------------- GENERAL ---------------------------------------------
#Función que abre la imagen - completar docstrings
def abrir_imagen(ruta_imagen):
    """
    La funcion abrir_imagen abre una imagen y la convierte en un array de NumPy 
    si se puede abrir, devuelve 
    """
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


#--------------------------------------------------------------------------------------


#Se solicita al usuario que ingrese la ruta de la imagen
ruta_imagen = input("Ingrese la ruta de la imagen: ")
imagen = abrir_imagen(ruta_imagen)

while imagen is None:
    print("No se encontró la imagen. Por favor, verifique la ruta e intente nuevamente.")
    ruta_imagen = input("Ingrese la ruta de la imagen: ")
    imagen = abrir_imagen(ruta_imagen)



opcion_elegida = elegir_opcion()

if opcion_elegida == "halftone":
    halftone(imagen)

elif opcion_elegida == "kmeans":
    kmeans(imagen) 

    



   


    

