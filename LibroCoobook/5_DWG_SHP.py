#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import ezdxf
import fiona
from fiona.crs import from_epsg
from shapely.geometry import Point, LineString, Polygon
import shapely.geometry

def listar_archivos_dwg(ruta):
    archivos_dwg = []
    for directorio_raiz, subdirectorios, archivos in os.walk(ruta):
        for archivo in archivos:
            if archivo.lower().endswith('.dwg'):
                archivos_dwg.append(os.path.join(directorio_raiz, archivo))
    return archivos_dwg

def extraer_geometrias_de_dwg(ruta_dwg):
    doc = ezdxf.readfile(ruta_dwg)
    print("INGRESO")
    print(type(doc))
    print(doc)
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
    
    return geometrias

def convertir_dwg_a_shapefile(ruta_dwg, ruta_salida):
    geometrias = extraer_geometrias_de_dwg(ruta_dwg)
    if not geometrias:
        print(f"No se encontraron geometrías en {ruta_dwg}")
        return

    schema = {
        'geometry': 'Unknown',
        'properties': {'id': 'int'}
    }

    if isinstance(geometrias[0], Point):
        schema['geometry'] = 'Point'
    elif isinstance(geometrias[0], LineString):
        schema['geometry'] = 'LineString'
    elif isinstance(geometrias[0], Polygon):
        schema['geometry'] = 'Polygon'

    nombre_archivo_salida = os.path.splitext(os.path.basename(ruta_dwg))[0]
    ruta_salida_completa = os.path.join(ruta_salida, nombre_archivo_salida + '.shp')

    with fiona.open(ruta_salida_completa, 'w', driver='ESRI Shapefile', crs=from_epsg(4326), schema=schema) as layer:
        for idx, geom in enumerate(geometrias):
            layer.write({
                'geometry': shapely.geometry.mapping(geom),
                'properties': {'id': idx}
            })

    print(f"Archivo convertido y guardado en {ruta_salida_completa}")

def list_file_dwg(pathFile):
    archivos_dwg = []
    for directorio_raiz, subdirectorios, archivos in os.walk(pathFile):
        for archivo in archivos:
            if archivo.lower().endswith('.dwg'):
                archivos_dwg.append(os.path.join(directorio_raiz, archivo))
    return archivos_dwg

def main():
    #pathWork = os.path.join(os.path.dirname(__file__), "dwg")
    pathWork = os.path.join(os.getcwd(),"LibroCoobook","0_data")
    if (os.path.exists(pathWork)):
        # Obtiene todos los DWFG
        fileDWG = list_file_dwg(pathWork)

        print(fileDWG)
        
        #Lista todos los archivos
        for itemDWG in fileDWG:
            pathSHP = os.path.join(os.getcwd(),"LibroCoobook","0_Instaladores")
            print(pathSHP)
            print(os.path.exists(pathSHP))
            if (os.path.exists(pathSHP)):
                # Migra los datos de DWG a SHP
                print(itemDWG)
                print("Entro") 
                convertir_dwg_a_shapefile(itemDWG, pathSHP)

	    # Antes de entrar a la ruta se tiene que verificar si existe el directorio
    else:
        print("No existe RUTA")

if __name__ == "__main__":
    main()
""""
import os
from osgeo import ogr

# Ruta al archivo DWG de entrada
input_dwg = os.path.join(os.getcwd(),"LibroCoobook","0_data","AREA 3J.dwg")

if os.path.exists(input_dwg):
    print("El archivo existe.")
else:
    print("El archivo no existe.")


driver = ogr.GetDriverByName("CAD")

if driver is None:
    print("Error: No se encontró el driver para DWG.")
else:
    print("Driver DWG encontrado correctamente.")

# Abrir el archivo DWG
driver = ogr.GetDriverByName('CAD')
print(input_dwg)
datasource = driver.Open(input_dwg, 0)  # 0 significa solo lectura
# Verificar si el driver está disponible
if driver is None:
    print("Error: No se encontró el driver para GeoJSON.")

if not datasource:
    print(f"No se pudo abrir el archivo: {input_dwg}")
else:
    print(f"Archivo DWG abierto exitosamente: {input_dwg}")

    # Iterar a través de las capas en el archivo DWG
    for i in range(datasource.GetLayerCount()):
        layer = datasource.GetLayerByIndex(i)
        layer_name = layer.GetName()
        print(f"Convirtiendo capa: {layer_name}")

        # Crear una ruta de salida para el Shapefile
        shapefile_path = os.path.join(output_dir, f"{layer_name}.shp")

        # Crear el Shapefile de salida
        shapefile_driver = ogr.GetDriverByName("ESRI Shapefile")
        if os.path.exists(shapefile_path):
            shapefile_driver.DeleteDataSource(shapefile_path)

        output_shapefile = shapefile_driver.CreateDataSource(shapefile_path)
        output_layer = output_shapefile.CreateLayer(layer_name, geom_type=layer.GetGeomType())

        # Copiar los campos de atributos
        layer_defn = layer.GetLayerDefn()
        for j in range(layer_defn.GetFieldCount()):
            field_defn = layer_defn.GetFieldDefn(j)
            output_layer.CreateField(field_defn)

        # Copiar las características (features)
        for feature in layer:
            geom = feature.GetGeometryRef()
            out_feature = ogr.Feature(output_layer.GetLayerDefn())
            out_feature.SetGeometry(geom)

            # Copiar los atributos
            for j in range(out_feature.GetFieldCount()):
                out_feature.SetField(out_feature.GetFieldDefnRef(j).GetNameRef(), feature.GetField(j))

            output_layer.CreateFeature(out_feature)
            out_feature = None  # Limpiar memoria

        # Cerrar el Shapefile de salida
        output_shapefile = None
        print(f"Capa convertida y guardada en: {shapefile_path}")

    # Cerrar el archivo DWG
    datasource = None
    print("Conversión completada.")
"""