"""
    https://parzibyte.me/blog
"""
import numpy as np
import imageio
NOMBRE_IMAGEN = "travel.bmp"


def leer_imagen(ruta):
    return np.array(imageio.imread(ruta), dtype='int').tolist()


def guardar_imagen(ruta, matriz):
    return imageio.imwrite(ruta, np.array(matriz, dtype="uint8"))


def reflejo_horizontal(nombre_imagen):
    matriz = leer_imagen(nombre_imagen)
    ancho = len(matriz[0])
    alto = len(matriz)
    for y in range(alto):
        for x in range(int(ancho/2)):
            indice_opuesto = ancho - x - 1
            opuesto = matriz[y][indice_opuesto]
            actual = matriz[y][x]
            matriz[y][indice_opuesto] = actual
            matriz[y][x] = opuesto
    return matriz


def difuminado(nombre_imagen):
    matriz_original = leer_imagen(nombre_imagen)
    # Eliminar referencia para crear una nueva matriz
    matriz_difuminada = matriz_original[:]
    ancho = len(matriz_difuminada[0])
    alto = len(matriz_difuminada)
    for y in range(alto):
        for x in range(ancho):
            # Vamos a recorrer una mini matriz en la caja
            inicio_y = y-1
            inicio_x = x-1
            fin_y = y+1
            fin_x = x+1
            if inicio_y < 0:
                inicio_y = 0
            if inicio_x < 0:
                inicio_x = 0
            if fin_x >= ancho:
                fin_x = ancho - 1
            if fin_y >= alto:
                fin_y = alto - 1
            suma_red = 0
            suma_green = 0
            suma_blue = 0
            conteo = 0
            while inicio_y <= fin_y:
                indice_x = inicio_x
                while indice_x <= fin_x:
                    pixel_matriz_original = matriz_original[inicio_y][indice_x]
                    suma_red += pixel_matriz_original[0]
                    suma_green += pixel_matriz_original[1]
                    suma_blue += pixel_matriz_original[2]
                    indice_x += 1
                    conteo += 1
                inicio_y += 1
            promedio_red = round(suma_red/conteo)
            promedio_green = round(suma_green/conteo)
            promedio_blue = round(suma_blue/conteo)
            matriz_difuminada[y][x] = [
                promedio_red, promedio_green, promedio_blue]
    return matriz_difuminada


def escala_grises(nombre_imagen):
    matriz = leer_imagen(nombre_imagen)
    ancho = len(matriz[0])
    alto = len(matriz)
    for y in range(alto):
        for x in range(ancho):
            pixel = matriz[y][x]
            # El doble / es para dividir y redondear a entero
            promedio = (pixel[0] + pixel[1] + pixel[2])//3
            matriz[y][x][0] = promedio
            matriz[y][x][1] = promedio
            matriz[y][x][2] = promedio
    return matriz


def sepia(nombre_imagen):
    matriz = leer_imagen(nombre_imagen)
    ancho = len(matriz[0])
    alto = len(matriz)
    for y in range(alto):
        for x in range(ancho):
            pixel = matriz[y][x]
            original_rojo = pixel[0]
            original_verde = pixel[1]
            original_azul = pixel[2]
            sepia_rojo = round(0.393*original_rojo +
                               0.769*original_verde+0.189*original_azul)
            sepia_verde = round(0.349*original_rojo +
                                0.686*original_verde+0.168*original_azul)
            sepia_azul = round(0.272*original_rojo +
                               0.534*original_verde+0.131*original_azul)
            pixel_sepia = [sepia_rojo, sepia_verde, sepia_azul]
            for indice in range(len(pixel_sepia)):
                if pixel_sepia[indice] < 0:
                    pixel_sepia[indice] = 0
                elif pixel_sepia[indice] > 255:
                    pixel_sepia[indice] = 255
            matriz[y][x] = pixel_sepia
    return matriz


guardar_imagen("travel_sepia.bmp", sepia(NOMBRE_IMAGEN))
print("Imagen sepia guardada")
guardar_imagen("travel_grises.bmp", escala_grises(NOMBRE_IMAGEN))
print("Imagen escala de grises guardada")
guardar_imagen("travel_reflejo.bmp", reflejo_horizontal(NOMBRE_IMAGEN))
print("Imagen reflejo guardada")
guardar_imagen("travel_difuminada.bmp", difuminado(NOMBRE_IMAGEN))
print("Imagen difuminada guardada")
