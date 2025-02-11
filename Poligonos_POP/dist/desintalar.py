import subprocess

def desinstalar_dependencias():
    """
    Desinstala las dependencias utilizadas en el proyecto.
    """
    dependencias = [
        "shapely",
        "pygeohash",
        "geohash2"
    ]

    print("Desinstalando dependencias...\n")

    for dependencia in dependencias:
        try:
            print(f"Desinstalando {dependencia}...")
            subprocess.run(["pip", "uninstall", "-y", dependencia], check=True)
            print(f"{dependencia} desinstalada correctamente.\n")
        except subprocess.CalledProcessError as e:
            print(f"Error al desinstalar {dependencia}: {e}\n")

    print("Desinstalación de dependencias completada.")

if __name__ == "__main__":
    desinstalar_dependencias()
