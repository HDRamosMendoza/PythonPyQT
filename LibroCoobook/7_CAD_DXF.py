import subprocess, os

def convert_dwg_to_dxf(input_folder, output_folder, output_version="ACAD2018"):
    # Ruta al ejecutable ODAFileConverter
    oda_converter_path = os.path.join("C:\Program Files\ODA\ODAFileConverter_title 21.9.0", "ODAFileConverter.exe")

    # Verifica si el archivo ejecutable existe
    if not os.path.isfile(oda_converter_path):
        print(f"No se encontró el ejecutable en la ruta: {oda_converter_path}")
        return

    # Verifica si la carpeta de entrada existe
    if not os.path.isdir(input_folder):
        print(f"No se encontró la carpeta de entrada: {input_folder}")
        return

    # Crea la carpeta de salida si no existe
    os.makedirs(output_folder, exist_ok=True)

    # Parámetros para el comando
    params = [
        oda_converter_path, # Ruta al ejecutable
        f'{input_folder}',  # Carpeta de entrada entre comillas
        f'{output_folder}', # Carpeta de salida entre comillas
        output_version,     # Versión de salida (e.g., "ACAD2018")
        "DXF",              # Tipo de archivo de salida ("DXF")
        "0",                # Recursividad ("0" - No recursivo)
        "1",                # Auditar cada archivo ("0" - No auditar, "1" - Auditar)
        "*.DWG"             # Filtro de archivos de entrada (opcional)
    ]

    try:
        # Ejecutar el comando
        result = subprocess.run(params, capture_output=True, text=True, shell=True)

        # Comprobar el código de salida
        if result.returncode == 0:
            print("Conversión exitosa:")
            print(result.stdout)  # Muestra la salida del comando
        else:
            print("Error en la conversión:")
            print(result.stderr)  # Muestra el error del comando

    except Exception as e:
        print(f"Error al ejecutar ODAFileConverter: {e}")

input_folder = os.path.join(os.getcwd(), "LibroCoobook", "0_data")
output_folder = os.path.join(os.getcwd(), "LibroCoobook", "0_temp")

convert_dwg_to_dxf(input_folder, output_folder)