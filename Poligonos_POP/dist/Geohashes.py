import json
import geohash2
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom
import webbrowser
import os
import sys

def calcular_caja_geohash(geohash):
    lat, lon, error_lat, error_lon = geohash2.decode_exactly(geohash)
    return {
        "oeste": lon - error_lon,
        "este": lon + error_lon,
        "norte": lat + error_lat,
        "sur": lat - error_lat,
    }

def crear_kml_desde_geohashes(ruta_archivo_json, ruta_salida_kml):
    with open(ruta_archivo_json, 'r') as archivo:
        geohashes_por_poligono = json.load(archivo)

    kml = Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    documento = SubElement(kml, "Document")

    for nombre_poligono, geohashes in geohashes_por_poligono.items():
        carpeta = SubElement(documento, "Folder")
        nombre_carpeta = SubElement(carpeta, "name")
        nombre_carpeta.text = nombre_poligono

        for geohash in geohashes:
            caja = calcular_caja_geohash(geohash)
            coordenadas = [
                (caja["oeste"], caja["sur"]),
                (caja["oeste"], caja["norte"]),
                (caja["este"], caja["norte"]),
                (caja["este"], caja["sur"]),
                (caja["oeste"], caja["sur"]),
            ]

            marca_lugar = SubElement(carpeta, "Placemark")
            nombre = SubElement(marca_lugar, "name")
            nombre.text = geohash

            poligono = SubElement(marca_lugar, "Polygon")
            limite_exterior = SubElement(poligono, "outerBoundaryIs")
            anillo_lineal = SubElement(limite_exterior, "LinearRing")

            texto_coordenadas = " ".join(f"{lon},{lat},0" for lon, lat in coordenadas)
            coords = SubElement(anillo_lineal, "coordinates")
            coords.text = texto_coordenadas

    cadena_xml = tostring(kml, encoding="utf-8")
    xml_pretty = xml.dom.minidom.parseString(cadena_xml).toprettyxml(indent="  ")

    with open(ruta_salida_kml, 'w') as archivo_kml:
        archivo_kml.write(xml_pretty)

    print(f"Archivo KML generado: {ruta_salida_kml}")

    url_google_earth = "https://earth.google.com/web/"
    print("Abriendo Google Earth Web...")
    webbrowser.open(url_google_earth)

    ruta_carpeta = os.path.dirname(ruta_salida_kml)
    print("Abriendo carpeta del archivo KML...")
    os.startfile(ruta_carpeta)

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        dir_base = os.path.dirname(sys.executable)
    else:
        dir_base = os.path.dirname(os.path.abspath(__file__))

    dir_base = os.path.abspath(os.path.join(dir_base, os.pardir))
    # Definir rutas relativas basadas en el directorio base
    ruta_archivo_json = os.path.join(dir_base, "Geohash", "geohashes.json")
    ruta_salida_kml = os.path.join(dir_base, "Geohash", "geohashes_visual.kml")

    crear_kml_desde_geohashes(ruta_archivo_json, ruta_salida_kml)
