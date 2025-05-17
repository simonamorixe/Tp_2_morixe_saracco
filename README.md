# Tp_2_morixe_saracco

## Introducción
El proyecto propone un algoritmo para generar imagenes a partir de una foto base. El usuario selecciona el tipo de formato que desea para generar la imagen y luego el programa ejecuta el codigo correspondiente a la opción seleccionada.

Luego de la ejecución, el usuario decidirá que imagen utilizará como imagen final.


## Composición
El proyecto esta compuesto por tres archivos de codigo:

    - funciones_halftone.py (funciones que ejecutan el codigo perteneciente al Filtro Halftone)
    - funciones_kmeans.py (funciones que ejecutan el codigo de la Cuantización K-Means)
    - main.py (codigo principal que importa los archivos de funciones y ejecuta el programa completo)

Además, contiene un archivo README.md (archivo actual)


## Descripción
El proyecto implementa dos metodos de cuantización de imagenes: 

- **Filtro Halftone**
- **Cuantización K-Means**

Ambos métodos buscan reducir la cantidad de colores y la calidad de la imagen, preservando a su vez la estetica visual.

# 1. Halftone
Halftone simula una impresión por puntos de diferentes tamaños para cada canal RGB de la imagen de entrada.

# 2. K-Means
K-Means reduce los colores de la imagen original, agrupando los pixeles similares y asignandolos a centroides.


Al finalizar, se muestra la imagen y se guarda el resultado para que el usuario evalue que metodo prefiere utilizar.
---


## ▶️ Instrucciones de uso

1. El usuario debe ingresar la ruta de la imagen en el input mostrado en pantalla.
    - Si la imagen no el válida, se pedirá de nuevo una ruta hasta que la imagen se pueda abrir.

2. El usuario debe seleccionar el método que desea para generar la nueva imagen.
    - Mientras el usuario no ingrese una opción valida, se volverá a pedir el input.

    - Si se elige la opción de Halftone:
        - El usuario deberá ingresar el tamaño del punto deseado. (Si no hay input, se utilizará el valor default (5).)
        - El usuario deberá ingresar los angulos deseados, separados por comas. (Si no hay input, se utilizará el valor default ([15,45,0]).)
        - Una vez terminado, se guardará la imagen como un archivo llamando "resultado.png"


    - Si se elige la opción de K-Means:
        - El usuario deberá ingresar la cantidad de colores deseada. (Si no hay input, se utilizará el valor default (8).)
        - Se mostrará en pantalla el porcentaje de evolución del proceso.
        - Una vez terminado, se guardará la imagen como un archivo llamando "resultado.png"

3. Luego de la ejecución, el usuario deberá elegir el formato que prefiere para su imagen.


