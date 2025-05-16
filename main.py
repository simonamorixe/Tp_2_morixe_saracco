from PIL import Image
import math
import numpy as np
from funciones_kmeans import kmeans
from funciones_halftone import halftone

import random

#-------------------------------- GENERAL ---------------------------------------------
#Función que abre la imagen - completar docstrings
def abrir_imagen(ruta_imagen):
    """
    La funcion abrir_imagen abre una imagen y la convierte en un array de NumPy 
    si se puede abrir, devuelve 
    """
    try:
        imagen = Image.open(ruta_imagen).convert("RGB")
        return np.array(imagen)
        #Usamos la imagen como un array de datos
    
    except FileNotFoundError: 
        return None
        #devuelve un None para que luego imprima el Error





#--------------------------------------------------------------------------------------


#Se solicita al usuario que ingrese la ruta de la imagen
ruta_imagen = input("Ingrese la ruta de la imagen: ")
imagen = abrir_imagen(ruta_imagen)

while imagen is None:
    print("No se encontró la imagen. Por favor, verifique la ruta e intente nuevamente.")
    ruta_imagen = input("Ingrese la ruta de la imagen: ")
    imagen = abrir_imagen(ruta_imagen)


#Imprime las opciones posibles
print("1. Halftone")
print("2. K-means")
    
entrada = input("Seleccione el método de cuantización [1-2]: ")

while entrada !="1" and entrada !="2":
    print("Opción inválida, intente de nuevo.")
    entrada = input("Seleccione el método de cuantización [1-2]: ")
    
if entrada == "1":
    opcion_elegida = "halftone"
    halftone(imagen)
    
elif entrada == "2":
    opcion_elegida = "kmeans"
    kmeans(imagen)

    
    



   


    

