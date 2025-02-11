import os
import xml.etree.ElementTree as ET
import sys

def obtener_archivos_kml(ruta_carpeta):
    """
    Obtiene todos los archivos .kml en la carpeta
    """
    return [os.path.join(ruta_carpeta, archivo) for archivo in os.listdir(ruta_carpeta) if archivo.endswith('.kml')]

def crear_kml_combinado(lista_archivos, archivo_salida):
    """
    Combina múltiples archivos KML en un solo archivo.
    """
    espacio_nombres = {'kml': 'http://www.opengis.net/kml/2.2'}
    ET.register_namespace('', espacio_nombres['kml'])
    raiz = ET.Element(f"{{{espacio_nombres['kml']}}}kml")
    documento = ET.SubElement(raiz, 'Document')
    
    estilo = ET.SubElement(documento, 'Style', {'id': 'polygonStyle'})
    estilo_linea = ET.SubElement(estilo, 'LineStyle')
    ET.SubElement(estilo_linea, 'color').text = 'ff0000ff'
    ET.SubElement(estilo_linea, 'width').text = '2'
    estilo_poligono = ET.SubElement(estilo, 'PolyStyle')
    ET.SubElement(estilo_poligono, 'color').text = '7dff0000'
    
    for archivo in lista_archivos:
        arbol = ET.parse(archivo)
        lugares = arbol.findall('.//kml:Placemark', espacio_nombres)
        for lugar in lugares:
            documento.append(lugar)
    
    arbol = ET.ElementTree(raiz)
    arbol.write(archivo_salida, encoding='utf-8', xml_declaration=True)
    print(f"Archivo KML combinado creado: {archivo_salida}")

if __name__ == "__main__":

    if getattr(sys, 'frozen', False):
        directorio_base = os.path.dirname(sys.executable)
    else:
        directorio_base = os.path.dirname(os.path.abspath(__file__))
    
    directorio_base = os.path.abspath(os.path.join(directorio_base, os.pardir))
    
    ruta_carpeta = os.path.join(directorio_base, "KML")
    kml_salida = os.path.join(directorio_base, "KMLC", "Poligonos.kml")

    if not os.path.exists(ruta_carpeta):
        print(f"La carpeta '{ruta_carpeta}' no existe. Verifica la ruta.")
    else:
        archivos_kml = obtener_archivos_kml(ruta_carpeta)
        if archivos_kml:
            print(f"Archivos KML encontrados: {archivos_kml}")
            crear_kml_combinado(archivos_kml, kml_salida)
        else:
            print("No se encontraron archivos KML en la carpeta especificada.")
