import sys, os, ezdxf
from pathlib import Path
#from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QListWidget, QMessageBox
#from qgis.utils import iface
import geopandas as gpd
from pyproj import CRS, Transformer
from shapely.geometry import Point, LineString, Polygon

# Directorio base
base_directory = Path(Path.cwd())
path_temp      = base_directory.joinpath("LibroCoobook", "0_temp")
path_geopackge = base_directory.joinpath("LibroCoobook", "0_package", "danielito_pe")
geometries = []

# Verificar si la ruta existe
if path_temp.exists():
    print(f"La ruta existe: {path_temp}")
else:
    print("La ruta no existe")

"""
def exportSubLayerToGPKG(self, file_path, sub_layer_name, gpkg_path):
        # Cargar sub capa
        sub_layer_uri = f"'{file_path}'|layername={sub_layer_name}"
        sub_layer = QgsVectorLayer(sub_layer_uri, sub_layer_name, "ogr")
        
        if not sub_layer.isValid():
            print(self, "Error", f"No se pudo cargar la sub capa {sub_layer_name}.")
            return
        
        # Definir el CRS para la capa
        crs = QgsCoordinateReferenceSystem("EPSG:4326")
        sub_layer.setCrs(crs)
        
        # Exportar a GeoPackage
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = "GPKG"
        options.layerName = sub_layer_name
        options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
        
        error = QgsVectorFileWriter.writeAsVectorFormat(sub_layer, gpkg_path, options)
        
        if error[0] != QgsVectorFileWriter.NoError:
            print("Error", f"Error al exportar la sub capa {sub_layer_name} a GeoPackage.")
            return
"""
def get_units_name(units_code):
    # Mapa de códigos de unidades a nombres descriptivos
    units_map = {
        0: 'Unspecified',
        1: 'Inches',
        2: 'Feet',
        3: 'Miles',
        4: 'Millimeters',
        5: 'Centimeters',
        6: 'Meters',
        7: 'Kilometers',
        8: 'Microinches',
        9: 'Mils',
        10: 'Yards',
        11: 'Angstroms',
        12: 'Nanometers',
        13: 'Microns',
        14: 'Decimeters',
        15: 'Decameters',
        16: 'Hectometers',
        17: 'Gigameters',
        18: 'Astronomical Units',
        19: 'Light Years',
        20: 'Parsecs'
    }
    return units_map.get(units_code, 'Unknown')

def get_input_crs(units_code):
    # Determinar el CRS de entrada basado en el código de unidades
    if units_code in [0, 6]:  # Unspecified o Meters, asumiendo UTM o similar
        return CRS.from_epsg(3857)  # Web Mercator como predeterminado
    elif units_code == 4:  # Millimeters
        return CRS.from_epsg(3395)  # World Mercator
    elif units_code == 1:  # Inches, asumiendo que se trata de un sistema plano local
        return CRS.from_epsg(2227)  # NAD83 / California zone 3 (ftUS)
    elif units_code == 2:  # Feet
        return CRS.from_epsg(2277)  # NAD83 / Texas South Central (ftUS)
    else:
        return CRS.from_epsg(4326)  # Asumir WGS 84 por defecto
    
def save_as_geopackage():
    # Guardar las geometrías como GeoPackage
    if not geometries:
        print("Error")
        #QMessageBox.warning(self, "No hay datos", "No se ha cargado ningún archivo DXF o no se han encontrado geometrías.")
        return

    #file_path, _ = QFileDialog.getSaveFileName(self, "Guardar como GeoPackage", "", "Archivos GeoPackage (*.gpkg)")
    file_path = path_temp
    if file_path:
        try:
            gdf = gpd.GeoDataFrame(geometry = geometries, crs='EPSG:4326')
            gdf.to_file(file_path, driver="GPKG")
            print("Error")
            #QMessageBox.information(self, "Guardado", f"Datos guardados en {file_path}")
        except Exception as e:
            print("Error")
            #QMessageBox.critical(self, "Error", f"Error al guardar el GeoPackage: {str(e)}")

        
