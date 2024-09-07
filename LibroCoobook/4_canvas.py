import ezdxf 
print("HOLA MUNDO")

import pkg_resources

installed_packages = pkg_resources.working_set
installed_packages_list = sorted([f"{package.project_name}=={package.version}" for package in installed_packages])

for package in installed_packages_list:
    print(package)

"""
canvas = QgsMapCanvas()
canvas.show()
vlayer = QgsVectorLayer("Ciudad_de_Ayacucho.shp", "Ciudad de Ayacucho", "ogr")
if not vlayer.isValid():
    print("Capa fallo al cargar")
else:
    QgsProject.instance().addMapLayer(vlayer)
canvas.setCanvasColor(Qt.white)
canvas.enableAntiAliasing(True)
canvas.setExtent(vlayer.extent())
# Se cambia el canvas del mapa
canvas.setLayers([vlayer])
"""