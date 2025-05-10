from PIL import Image
import math
import numpy as np



def cargar_imagen(ruta):
    """
    La funcion cargar_imagen abre la imagen dada por el usuario y verifica que se pueda usar, si la imagen es png 
    retorna la imagen cargada, sino retorna None
    """
    try:
        imagen = Image.open(ruta)
        return imagen
    except:
        print("No se pudo abrir la imagen.")
        return None

 
def medidas(imagen):
    """
    La funcion medidias busca el ancho y el alto de la imagen a partir de una funcion de la libreria pillow
    Retorna estos parametros para luego usarlos en otras funciones
    """
    ancho, alto= imagen.size()
    return ancho, alto 

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

