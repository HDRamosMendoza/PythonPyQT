from qgis.core import *
import qgis.utils

"""
layer = qgis.utils.iface.activeLayer() # Lista las capas activas. Se debe de tener alguna capa activa
print(layer.id()) # Obtiene el id de la capa en el TOC
print(layer.featureCount()) # Obtiene el contador de registros de la capa activa
"""

# import os
# os.chdir(r"C:\Workspace_PyQt\PythonPyQT\LibroCoobook")
# os.listdir(os.getcwd())
path_to_ayacucho = r"./0_data/Ciudad_de_Ayacucho.shp"
vlayer = QgsVectorLayer(path_to_ayacucho, "Airports layer", "ogr")
if not vlayer.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(vlayer)


#- iface para ceder a la interfaz de la API de QGIS
#- Capa activa
layer = qgis.utils.iface.activeLayer()

#- Te muestra todos los métodos disponibles para cualquier objeto. Esto es útil cuando no estás seguro que 
#funciones están disponibles para el objeto. Ejecuta el siguiente comando para ver que operaciones 
#podemos hacer en la variable LAYER.
dir(layer)

#- Te conseguirá la referencia de todos los elementos de una capa.
for f in layer.getFeatures():
    print(f)
    
#- Contiene una referencia a un elementos dentro de la capa. La referencia al elemento está almacenada en 
# la variable f. Podemos usar la variable f para acceder a los atributos de cada elemento.
for f in layer.getFeatures():
    print(f['name'], f['iata_code'])
	
#- Acceder programáticamente al atributo de cada entidad en una capa.
for f in layer.getFeatures():
    geom = f.geometry()
    print(geom.asPoint())

#- Obtener sólo la coordenadas x del elemento.
for f in layer.getFeatures():
    geom = f.geometry()
    print(geom.asPoint().x())

#- Unir para generar el resultado deseado.
for f in layer.getFeatures():
    geom = f.geometry()
    print('%s, %s, %f, %f' % (f['name'], f['iata_code'], geom.asPoint().y(), geom.asPoint().x()))
		 
#- La salida impresa en la consola. Una forma más útil de almacenar la salida sería en un archivo
output_file = open('c:/Users/Ujaval/Desktop/airports.txt', 'w')
for f in layer.getFeatures():
    geom = f.geometry()
    line = '%s, %s, %f, %f\n' % (f['name'], f['iata_code'], geom.asPoint().y(), geom.asPoint().x())
    unicode_line = line.encode('utf-8')
    output_file.write(unicode_line)
output_file.close()

#FUENTE:
#- https://www.qgistutorials.com/es/index.html

#- Listar
iterator = iface.activeLayer().getFeatures()
features = list(iterator)
len(features)
feature = features[0]
feature.geometry()
feature.geometry().asWkt()
feature["wikipedia"]


layer = iface.activeLayer()
layer.fields()
fieldsList = layer.fields().toList()
fieldNames = [f.name() for f in fieldsList]
feature[fieldName[0]]

layer = iface.activeLayer()
features = list(layer.getFeatures())
print(feature[0]["wikipedia"])

#- Suma de datos de una columna
sum([f["POP_EST"] for f in iface.activeLayer().getFeatures()])
sum([f["POP_EST"] for f in iface.activeLayer().getFeatures() if f["CONTINENT"] == "Europe"])
sum([f["POP_EST"] for f in iface.activeLayer().getFeatures('"CONTINENT" = \'Europe\'']))


layer = QgsVectorLayer(r"C:\..\countries.shp", "capa")
layer.getFeatures()
list(layer.getFeatures())

layer = QgsVectorLayer(r"C:\..\countries.shp", "capa")
layer = QgsVectorLayer(r"Point?crs=EPSG:4326", "capa", "memory")
list(layer.getFeatures())
layer.fields().toList() # Te lista la identidad
field = QgsField("id", QVariant.String)
field.name()
layer.addAttribute(field) # Te muestra FALSE. Tenemos que abrir la capa en edición.
layer.fields().toList()
layer.data´Provider().addAttributes([field]) #true
layer.fields().toList()
layer.updateFields() #Actualiza la capa
layer.fields().toList()
layer.fields().toList()[0].name()

feature = QgsFeature()
layer
layer.source()
feature.setFields(layer.fields())
feature.setAttributes(["1"]) # Agregar un dato porqué tengo solo una columna
feature["id"]
feature.setAttribute(0, "3")
feature.setAttribute("id", "3")
feature["id"]

pt = QgsPointXY(1,1)
geom = QgsGeometry.fromPointXY(pt)
geom.asWkt()
feature.setGeometry(geom)
layer.dataProvider().addFeatures([feature])
list(layer.getFeatures())

def createLayer(n):
	layer = QgsVectorLayer("Point?crs=EPSG:4326","capa","memory")
	layer.dataProvider().addAttributes([QgsField("id",QVariant.Int)])
	layer.updateFields()
	fields = layer.fields()
	features = []
	for i in range(n):
		feature = QgsFeature()
		feature.setFields(fields)
		x = random.uniform(-180,180)
		y = random.uniform(-90,90)
		pt = QgsPointXY(x,y)
		geom = QgsGeometry.fromPointXY(pt)
		feature.setGeometry(geom)
		feature.setAttribute(0, i)
		features.append(feature)
	layer.dataProvider().addFeatures(features)
	return layer
	
		
randomLayer = createLayer(50)
print(len(list(randomLayer.getFeatures())))
QgsProject.instance().addMapLayer(randomLayer)

#PARA EJECUTAR EN TERMINAL DE QGIS
exec(open('C:/.../capa.py').encode('utf-8')).read())


layer
layer.source()
layer.crs()
layer.crs().authid()
epsg4326 = QgsCoordinateReferenceSystem("EPSG:4326")
epsg3857 = QgsCoordinateReferenceSystem("EPSG:3857")
transform = QgsCoordinateTransform(epsg4326,epsg3857,QgsProject.instance())
geom = QgsGeometry.fromPointXY(QgsPointXY(1,1))
geom.transform(transform)
geom.asWkt()


#EN FIELD CALCULATE

from qgis.core import *
from qgis.gui import *
@qgsfunction(args="auto",group="Custom", usesgeometry=true)
def hemisphere(geom,feature,parent):
	box = geom.boundingBox()
	if box.yMinimum()>0 and box.yMaximum()>0:
		return "N"
	if box.yMinimum()<=0 and box.yMaximum()<=0:
		return "S"
	else:
		return "B"
	
#LLAMAR A LA EXPRESION
hemisphere($geometry)

#Fuente:
#- GeoAPIsPyQt/QAction
#- volaya/curso-qgis-python


#FUENTE:
#- https://www.youtube.com/watch?v=vZ08dYlM-7U

"""
multipach
overlap
gap
hueco o sobre espuesto
dwg
poligono o linea
- una linea continua y que no tenga roto.
- xyz pierde la altura. Considerar ponigon Zo polinea. 
xyz
"""