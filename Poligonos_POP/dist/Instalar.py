import subprocess

def instalar_dependencias():
    """
    Instala las dependencias necesarias directamente usando pip.
    """
    dependencias = [
        "shapely",
        "pygeohash",
        "geohash2"
        "pandas",
        "xlsxwriter"
    ]

    print("Instalando dependencias...\n")

    for dependencia in dependencias:
        try:
            print(f"Instalando {dependencia}...")
            subprocess.run(["pip", "install", dependencia], check=True)
            print(f"{dependencia} instalada correctamente.\n")
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar {dependencia}: {e}\n")
            print("Por favor, revisa tu conexión a internet o el nombre de la dependencia.\n")

    print("Instalación de dependencias completada.")

if __name__ == "__main__":
    instalar_dependencias()
