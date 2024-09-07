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

base_directory = Path("C:\Workspace_PyQt\PythonPyQT")
path_temp      = base_directory.joinpath("LibroCoobook", "0_temp")
path_geopackge = base_directory.joinpath("LibroCoobook", "0_package", "danielito_pe")

out_layer = os.path.join(base_directory,"demo5.gpkg")

schema = QgsFields()
schema.append(QgsField('id', QVariant.Int))

crs = QgsCoordinateReferenceSystem('epsg:4326')
options = QgsVectorFileWriter.SaveVectorOptions()
options.driverName = "GPKG"
options.fileEncoding = 'cp1251'

fw = QgsVectorFileWriter.create(
    fileName=out_layer,
    fields=schema,
    geometryType=QgsWkbTypes.Polygon,
    srs=crs,
    transformContext=QgsCoordinateTransformContext(),
    options=options)
del fw 
#lyr = QgsVectorLayer(r"D:\GIS\Терпланирование\sheet_folder\demo5.gpkg", 'my_layer', 'ogr')    
#QgsProject.instance().addMapLayer(lyr)