import os
import subprocess
import sys

def instalar_dependencias():
    """
    Ejecuta el script Instalar.py para instalar las dependencias necesarias.
    """
    script_instalacion = os.path.join(base_dir, "Instalar.py")

    if os.path.exists(script_instalacion):
        print("Instalando dependencias necesarias...")
        try:
            # Ejecuta el script Instalar.py
            subprocess.run(["python", script_instalacion], check=True)
            print("Dependencias instaladas correctamente.\n")
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar dependencias: {e}\n")
            print("No se puede continuar sin las dependencias. Saliendo.")
            exit(1)
    else:
        print(f"No se encontró el script {script_instalacion}. Asegúrese de que esté en la misma carpeta que este archivo.")
        exit(1)

def ejecutar_archivos(archivos):
    """
    Ejecuta una lista de scripts en orden, deteniéndose si ocurre un error.
    """
    for archivo in archivos:
        ruta_completa = os.path.join(base_dir, archivo)  # Ruta completa del script
        if not os.path.exists(ruta_completa):
            print(f"El archivo {archivo} no existe en {base_dir}. Verifique su ubicación.")
            break

        print(f"Ejecutando {archivo}...")
        try:
            subprocess.run(["python", ruta_completa], check=True)
            print(f"{archivo} ejecutado correctamente.\n")
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar {archivo}: {e}\n")
            break

def menu_principal():
    ruta_archivo_json = os.path.join(base_dir, "Geohash", "geohashes.json")

    while True:
        print("\nMenú principal")
        print("1. Ejecutar programa")
        print("2. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            if os.path.exists(ruta_archivo_json):
                print("El archivo geohashes.json ya existe.")
                recrear = input("¿Desea crearlo nuevamente? (s/n): ").strip().lower()
                if recrear == 's':
                    print("Recreando el archivo y ejecutando todos los scripts...")
                    ejecutar_archivos([
                        "Poligono.py",
                        "PoligonosCompleto.py",
                        "Geohash.py",
                        "Geohashes.py",
                        "CrearTabla.py"
                    ])
                elif recrear == 'n':
                    print("Ejecutando únicamente Geohashes.py...")
                    ejecutar_archivos(["Geohashes.py"])
                else:
                    print("Opción no válida. Volviendo al menú principal.\n")
            else:
                ejecutar_archivos([
                    "Poligono.py",
                    "PoligonosCompleto.py",
                    "Geohash.py",
                    "Geohashes.py",
                    "CrearTabla.py"
                ])
        elif opcion == "2":
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente nuevamente.\n")

if __name__ == "__main__":
    # Determinar el directorio base
    if getattr(sys, 'frozen', False):  # Si está empaquetado
        base_dir = os.path.dirname(sys.executable)  # Carpeta del ejecutable
    else:  # En desarrollo o ejecución normal
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Carpeta del script

    # Primero instalamos las dependencias
    instalar_dependencias()
    
    # Luego mostramos el menú principal
    menu_principal()
