import os, time

from qgis.core import (
 QgsGeometry,
 QgsMapSettings,
 QgsPrintLayout,
 QgsMapSettings,
 QgsMapRendererParallelJob,
 QgsLayoutItemLabel,
 QgsLayoutItemLegend,
 QgsLayoutItemMap,
 QgsLayoutItemPolygon,
 QgsLayoutItemScaleBar,
 QgsLayoutExporter,
 QgsLayoutItem,
 QgsLayoutPoint,
 QgsLayoutSize,
 QgsUnitTypes,
 QgsProject,
 QgsFillSymbol,
 QgsCoordinateReferenceSystem,
 QgsVectorFileWriter,
 QgsVectorLayer,
)

from qgis.PyQt.QtGui import (QPolygonF, QColor)
from qgis.PyQt.QtCore import (QPointF, QRectF, QSize)

abc = r"C:\Users\heber\Downloads\PlanosconPyQGIS"
#dwg_file_path = r".\AREA 3J.dwg" 
#files = [f for f in os.listdir(abc) if f.lower().endswith(('.dwg', '.dxf'))]
gpkg_file = r".\demo55.gpkg"

files = [f for f in os.listdir(abc) if f.lower().endswith(('.dwg'))]

print(files)

for file in files:
    layer = QgsVectorLayer(file, "HEBER", "ogr")
    if not layer.isValid():
        QMessageBox.warning(none, 'Layer Error', f'Failed to load layer from {file}.')
        continue

    # Define CRS if necessary
    crs = layer.crs()  # Use CRS of the original layer

    # Define output path and layer name in GeoPackage
    layer_name = os.path.splitext(os.path.basename(file))[0]  # Use base name without extension
    print("- - -- - - - - - -- ")
    geometry_type = layer.geometryType()
    print(layer.geometryType())
    print(geometry_type)
    
    print(type(geometry_type))
    print(type(QgsWkbTypes.PointGeometry))
    
    print("****")
    print(QgsWkbTypes.PointGeometry)
    print(QgsWkbTypes.LineGeometry)
    print(QgsWkbTypes.PolygonGeometry)
    print("****")
    
    # Configurar el Writer para el GeoPackage
    writer = QgsVectorFileWriter(
        gpkg_file,
        "UTF-8",
        layer.fields(),
        QgsWkbTypes.Polygon,
        QgsCoordinateReferenceSystem('epsg:4326'),
        "GPKG"
    )
        
    """
    if geometry_type == QgsWkbTypes.PointGeometry:
        print("Point")
        print(QgsWkbTypes.PointGeometry)
        print(QgsWkbTypes.Point)
        geometry_type = QgsWkbTypes.Point
    elif geometry_type == QgsWkbTypes.LineGeometry:
        print("LineString")
        print(QgsWkbTypes.LineGeometry)
        print(QgsWkbTypes.LineString)
        geometry_type = QgsWkbTypes.LineString
    elif geometry_type == QgsWkbTypes.PolygonGeometry:
        print("Polygon")
        print(QgsWkbTypes.PolygonGeometry)
        print(QgsWkbTypes.Polygon)
        geometry_type = QgsWkbTypes.Polygon
    
                
    # Save to GeoPackage
    writer = QgsVectorFileWriter(
        gpkg_file,
        "ogr",
        layer.fields(),
        geometry_type,
        crs,
        "GPKG"
    )
    
    if writer.hasError() != QgsVectorFileWriter.NoError:
        print("ERROR PENULTIMO")
        continue

    for feature in layer.getFeatures():
        writer.addFeature(feature)

    del writer
    """
