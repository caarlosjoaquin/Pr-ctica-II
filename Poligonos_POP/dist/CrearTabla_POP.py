import os
import pandas as pd
import sys


def generar_datos_txt(archivo_excel, archivo_txt, separador="|"):
    print("Generando archivo datos.txt...")
    try:
        df = pd.read_excel(archivo_excel)
    except FileNotFoundError:
        print(f"Error: Archivo Excel '{archivo_excel}' no encontrado.")
        return  # Salir de la función si el archivo no existe
    except Exception as e: #manejo de errores mas generales
        print(f"Error al leer el archivo excel: {e}")
        return

    # Seleccionar columnas AN, E y F (pop, nombre, estado)
    try:
        columnas_an_e_f = df[["POP", "NOMBRE", "ESTADO"]]  # Selecciona las columnas por nombre
    except KeyError as e:
        print(f"Error: No se encontraron las columnas {e}. Verifique que las columnas 'POP', 'NOMBRE' y 'ESTADO' existan en el archivo Excel.")
        return

    # Convertir a string y manejar valores faltantes
    for col in columnas_an_e_f.columns:
        columnas_an_e_f[col] = columnas_an_e_f[col].astype(str).fillna("")  # Convierte a str y rellena vacíos con ""
        columnas_an_e_f[col] = columnas_an_e_f[col].str.strip() #quita espacios en blanco

    columnas_an_e_f = columnas_an_e_f.apply(lambda col: col.map(lambda x: x.upper() if isinstance(x, str) else x))

    columnas_an_e_f.to_csv(archivo_txt, index=False, header=False, sep=separador)
    print(f"Archivo {archivo_txt} generado correctamente.\n")

# Lee geohashes.txt y datos.txt para generar resultado_final.xlsx
def procesar_geohashes_y_datos(base_dir):
    print("Procesando geohashes y datos...")
    
    carpeta_coordenadas = os.path.join(base_dir, "Geohash")
    archivo_geohashes = os.path.join(carpeta_coordenadas, "geohashes.txt")
    archivo_datos = os.path.join(base_dir, "Archivos", "datos.txt")

    # Lee geohashes.txt
    def leer_geohashes(archivo):
        poligonos = {}
        with open(archivo, "r", encoding="latin-1") as f:
            lineas = f.readlines()
            i = 0
            while i < len(lineas):
                if lineas[i].startswith("Polígono:"):
                    nombre_poligono = lineas[i].split(":")[1].strip().upper()
                    i += 1
                    geohashes = []
                    i += 1
                    while i < len(lineas) and lineas[i].strip() != "":
                        geohashes.append(lineas[i].strip())
                        i += 1
                    poligonos[nombre_poligono] = geohashes
                else:
                    i += 1
        return poligonos

    # Lee datos.txt
    def leer_datos(archivo, separador="|"):
        datos = {}
        with open(archivo, "r", encoding="utf-8") as f:
            for linea in f:
                nombre, direccion, estado = linea.strip().split(separador)
                datos[nombre.strip().upper()] = {"nombre": nombre.strip(), "Direccion": direccion.strip(), "Estado": estado.strip()}
        return datos

    poligonos = leer_geohashes(archivo_geohashes)
    datos = leer_datos(archivo_datos, separador="|")

    resultados = []
    id_counter = 1

    for nombre_poligono, geohashes in poligonos.items():
        if nombre_poligono in datos:
            direccion_poligono = datos[nombre_poligono]["Direccion"]
            estado_poligono = datos[nombre_poligono]["Estado"]
            for gh in geohashes:
                descripcion = direccion_poligono  # Descripción modificada
                resultados.append(["", nombre_poligono, gh, descripcion, estado_poligono])  # ID vacío
                id_counter += 1

    df_resultado = pd.DataFrame(resultados, columns=["ID", "Nombre_poligono", "Geohash", "Descripcion", "Tipo"])

    # Guardar resultado en CSV
    ruta_salida_csv = os.path.join(base_dir, "Archivos", "Tabla.csv")  # Cambia la extensión a .csv
    df_resultado.to_csv(ruta_salida_csv, index=False, encoding='utf-8', sep=",") # Usa to_csv
    print(f"Archivo Tabla.csv guardado en: {ruta_salida_csv}")

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.abspath(os.path.join(base_dir, os.pardir))

    # Archivos de entrada y salida
    archivo_excel = os.path.join(base_dir, "Archivos", "subset_1.xlsx")
    archivo_txt = os.path.join(base_dir, "Archivos", "datos.txt")

    generar_datos_txt(archivo_excel, archivo_txt, separador="|")
    procesar_geohashes_y_datos(base_dir)