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

"""
 Se copia el SHP a un GEOPACKGE. Si no existe el geopacke te lo crea
"""

base_directory = Path("C:\Workspace_PyQt\PythonPyQT")
path_temp      = base_directory.joinpath("LibroCoobook", "0_data","Acuifero.shp")
path_geopackge = base_directory.joinpath("LibroCoobook", "0_package","my_new_file.gpkg")

layer = QgsVectorLayer(str(path_temp), "shp_temp","ogr")
save_options = QgsVectorFileWriter.SaveVectorOptions()
save_options.layerName = "Acuifero_temp"
transform_context = QgsProject.instance().transformContext()

fw = QgsVectorFileWriter.writeAsVectorFormatV3(
    layer,
    str(path_geopackge),
    transform_context,    
    save_options
)
del fw 
#lyr = QgsVectorLayer(r"D:\GIS\Терпланирование\sheet_folder\demo5.gpkg", 'my_layer', 'ogr')    
#QgsProject.instance().addMapLayer(lyr)