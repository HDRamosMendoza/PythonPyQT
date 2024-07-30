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
