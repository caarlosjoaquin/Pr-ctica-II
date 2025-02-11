import os
import sys

def procesar_archivos():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    base_dir = os.path.abspath(os.path.join(base_dir, os.pardir))

    # Directorios
    carpeta_coordenadas = os.path.join(base_dir, "Coordenadas")
    carpeta_kml = os.path.join(base_dir, "KML")

    # Crear la carpeta KML si no existe
    if not os.path.exists(carpeta_kml):
        os.makedirs(carpeta_kml)

    # Procesar cada archivo .txt en la carpeta Coordenadas
    for archivo in os.listdir(carpeta_coordenadas):
        if archivo.endswith(".txt"):
            ruta_archivo = os.path.join(carpeta_coordenadas, archivo)
            nombre_base = os.path.splitext(archivo)[0]
            nombre_kml = f"{nombre_base}.kml"
            ruta_kml = os.path.join(carpeta_kml, nombre_kml)

            # Leer las coordenadas del archivo
            coordenadas = []
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                lineas = f.readlines()
                for linea in lineas:
                    linea = linea.strip()
                    if not linea or "," not in linea:
                        continue
                    try:
                        lat, lon = linea.split(", ")
                        # Invertir latitud y longitud, y agregar ",0"
                        coordenada_formateada = f"{lon},{lat},0"
                        coordenadas.append(coordenada_formateada)
                    except ValueError:
                        print(f"Línea malformada ignorada en {archivo}: {linea}")

            # Crear el contenido del archivo KML
            contenido_kml = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>{nombre_base}</name>
    <Style id="polygonStyle">
      <LineStyle>
        <color>ff0000ff</color>
        <width>2</width>
      </LineStyle>
      <PolyStyle>
        <color>7dff0000</color>
      </PolyStyle>
    </Style>
    <Placemark>
      <name>{nombre_base}</name>
      <styleUrl>#polygonStyle</styleUrl>
      <Polygon>
        <outerBoundaryIs>
          <LinearRing>
            <coordinates>
{'\n'.join(coordenadas)}
            </coordinates>
          </LinearRing>
        </outerBoundaryIs>
      </Polygon>
    </Placemark>
  </Document>
</kml>"""

            with open(ruta_kml, "w", encoding="utf-8") as kml:
                kml.write(contenido_kml)

            print(f"Archivo KML creado: {ruta_kml}")

if __name__ == "__main__":
    procesar_archivos()
