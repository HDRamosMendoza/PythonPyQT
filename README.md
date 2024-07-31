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

- Para exportar las carpetas personalizadas al usar pb_tool deploy. Se agrega ui e images que son carpetas que tienen diversos archivos.
extra_dirs: ui images

- Libro.
https://docs.qgis.org/3.22/pdf/es/QGIS-3.22-PyQGISDeveloperCookbook-es.pdf

- Python de QGIS. Al abrir la consola de QGIS no se tiene pip.
Para instalar pip en el python de QGIS. Se debe de instalar por subprocesos.

1. Instalar pip
	import subprocess
	subprocess.run(['python', 'get-pip.py'])
	subprocess.run(['pip', '--version'])

2. Instalar ezdxf
	import subprocess
	subprocess.run(['pip', 'install', 'ezdxf'])

	import ezdxf
	print(ezdxf.__version__)

3. Instalar y actualizar numpy
	import subprocess
	subprocess.run(['pip', 'install', '--upgrade', 'numpy'])

