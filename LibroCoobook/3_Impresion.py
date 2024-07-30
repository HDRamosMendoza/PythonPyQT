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
)

from qgis.PyQt.QtGui import (QPolygonF, QColor)
from qgis.PyQt.QtCore import (QPointF, QRectF, QSize)

import MapComposer2

image_location = os.path.join(QgsProject.instance().homePath(), "UE003_{0}_{1}.png".format(time.strftime("%d%m%y"),time.strftime("%H%M%S")))

vlayer = QgsVectorLayer("Ciudad_de_Ayacucho.shp", "Ciudad de Ayacucho", "ogr")
project = QgsProject.instance()

if not vlayer.isValid():
    print("Capa fallo al cargar")
else:
    project.addMapLayer(vlayer)

"""
layers = [iface.activeLayer()]
settings = QgsMapSettings()
settings.setLayers(layers)
settings.setDestinationCrs(layers[0].crs())
settings.setBackgroundColor(QColor(255, 255, 255))
settings.setOutputSize(QSize(1122.5,793.7)) # A4 LANSCAPE 1122.5x793.7
# A4 PORTRAIT
# A3 1122.5 x 1587.4
settings.setExtent(layers[0].extent())

render = QgsMapRendererParallelJob(settings)

layout = QgsPrintLayout(project)
layout.initializeDefaults()
layout.setName("MyLayout")
project.layoutManager().addLayout(layout)


map = QgsLayoutItemMap(layout)
map.attempt(QgsLayoutPoint(5,5,QgsUnitTypes.LayoutMillimeters))
map.attemptResize(QgsLaoutSize(200,200,QgsUnitTypes.LoutMillimeters))
map.zoomToExtent(iface.mapCanvas().extent)
layout.addLayoutItem(map)


def finished():
	img = render.renderedImage()
	# save the image; e.g. img.save("/Users/myuser/render.png","png")
	img.save(image_location, "png")

render.finished.connect(finished)

# Start the rendering
render.start()

# The following loop is not normally required, we
# are using it here because this is a standalone example.
from qgis.PyQt.QtCore import QEventLoop
loop = QEventLoop()
render.finished.connect(loop.quit)
loop.exec_()
"""