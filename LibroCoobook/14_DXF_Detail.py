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

# Valida. Si la capa no existe lo agrega
def add_layer(lyr, arr):
    if not any(item['Layer'] == lyr['Layer'] and item['Geometry'] == lyr['SubClasses'] for item in arr):
        arr.append({"Layer": lyr['Layer'], "Geometry": lyr['SubClasses']})

def main():
    file_path_dxf = os.path.join(str(path_temp),"AREA 3J.dxf|layername=entities|geometrytype=Polygon")
    abc2 = os.path.join(str(path_temp),"AREA 3J.dxf")
    print("Ruta de DXF")
    # Abrir el archivo DXF
    layer = QgsVectorLayer(file_path_dxf, 'DXF layer', 'ogr')

    if not layer.isValid():
        print("No es una capa")
    else:
        unique_layers = []
        for feature in layer.getFeatures():
            #print("Geometria")
            #print(feature.geometry().type())
            add_layer(feature, unique_layers)
            
        print(f"Lista de objetos geometricos \n")
        for lyr in unique_layers:
            """
            '010101_LIMITEMANZANA'
            temp_layer = QgsVectorLayer(f"{abc2}|layername={lyr['Layer']}", lyr['Layer'], "ogr")
            geometry_type = temp_layer.geometryType()  # Obtener el tipo de geometría
            if geometry_type == QgsWkbTypes.PointGeometry:
                geometry_type_str = "Point"
            elif geometry_type == QgsWkbTypes.LineGeometry:
                geometry_type_str = "Line"
            elif geometry_type == QgsWkbTypes.PolygonGeometry:
                geometry_type_str = "Polygon"
            else:
                geometry_type_str = "Unknown"
            """
                
            print(f"{lyr['Layer']} - {lyr['Geometry']}")

    """
    # Cargar el archivo DXF
    doc = ezdxf.readfile(abc2)

    # Acceder al modelo espacial
    modelspace = doc.modelspace()

    # Iterar sobre las entidades y mostrar información básica
    for entity in modelspace:
        print(f"Entidad: {entity.dxftype()}")

        # Mostrar información adicional según el tipo de entidad
        if entity.dxftype() == "LINE":
            print(f"  Inicio: {entity.dxf.start}, Fin: {entity.dxf.end}")
        elif entity.dxftype() == "CIRCLE":
            print(f"  Centro: {entity.dxf.center}, Radio: {entity.dxf.radius}")
        elif entity.dxftype() == "TEXT":
            print(f"  Contenido: {entity.dxf.text}")

    # Guardar el archivo modificado si fuera necesario
    doc.saveas("archivo_modificado.dxf")
    """
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