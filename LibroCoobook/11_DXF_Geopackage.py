import os, subprocess, zipfile, ezdxf
from datetime import datetime
from pathlib import Path
from pyproj import CRS, Transformer
from shapely.geometry import Point, LineString, Polygon
from qgis.core import (
    QgsApplication,
    QgsField,
    QgsFields,
    QgsVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransformContext,
    QgsCoordinateTransform,
    QgsProject,
    QgsVectorFileWriter,    
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsWkbTypes,
    QgsCoordinateTransformContext
)
from PyQt5.QtCore import QVariant

# Base directory
BASE_DIRECTORY = Path("C:\Workspace_PyQt\PythonPyQT\LibroCoobook") #Path.cwd()

# File name TEMP
FOLDER_NAME_TEMP = "temp"

# Config path DWG
input_FOLDER_DWG = os.path.join("C:\Workspace_PyQt\PythonPyQT\LibroCoobook", "0_data")

# Config CRS
input_CRS = QgsCoordinateReferenceSystem('EPSG:32718')

# Load files extension
input_list_files_extension = [
    { 
        "format": "KML"
        , "extension": "kml"
        , "download": ""
    }, {
        "format": "ESRI Shapefile"
        , "extension": "shp"
        , "download": ""
    }, { 
        "format": "GeoJSON"
        , "extension": "geojson"
        , "download": ""
    }, { 
        "format": "DXF"
        , "extension": "dxf"
        , "download": ""
    }
]

# Compress files
def get_compress_name():
    try:
        # Get date now
        date_now = datetime.now()
        # Format date and hour
        return date_now.strftime('%d%m%Y_%H%M%S')
    except Exception as e:
        print(f"{e}")

