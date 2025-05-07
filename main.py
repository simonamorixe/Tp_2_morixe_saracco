from PIL import Image
import math
import numpy as np
import funciones
import random


 
# c

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
        pass

   
