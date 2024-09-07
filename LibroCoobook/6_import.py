from qgis.core import QgsVectorLayer, QgsProject, QgsDataSourceUri, QgsCoordinateReferenceSystem
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtWidgets import QApplication
import os


# Configura tu entorno si estás ejecutando esto fuera de QGIS
# os.environ['QGIS_PREFIX_PATH'] = 'C:/OSGeo4W/apps/qgis'
# from qgis.core import QgsApplication
# QgsApplication.setPrefixPath(os.environ['QGIS_PREFIX_PATH'], True)
# qgs = QgsApplication([], False)
# qgs.initQgis()

def import_dwg_to_geopackage(dwg_file_path, geopackage_path, crs='EPSG:4326'):
    """
    Importa capas de un archivo DWG a un GeoPackage en QGIS 3.24.

    :param dwg_file_path: Ruta completa al archivo DWG.
    :param geopackage_path: Ruta completa al archivo GeoPackage de destino.
    :param crs: Código CRS al que convertir las capas (por defecto 'EPSG:4326').
    """

    # Comprueba si el archivo DWG existe
    if not os.path.isfile(dwg_file_path):
        print(f"El archivo DWG no existe en la ruta: {dwg_file_path}")
        return
    
    # Verifica la existencia de GDAL DWG driver
    from osgeo import ogr
    driver = ogr.GetDriverByName('DXF')
    if not driver:
        print("El controlador DWG no está disponible.")
        return
    
    # Importar el archivo DWG usando OGR
    uri = QgsDataSourceUri()
    uri.setParam('layerName', 'entities')
    uri.setParam('geometry', 'Polygon')
    uri.setParam('source', dwg_file_path)
    uri.setParam('provider', 'ogr')
    dwg_layer = QgsVectorLayer(uri.uri(), 'DWG Import', 'ogr')

    if not dwg_layer.isValid():
        print(f"Error al cargar el archivo DWG: {dwg_file_path}")
        return

    # Añadir la capa DWG al proyecto actual
    QgsProject.instance().addMapLayer(dwg_layer)

    # Establece el CRS si se especifica
    if crs:
        crs_obj = QgsCoordinateReferenceSystem(crs)
        dwg_layer.setCrs(crs_obj)

    # Crea un nuevo GeoPackage o abre uno existente
    if not os.path.exists(geopackage_path):
        # El GeoPackage se creará al exportar la primera capa
        print(f"Creando un nuevo GeoPackage en: {geopackage_path}")
    else:
        print(f"El GeoPackage ya existe. Añadiendo capas a: {geopackage_path}")

    # Guardar cada capa en el GeoPackage
    layer_list = dwg_layer.dataProvider().subLayers()

    for layer_id, layer_name in layer_list:
        sub_layer = QgsVectorLayer(f"{uri.uri()}|layername={layer_name}", layer_name, "ogr")

        if sub_layer.isValid():
            sub_layer.setCrs(crs_obj)
            QgsProject.instance().addMapLayer(sub_layer)
            
            # Exportar subcapa a GeoPackage
            options = QgsVectorFileWriter.SaveVectorOptions()
            options.driverName = "GPKG"
            options.layerName = layer_name
            QgsVectorFileWriter.writeAsVectorFormat(sub_layer, geopackage_path, options)

            print(f"Subcapa '{layer_name}' exportada a GeoPackage con éxito.")

        else:
            print(f"No se pudo cargar la subcapa: {layer_name}")

    print("Importación de DWG a GeoPackage completada.")

# Configuración de rutas
dwg_path = r"0_data\LIMITE_DEPARTAMENTAL_WGS84.dwg"
gpkg_path = r"0_temp\archivo.gpkg"

# Llama a la función para importar DWG a GeoPackage
import_dwg_to_geopackage(dwg_path, gpkg_path)

# Finaliza la aplicación QGIS si estás ejecutando fuera de QGIS
# qgs.exitQgis()