# Compress files
def compress_files(directorio_shapefile, nombre_zip):
    try:
        extension = ['.geojson', '.dxf', '.kml', '.shp', '.shx', '.dbf', '.prj']
        # Crear un archivo ZIP
        with zipfile.ZipFile(nombre_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Recorre todos los archivos en el directorio dado
            for carpeta_raiz, _, archivos in os.walk(directorio_shapefile):
                for archivo in archivos:
                    if any(archivo.lower().endswith(ext) for ext in extension):
                        # Crear la ruta completa del archivo
                        ruta_archivo = os.path.join(carpeta_raiz, archivo)
                        # Agregar el archivo al ZIP
                        zipf.write(ruta_archivo, os.path.relpath(ruta_archivo, directorio_shapefile))
                        
    except Exception as e:
        print(f"{e}")

# Path ODA .exe
def get_path_oda():
    try:
        # Nombre del archivo a buscar
        FILE_NAME = 'ODAFileConverter.exe'
        # Path .exe
        file_path_found = None
        # Search file
        for root, dirs, files in os.walk('C:/'):
            if FILE_NAME in files:
                file_path_found = os.path.join(root, FILE_NAME)
                break
        # File path
        print(f"Ruta: {file_path_found}")
        return file_path_found
    except Exception as e:
        print(f"{e}")

def convert_dwg_to_dxf(input_folder, output_folder, output_version="ACAD2018"):
    # Validate executable
    if get_path_oda() is None:
        return
    
    # Ruta al ejecutable ODAFileConverter
    oda_converter_path = get_path_oda()

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
            print(f"Conversión exitosa. Muestra la salida del comando: {result.stdout}")
        else:
            print(f"Error en la conversión. Muestra el error del comando: {result.stderr}")

    except Exception as e:
        print(f"Error al ejecutar ODAFileConverter: {e}")

# List file - delete
def delete_files(folder_export):
    try:
        #direcotory_export = BASE_DIRECTORY.joinpath("LibroCoobook", folder_export)
        direcotory_export = BASE_DIRECTORY.joinpath(folder_export)
        # Create folder
        if not direcotory_export.exists():
            direcotory_export.mkdir(parents=True)
        # Delete files
        for file_path in direcotory_export.iterdir():
            if file_path.is_file():
                file_path.unlink()
                #print(f"archivo eliminado: {file_path}")
    except Exception as e:
        print(f"{e}")

# Path folder
def get_folder(folder_export, file_extension = ""):
    try:
        return os.path.join(
            #BASE_DIRECTORY.joinpath("LibroCoobook", folder_export)
            BASE_DIRECTORY.joinpath(folder_export)
            , file_extension
        )
    except Exception as e:
        print(f"{e}")

# Importa datos
def import_files(file_path):
    try:        
        file_path_dxf = f"{str(file_path)}|layername=entities"
        # Abrir el archivo DXF
        layer = QgsVectorLayer(file_path_dxf, 'DXF layer', 'ogr')
        if not layer.isValid():
            print('Capa no válida.')
        else:
            for item_file in input_list_files_extension:
                list_lyr = []
                list_fileWriter = []
                # Delete files
                delete_files(item_file['extension'])                
                # Crear los objetos por tipo
                for feature in layer.getFeatures():
                    if feature['LAYER'] not in list_lyr:
                        # Obtener el tipo de geometría
                        geom_type = layer.geometryType()
                        list_lyr.append(feature['LAYER'])
                        file_name   = f"{feature['LAYER']}.{item_file['extension']}"
                        folder_name = get_folder(item_file['extension'], file_name)
                        crs_32718 = QgsCoordinateReferenceSystem('epsg:32718')
                        #transform_context = QgsProject.instance().transformContext()
                        save_options = QgsVectorFileWriter.SaveVectorOptions()
                        save_options.driverName = item_file['format']
                        save_options.fileEncoding = "UTF-8"
                        save_options.crs = QgsCoordinateReferenceSystem.fromEpsgId(32718)
                        #save_options.ct = QgsCoordinateTransform(layer.crs(), QgsCoordinateReferenceSystem('EPSG:4326'), QgsProject.instance())  # Transformación CRS si es necesario
                        # Create file
                        lyr_vector = QgsVectorFileWriter.create(
                            folder_name
                            , layer.fields()
                            , layer.wkbType()
                            , crs_32718
                            , QgsCoordinateTransformContext()
                            , save_options
                        )

                        # Add list
                        list_fileWriter.append({
                            "lyr" : feature['LAYER']
                            , "type": str(geom_type)
                            , "vfw": lyr_vector
                        })

                # Guardar datos de las capas
                for lyr_name in list_fileWriter:
                    for feature in layer.getFeatures():
                        #print(feature['LAYER'])                    
                        if(feature['Layer'] == lyr_name["lyr"]):
                            # Obtener atributos: attrs = feature.attributes()
                            lyr_name["vfw"].addFeature(feature)
            
                item_file['download'] = get_folder(
                    item_file['extension']
                    , f"{item_file['extension']}_{get_compress_name()}.zip"
                )

                compress_files(get_folder(item_file['extension']), item_file['download'])

    except Exception as e:
        print(f"{e}")
        #QMessageBox.critical(self, "Error", f"Error al leer el archivo DXF: {str(e)}")
        #QgsProject.instance().addMapLayer(layer)
        # Seleccionar ruta para guardar el GeoPackage
        #gpkg_path, _ = QFileDialog.getSaveFileName(self, "Guardar como GeoPackage", "", "GeoPackage (*.gpkg)")

# Lista todos los archivos DWG o DXF
def list_files(folder_path):
    listFile = []
    path_files_dxf = BASE_DIRECTORY.joinpath(folder_path).glob('*.dxf')
    # dwg_files = [f for f in os.listdir(folder_path) if f.endswith('.dwg') or f.endswith('.dxf')]
    # path_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.dwg', '.dxf'))]
    for dxf_file in path_files_dxf:
        listFile.append(dxf_file)
    return listFile

def main():    
    """
    # Obtener y listar los drivers soportados
    drivers = QgsVectorFileWriter.ogrDriverList()
    print("Drivers soportados:")
    for driver in drivers:
        print(driver.driverName)
    """
    #print(QgsWkbTypes.Point)
    #print(QgsWkbTypes.Polygon)
    #print(QgsWkbTypes.Line)

    # Create folder TEMP
    delete_files(FOLDER_NAME_TEMP)

    # Get folder path TEMP
    #output_folder_temp = BASE_DIRECTORY.joinpath("LibroCoobook", FOLDER_NAME_TEMP)
    output_folder_temp = BASE_DIRECTORY.joinpath(FOLDER_NAME_TEMP)

    # Process DWG to DXF
    convert_dwg_to_dxf(input_FOLDER_DWG, output_folder_temp)

    # Obtener la lista de archivos seleccionados DXF
    pathDXFFiles = list_files(output_folder_temp) 
    selected_files = [item for item in pathDXFFiles]
    if not selected_files:
        print("Error al leer el archivo")
        return
    
    for path_file in selected_files:        
        import_files(path_file)

main()

"""
    $ACADVER: Versión del DXF, indica con qué versión de AutoCAD fue creado el archivo (por ejemplo, "AC1027" para AutoCAD 2013).
    $INSUNITS: Unidades de inserción de objetos. Este valor puede ser:
    0 - Sin unidades
    1 - Pulgadas
    2 - Pies
    3 - Millas
    4 - Milímetros
    5 - Centímetros
    6 - Metros
    Otros valores para otras unidades.
    $MEASUREMENT: Sistema de medición utilizado (métrico o imperial).
    0 - Unidades imperiales
    1 - Unidades métricas
    $EXTMIN y $EXTMAX: Coordenadas mínimas y máximas del límite de extensión del dibujo.
    $LIMMIN y $LIMMAX: Coordenadas mínimas y máximas del límite del área de dibujo.
    $VIEWDIR: Dirección de la vista en coordenadas del espacio 3D.
    $TEXTSTYLE: Estilo de texto actual.
    $LUNITS: Unidades de longitud.
    $ANGBASE: Ángulo base para las rotaciones (en grados).
    $ANGDIR: Dirección de ángulo (0 = en sentido antihorario, 1 = en sentido horario).

Diferentes códigos de versión de version
    MC0.0 - DWG Release 1.1
    AC1.2 - DWG Release 1.2
    AC1.4 - DWG Release 1.4
    AC1.50 - DWG Release 2.0
    AC2.10 - DWG Release 2.10
    AC1002 - DWG Release 2.5
    AC1003: versión DWG 2.6
    AC1004 - DWG Release 9
    AC1006 - DWG Release 10
    AC1009 - DWG Release 11/12 (LT R1/R2)
    AC1012: versión DWG 13 (LT95)
    AC1014: versión DWG 14, 14.01 (LT97/LT98)
    AC1015 - DWG AutoCAD 2000/2000i/2002
    AC1018 - DWG AutoCAD 2004/2005/2006
    AC1021 - DWG AutoCAD 2007/2008/2009
    AC1024 - DWG AutoCAD 2010/2011/2012
    AC1027 - DWG AutoCAD 2013/2014/2015/2016/2017
    AC1032 - DWG AutoCAD 2018/2019/2020/2021/2022/2023/2024
"""