# Importa datos
def import_files(file_path):
    print("****************************************************** DXF")    
    try:
        dxf_doc = ezdxf.readfile(file_path)
        
        # Para windows se usa "\\" para otros "/"
        file_name   = str(file_path).split('\\')[-1]
        dxf_version = dxf_doc.acad_release
        header_vars = dxf_doc.header
        # Obtener las unidades de medida
        units_code       = header_vars.get("$INSUNITS", 0)
        units_name = get_units_name(units_code)
        print(f"Unidades del archivo DXF: {units_name}")
        
        # Intentar encontrar información sobre el CRS
        if 'GCS' in header_vars:
            print(f"GCS (Geographic Coordinate System): {header_vars['GCS']}")

        # Imprimir información del archivo
        print(f"Nombre del archivo: {file_name}")
        print(f"Versión de DXF: {dxf_version}")
        print(f"Unidades: {units_code}")

        # Obtener todas las capas
        layers = dxf_doc.layers
        print("\nCapas en el archivo DXF:")
        # Si no esta definido en el DXF el valor sería NONE.
        for layer in layers:
            print(f"- " * 40)
            print(f"- Nombre de capa: {layer.dxf.name}")
            print(f"- Color: {layer.dxf.color}")
            print(f"- Tipo de línea: {layer.dxf.linetype}")
            print(f"- Ancho de línea: {layer.dxf.lineweight}")

        
        # Extraer la geometría
        msp = dxf_doc.modelspace()
        for entity in msp:
            
            print(entity.dxftype())
            if entity.dxftype() == 'LINE':
                start_point = entity.dxf.start
                end_point = entity.dxf.end
                print(" - - - - - - - - - ")
                print(entity.dxf.start)
                print(entity.dxf.end)

                input_crs = get_input_crs(units_code)
                output_crs = CRS.from_epsg(4326)

                transformer = Transformer.from_crs(input_crs, output_crs, always_xy=True)
                line = LineString([transformer.transform(start_point, end_point)])
                geometries.append(line)
            elif entity.dxftype() == 'LWPOLYLINE':
                points = entity.get_points('xy')
                polyline = LineString(points)
                geometries.append(polyline)
            elif entity.dxftype() == 'CIRCLE':
                center = entity.dxf.center
                radius = entity.dxf.radius
                circle = Point(center).buffer(radius)
                geometries.append(circle)
            elif entity.dxftype() == 'POLYLINE':
                points = [vertex.dxf.location for vertex in entity.vertices]
                if entity.is_closed:
                    poly = Polygon(points)
                else:
                    poly = LineString(points)
                geometries.append(poly)
        
        save_as_geopackage()

    except Exception as e:
        print(f"{e}")
        #QMessageBox.critical(self, "Error", f"Error al leer el archivo DXF: {str(e)}")


    #layer = QgsVectorLayer(file_path, os.path.basename(file_path), "ogr")
    #print(layer)
    
    #QgsProject.instance().addMapLayer(layer)
    
    # Listar las capas dentro del DWG/DXF
    #sub_layers = layer.dataProvider().subLayers()
    #print(sub_layers)
    #sub_layer_names = [sub_layer.split(':')[-1] for sub_layer in sub_layers]
    
    # Seleccionar ruta para guardar el GeoPackage
    #gpkg_path, _ = QFileDialog.getSaveFileName(self, "Guardar como GeoPackage", "", "GeoPackage (*.gpkg)")
    """
    print(gpkg_path)
    if gpkg_path:
        # Iterar sobre sub capas y exportarlas
        print(sub_layer_names)
        for sub_layer_name in sub_layer_names:
            print("NOMBRES")
            print(sub_layer_name)
            exportSubLayerToGPKG(file_path, sub_layer_name, gpkg_path)
            
        print("Éxito", f"El archivo {file_path} se ha convertido exitosamente a {gpkg_path}.")
    """
    
# Lista todos los archivos DWG o DXF
def list_files():
    listFile = []
    path_files_dxf = path_temp.glob('*.dxf')
    # dwg_files = [f for f in os.listdir(path_temp) if f.endswith('.dwg') or f.endswith('.dxf')]
    # path_files = [f for f in os.listdir(path_temp) if f.lower().endswith(('.dwg', '.dxf'))]
    for dxf_file in path_files_dxf:
        listFile.append(dxf_file)
    return listFile

def main():
    pathDXFFiles = list_files() # Obtener la lista de archivos seleccionados
    selected_files = [item for item in pathDXFFiles]
    
    if not selected_files:
        print("Error al leer el archivo")
        return
    
    for path_file in selected_files:
        import_files(path_file)

main()
"""
def importDWG(self, file_path):
    # Usar QGIS para cargar y convertir DWG/DXF
    layer = QgsVectorLayer(file_path, os.path.basename(file_path), "ogr")
    
    if not layer.isValid():
        QMessageBox.critical(self, "Error", f"El archivo {file_path} no se pudo cargar como capa válida.")
        return
    
    QgsProject.instance().addMapLayer(layer)
    
    # Listar las capas dentro del DWG/DXF
    sub_layers = layer.dataProvider().subLayers()
    sub_layer_names = [sub_layer.split(':')[-1] for sub_layer in sub_layers]
    
    # Seleccionar ruta para guardar el GeoPackage
    gpkg_path, _ = QFileDialog.getSaveFileName(self, "Guardar como GeoPackage", "", "GeoPackage (*.gpkg)")
    
    if gpkg_path:
        # Iterar sobre sub capas y exportarlas
        for sub_layer_name in sub_layer_names:
            self.exportSubLayerToGPKG(file_path, sub_layer_name, gpkg_path)
            
        QMessageBox.information(self, "Éxito", f"El archivo {file_path} se ha convertido exitosamente a {gpkg_path}.")

def exportSubLayerToGPKG(self, file_path, sub_layer_name, gpkg_path):
    # Cargar sub capa
    sub_layer_uri = f"'{file_path}'|layername={sub_layer_name}"
    sub_layer = QgsVectorLayer(sub_layer_uri, sub_layer_name, "ogr")
    
    if not sub_layer.isValid():
        QMessageBox.critical(self, "Error", f"No se pudo cargar la sub capa {sub_layer_name}.")
        return
    
    # Definir el CRS para la capa
    crs = QgsCoordinateReferenceSystem("EPSG:4326")
    sub_layer.setCrs(crs)
    
    # Exportar a GeoPackage
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GPKG"
    options.layerName = sub_layer_name
    options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
    
    error = QgsVectorFileWriter.writeAsVectorFormat(sub_layer, gpkg_path, options)
    
    if error[0] != QgsVectorFileWriter.NoError:
        QMessageBox.critical(self, "Error", f"Error al exportar la sub capa {sub_layer_name} a GeoPackage.")
        return
"""