# PythonPyQT
Avance de aprendizaje en PyQt

- Puntos a tomar en cuenta:

Python 		 3.9
QGIS Desktop 		3.32.3
Postgresql (5432) 	15.7.2
	PostGIS 3.4		3.4.1
	
Plugins > Manage and Install Plugin > 
Not installed : 
	- Plugin builder 3
	- Plugin reloader


pb_tool.cfg: En donde debe de quedar desplegado
Línea 47: C:/Users/heber/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins 

Instalar PB TOOL
pip install pb-tool
pip install PyQt5

pb_tool deploy

Para recompilar 
pyrcc5 -o resources.py resources.qrc

Ruta en donde se almacena el plugin
User/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins

plugin_reloader
pluginbuilder3

- En el caso de no reflejar los cambios. Validar la carpeta publicada del plugin con el ambiente de desarrollo.
Copying help/build/html to C:/Users/heber/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins\acceso_sistema

- Libro.
https://docs.qgis.org/3.22/pdf/es/QGIS-3.22-PyQGISDeveloperCookbook-es.pdf