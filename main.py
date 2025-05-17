from PIL import Image
import numpy as np
from funciones_kmeans import kmeans
from funciones_halftone import halftone


#--------------------------- FUNCIONES GENERALES -----------------------------------

#Función que abre la imagen 
def abrir_imagen(ruta_imagen):
    """
    La funcion abrir_imagen abre una imagen y la convierte en un array de NumPy 
    Si se puede abrir, retorna la imagen en array.
    Si no se puede abrir, retorna none
    """
    try:
        imagen = Image.open(ruta_imagen).convert("RGB")
        return np.array(imagen)
        # Se usa la imagen como un array de datos.
    
    except FileNotFoundError: 
        return None
        # Devuelve un None para que luego imprima el Error.


#-------------------------- CÓDIGO PRINCIPAL --------------------------------------


# Se solicita al usuario que ingrese la ruta de la imagen.
ruta_imagen = input("Ingrese la ruta de la imagen: ")
imagen = abrir_imagen(ruta_imagen)

while imagen is None:
    print("No se encontró la imagen. Por favor, verifique la ruta e intente nuevamente.")
    ruta_imagen = input("Ingrese la ruta de la imagen: ")
    imagen = abrir_imagen(ruta_imagen)

# Imprime las opciones posibles.
print("1. Halftone")
print("2. K-means")
    
entrada = input("Seleccione el método de cuantización [1-2]: ")


# Verifica que la entrada sea valida.
while entrada !="1" and entrada !="2":
    print("Opción inválida, intente de nuevo.")
    entrada = input("Seleccione el método de cuantización [1-2]: ")
    
# Para cada valor se ejecuta una opcion diferente.
if entrada == "1":
    halftone(imagen)
    
elif entrada == "2":
    kmeans(imagen)

    
    



   


    

