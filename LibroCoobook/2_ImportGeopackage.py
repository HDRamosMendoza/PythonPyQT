import os, time, ezdxf

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

path_folder = r"0_data"
path_files = [f for f in os.listdir(path_folder) if f.lower().endswith(('.dwg', '.dxf'))]
listFiles = []

for itemFile in path_files:
    listFiles.append(itemFile)

# Recorrer la lista de archivos de CAD
for itemFile in listFiles:
    print(itemFile)

# Obtener la lista de archivos seleccionados DWG/DXF
selected_files = [item for item in listFiles]
if not selected_files:
    print("No se han seleccionado archivos DWG/DXF.")
    
# Recorre la lista
for dwg_file in selected_files:
    file_path = os.path.join(path_folder, dwg_file)
    print(str(file_path))
    if (os.path.exists(file_path)):
        doc = ezdxf.readfile(file_path)
        geometrias = []        
        for entity in doc.modelspace().query('LINE LWPOLYLINE POLYLINE CIRCLE ARC'):
            if entity.dxftype() == 'LINE':
                start = entity.dxf.start
                end = entity.dxf.end
                geom = LineString([start, end])
            elif entity.dxftype() == 'LWPOLYLINE':
                points = entity.get_points()
                geom = LineString(points) if not entity.is_closed else Polygon(points)
            elif entity.dxftype() == 'POLYLINE':
                points = [point[:2] for point in entity.points()]
                geom = LineString(points) if not entity.is_closed else Polygon(points)
            elif entity.dxftype() == 'CIRCLE':
                center = entity.dxf.center
                radius = entity.dxf.radius
                geom = Point(center).buffer(radius)
            elif entity.dxftype() == 'ARC':
                # Arcos no son soportados directamente, se pueden aproximar como líneas
                center = entity.dxf.center
                radius = entity.dxf.radius
                start_angle = entity.dxf.start_angle
                end_angle = entity.dxf.end_angle
                num_segments = 100
                angles = [start_angle + (end_angle - start_angle) / num_segments * i for i in range(num_segments + 1)]
                points = [(center[0] + radius * math.cos(math.radians(a)), center[1] + radius * math.sin(math.radians(a))) for a in angles]
                geom = LineString(points)
            else:
                continue

            geometrias.append(geom)
        
    
#####################

"""
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
"""






    
"""
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
