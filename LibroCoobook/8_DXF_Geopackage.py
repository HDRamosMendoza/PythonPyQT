import sys, os, ezdxf
from pathlib import Path
#from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QListWidget, QMessageBox
#from qgis.utils import iface
#import geopandas as gpd
from pyproj import CRS, Transformer
from shapely.geometry import Point, LineString, Polygon
from qgis.core import (
    QgsApplication,
    QgsField,
    QgsFields,
    QgsVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsProject,
    QgsVectorFileWriter,    
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsWkbTypes,
    QgsCoordinateTransformContext
)
from PyQt5.QtCore import QVariant

# Directorio base
#base_directory = Path(Path.cwd())

base_directory = Path("C:\Workspace_PyQt\PythonPyQT")
path_temp      = base_directory.joinpath("LibroCoobook", "0_temp")
path_geopackge = base_directory.joinpath("LibroCoobook", "0_package", "danielito_pe")


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
    
def save_as_geopackage(geometries):
    # Guardar las geometrías como GeoPackage
    if not geometries:
        print("Error")
        #QMessageBox.warning(self, "No hay datos", "No se ha cargado ningún archivo DXF o no se han encontrado geometrías.")
        return

    #file_path, _ = QFileDialog.getSaveFileName(self, "Guardar como GeoPackage", "", "Archivos GeoPackage (*.gpkg)")
    file_path = path_geopackge
    if file_path:
        try:
            gdf = gpd.GeoDataFrame(geometry = geometries, crs='EPSG:32718')
            gdf.to_file(file_path, driver="GPKG")
            print("Error GPKG")
            #QMessageBox.information(self, "Guardado", f"Datos guardados en {file_path}")
        except Exception as e:
            print("Error exception")
            #QMessageBox.critical(self, "Error", f"Error al guardar el GeoPackage: {str(e)}")

        
