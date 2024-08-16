import sys, os, ezdxf
from pathlib import Path
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
path_geopackge = base_directory.joinpath("LibroCoobook", "0_package")
path_geopackge_gpkg = base_directory.joinpath("LibroCoobook", "0_package", "my_new_file.gpkg")

# Configura el CRS, puedes cambiarlo según tus necesidades
crs = QgsCoordinateReferenceSystem('EPSG:32718')

# Verificar si la ruta existe
if path_temp.exists():
    print(f"La ruta existe: {path_temp}")
else:
    print("La ruta no existe")

# Importa datos
def import_files(file_path):
    try:        
        file_path_dxf = f"{str(file_path)}|layername=entities"
        # Abrir el archivo DXF
        layer = QgsVectorLayer(file_path_dxf, 'DXF layer', 'ogr')
        if not layer.isValid():
            print('Capa no válida.')
        else:
            print("Se muestra capa")
            list_lyr = []           
            existing_layers = {item["layer"] for item in list_lyr}
            # Iterar sobre las características (features) de la capa
            for feature in layer.getFeatures():
                if feature['LAYER'] not in existing_layers:                    
                    shapefile_path = f"{feature['LAYER']}.shp"
                    # Crear un shapefile para cada capa
                    writer = QgsVectorFileWriter(
                        os.path.join(path_geopackge, shapefile_path)
                        , 'UTF-8'
                        , layer.fields()
                        , layer.wkbType()
                        , crs
                        , 'ESRI Shapefile'
                    )
                    list_lyr.append({
                        "layer" : feature['LAYER']
                        , "shp": writer
                    })
                    
            # Imprimir los nombres de las capas
            for lyr_name in list_lyr:
                # Iterar sobre las características (features) de la capa
                for feature in layer.getFeatures():
                    #print(feature['LAYER'])                    
                    if(feature['LAYER'] == lyr_name["layer"]):
                        # Muestra alguna información sobre la geometría de la característica
                        geom = feature.geometry()
                        geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
                        if geom.type() == QgsWkbTypes.PointGeometry:
                            # El tipo de geometría puede ser de tipo único o múltiple
                            if geomSingleType:
                                x = geom.asPoint()
                                # print("Point: ", x)
                            else:
                                x = geom.asMultiPoint()
                                # print("MultiPoint: ", x)
                        elif geom.type() == QgsWkbTypes.LineGeometry:
                            if geomSingleType:
                                x = geom.asPolyline()
                                # print("Line: ", x, "length: ", geom.length())
                            else:
                                x = geom.asMultiPolyline()
                                # print("MultiLine: ", x, "length: ", geom.length())
                        elif geom.type() == QgsWkbTypes.PolygonGeometry:
                            if geomSingleType:
                                x = geom.asPolygon()
                                # print("Polygon: ", x, "Area: ", geom.area())
                            else:
                                x = geom.asMultiPolygon()
                                # print("MultiPolygon: ", x, "Area: ", geom.area())
                        else:
                            print("Unknown or invalid geometry")
                        # Obtener atributos
                        # attrs = feature.attributes()
                        # attrs es una lista. Contiene todos los valores de los atributos de esta función
                        lyr_name["shp"].addFeature(feature)
            
            del list_lyr
    except Exception as e:
        print(f"{e}")
        #QMessageBox.critical(self, "Error", f"Error al leer el archivo DXF: {str(e)}")
        #QgsProject.instance().addMapLayer(layer)
        # Seleccionar ruta para guardar el GeoPackage
        #gpkg_path, _ = QFileDialog.getSaveFileName(self, "Guardar como GeoPackage", "", "GeoPackage (*.gpkg)")

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