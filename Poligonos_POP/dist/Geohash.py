import os
import xml.etree.ElementTree as ET
from shapely.geometry import Polygon, Point
import pygeohash as pgh
import json
import sys

def analizar_kml(ruta_archivo):
    """
    Lee un archivo .kml y extrae los nombres y coordenadas de los polígonos.
    """
    arbol = ET.parse(ruta_archivo)
    raiz = arbol.getroot()
    espacio_nombres = {"kml": "http://www.opengis.net/kml/2.2"}

    poligonos = []

    for marca in raiz.findall(".//kml:Placemark", espacio_nombres):
        nombre = marca.find("kml:name", espacio_nombres).text
        coordenadas = marca.find(".//kml:coordinates", espacio_nombres).text.strip()
        coords = [
            tuple(map(float, coord.split(",")[:2]))
            for coord in coordenadas.split()
        ]
        poligonos.append({"nombre": nombre, "coordenadas": coords})

    return poligonos

def calcular_tamano_paso(precision):
    """
    Calcula el tamaño del paso en función de la precisión del geohash.
    """
    tamanos_paso = {
        5: 0.01,
        6: 0.005,
        7: 0.0025,
        8: 0.001,
        9: 0.00025
    }
    return tamanos_paso.get(precision, 0.00025)

def generar_geohashes_para_poligono(coordenadas_poligono, precision=9):
    """
    Genera geohashes para un polígono definido por sus coordenadas.
    """
    poligono = Polygon(coordenadas_poligono)
    min_lon, min_lat, max_lon, max_lat = poligono.bounds
    paso = calcular_tamano_paso(precision)
    geohashes = set()

    lon = min_lon
    while lon <= max_lon:
        lat = min_lat
        while lat <= max_lat:
            punto = Point(lon, lat)
            if poligono.contains(punto):
                geohash = pgh.encode(lat, lon, precision=precision)
                geohashes.add(geohash)
            lat += paso
        lon += paso

    for coord in poligono.exterior.coords:
        geohash = pgh.encode(coord[1], coord[0], precision=precision)
        geohashes.add(geohash)

    return list(geohashes)

def reducir_geohashes(geohashes):
    """
    Reduce la precisión de geohashes de 9 a 7 caracteres, eliminando duplicados.
    """
    geohashes_reducidos = {gh[:7] for gh in geohashes}
    return list(geohashes_reducidos)

def procesar_kml_y_generar_geohashes(ruta_archivo, datos_existentes=None, precision=9):
    """
    Procesa un archivo .kml y genera geohashes para cada polígono, 
    excluyendo los que ya existen en el archivo JSON si es necesario.
    """
    poligonos = analizar_kml(ruta_archivo)
    resultado = datos_existentes if datos_existentes else {}

    poligonos_existentes = set(resultado.keys()) if datos_existentes else set()

    for poligono in poligonos:
        if poligono["nombre"] not in poligonos_existentes:
            geohashes = generar_geohashes_para_poligono(poligono["coordenadas"], precision)
            geohashes_reducidos = reducir_geohashes(geohashes)
            resultado[poligono["nombre"]] = geohashes_reducidos

    return resultado

def cargar_geohashes_existentes(archivo_json):
    """
    Carga los geohashes existentes desde un archivo JSON, si existe.
    """
    if os.path.exists(archivo_json):
        with open(archivo_json, 'r') as archivo:
            return json.load(archivo)
    return None

def guardar_geohashes_en_json(geohashes_por_poligono, archivo_salida):
    """
    Guarda los geohashes generados en un archivo JSON.
    """
    with open(archivo_salida, 'w') as archivo_json:
        json.dump(geohashes_por_poligono, archivo_json, indent=4)
    print(f"Datos guardados en {archivo_salida}")

def guardar_geohashes_en_txt(geohashes_por_poligono, archivo_salida_txt):
    """
    Guarda los geohashes generados en un archivo .txt.
    """
    with open(archivo_salida_txt, 'w') as archivo_txt:
        for nombre, geohashes in geohashes_por_poligono.items():
            archivo_txt.write(f"Polígono: {nombre}\n")
            archivo_txt.write("Geohashes:\n")
            archivo_txt.write("\n".join(geohashes))
            archivo_txt.write("\n\n")
    print(f"Datos guardados en {archivo_salida_txt}")

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        dir_base = os.path.dirname(sys.executable)
    else:
        dir_base = os.path.dirname(os.path.abspath(__file__))
    
    dir_base = os.path.abspath(os.path.join(dir_base, os.pardir))
    
    ruta_archivo_kml = os.path.join(dir_base, "KMLC", "Poligonos.kml")
    archivo_salida_json = os.path.join(dir_base, "Geohash", "geohashes.json")
    archivo_salida_txt = os.path.join(dir_base, "Geohash", "geohashes.txt")

    datos_existentes = cargar_geohashes_existentes(archivo_salida_json)

    geohashes_por_poligono = procesar_kml_y_generar_geohashes(ruta_archivo_kml, datos_existentes, precision=9)

    guardar_geohashes_en_json(geohashes_por_poligono, archivo_salida_json)
    guardar_geohashes_en_txt(geohashes_por_poligono, archivo_salida_txt)