# Importa datos
def import_files(file_path):
    print("****************************************************** DXF")    
    try:
        dxf_doc = ezdxf.readfile(file_path)          # Información del archivo        
        file_name   = str(file_path).split('\\')[-1] # Para windows se usa "\\" para otros "/"
        dxf_version = dxf_doc.acad_release           # Versión de CAD
        header_vars = dxf_doc.header                 # Cabecera de información del archivo
        header_units       = header_vars.get("$INSUNITS")    # Unidades de dibujo
        header_version     = header_vars.get('$ACADVER')     # Código(conjunto) de versión de AutoCAD
        header_direction   = header_vars.get('$VIEWDIR')     # Dirección de vista
        header_measurement = header_vars.get('$MEASUREMENT') # Unidades de medición (Métrico/Imperial). 
                                                             # Unidades imperiales(0) y Unidades métricas(1).
        #print(f"Unidades: {header_units}")
        #print(f"Código(conjunto) de AutoCAD: {header_version}")
        #print(f"Dirección de vista: {header_direction}")
        #print(f"Unidades de medición: {header_measurement}")
        #print(f"Nombre del archivo: {file_name}")
        #print(f"Versión de DXF: {dxf_version}")

        layers     = dxf_doc.layers       # Obtener todas las capas
        modelspace = dxf_doc.modelspace() # Extraer la geometría
        output_crs = QgsCoordinateReferenceSystem("EPSG:32718") # CRS de salida EPSG:32718

        print("\n Capas en el archivo DXF:")

        #output_crs = CRS.from_epsg(32717)
        # Campos del shapefile
        fields = QgsFields()
        fields.append(QgsField("Layer", QVariant.String))


        

        # Si no esta definido en el DXF el valor sería NONE.
        for layer in layers:
            if(len(modelspace.query(f'*[layer=="{layer.dxf.name}"]')) == 0):
                continue
            
            print(f"- " * 40)
            print(f"- Nombre de capa: {layer.dxf.name}")
            print(f"- Color: {layer.dxf.color}")
            print(f"- Tipo de línea: {layer.dxf.linetype}")
            print(f"- Ancho de línea: {layer.dxf.lineweight}")
            print(f"- Visible: {'No' if layer.is_off() else 'Sí'}")
            print(f"- Bloqueada: {'Sí' if layer.is_locked() else 'No'}")

            geometries = []

            schema = QgsFields()
            schema.append(QgsField('id', QVariant.Int))
            
            options = QgsVectorFileWriter.SaveVectorOptions()
            options.driverName = "ESRI Shapefile"
            options.fileEncoding = 'UTF-8'

            file_writer = QgsVectorFileWriter.create(
                fileName = os.path.join(base_directory, f"{layer.dxf.name}.shp"),
                fields   = schema,
                geometryType = QgsWkbTypes.Polygon,
                srs          = QgsCoordinateReferenceSystem('epsg:32718'),
                transformContext = QgsCoordinateTransformContext(),
                options          = options
            )

           
            
            # Filtrar entidades por la capa actual
            for entity in modelspace.query(f'*[layer=="{layer.dxf.name}"]'):
                #print(f" Tipo de entidad: {entity.dxftype()}") # Entidades geométricas: LWPOLYLINE, TEXT
                #print(f" Capa: {entity.dxf.layer}")
                if entity.dxftype() == 'LWPOLYLINE':
                    pass
                    #print(" + + + + + + + + ")                    
                    #options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
                    #print("LWPOLYLINE")
                    #points = entity.get_points('xy')
                    #polyline = LineString(points)
                    file_writer.append(polyline)     # Agrega datos
                    
                    points = [QgsPointXY(p[0], p[1]) for p in entity.get_points()]
                    poly = QgsGeometry.fromPolygonXY([points])
                    feature = QgsFeature(fields)
                    feature.setGeometry(poly)
                    feature.setAttribute("Layer", entity.dxf.layer)
                    feature.addFeature(feature)
                    geometries.append(line)
                    
                
                """
                if entity.dxftype() == 'LINE':
                    print("LINE")
                    #output_crs = CRS.from_epsg(32717)
                    #transformer = Transformer.from_crs(input_crs, output_crs, always_xy=True)
                    print(f"GEOMETRÍA: {entity.dxftype()}")
                    print(f"{entity.dxf.start.x}")
                    print(f"{entity.dxf.start.y}")
                    #start_point = entity.dxf.start.x
                    #end_point   = entity.dxf.start.y
                    #line = LineString([start_point,end_point])
                    #geometries.append(line)         # Agrega datos
                elif entity.dxftype() == 'LWPOLYLINE':
                    print("LWPOLYLINE")
                    points = entity.get_points('xy')
                    polyline = LineString(points)
                    geometries.append(polyline)     # Agrega datos                
                elif entity.dxftype() == 'CIRCLE':
                    print("CIRCLE")
                    center = entity.dxf.center
                    radius = entity.dxf.radius
                    circle = Point(center).buffer(radius)
                    geometries.append(circle)       # Agrega datos
                elif entity.dxftype() == 'POLYLINE':
                    print("POLYLINE")
                    points = [vertex.dxf.location for vertex in entity.vertices]
                    if entity.is_closed:
                        poly = Polygon(points)      # Agrega datos
                    else:
                        poly = LineString(points)   # Agrega datos
                    geometries.append(poly)
                """
            del file_writer
            #del poly_writer
            #print(geometries)
        
        #save_as_geopackage(geometries)
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
        print(selected_files)
        return
    
    for path_file in selected_files:        
        import_files(path_file)

        #dxf_layer = QgsVectorLayer(path_file, "DXF Layer", "ogr")
        #if not dxf_layer.isValid():
            #print("No se pudo cargar el archivo DXF.")
            #return

        #dxf_layer.setCrs(QgsCoordinateReferenceSystem("EPSG:32718")) # Configurar la transformación de reproyección
        #QgsProject.instance().addMapLayer(dxf_layer) # Agregar la capa al proyecto

        #output_file_path = os.path.join(path_temp, f"{output_file_name}.shp") # Ruta del archivo de salida


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
"""

""""
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

"""
Entidades geométricas
- Líneas (LINE): Coordenadas de los puntos de inicio y fin.
- Arcos (ARC): Centro, radio, ángulo inicial y final.
- Círculos (CIRCLE): Centro y radio.
- Polilíneas (POLYLINE, LWPOLYLINE): Lista de vértices.
- Textos (TEXT, MTEXT): Contenido del texto, posición y estilo.
- Bloques (INSERT): Referencias a bloques insertados, posición y escala.
- Splines (SPLINE): Puntos de control y nudos.
- Elipses (ELLIPSE): Centro, ejes y proporción.
- Hachuras (HATCH): Patrón de hachurado y límites.
- Dimensiones (DIMENSION): Valores y estilo de la cota.
"""