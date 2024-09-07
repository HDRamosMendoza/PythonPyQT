import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QListWidget, QMessageBox
from qgis.utils import iface

path_folder = r"0_data"
gpkg_path = r"0_temp/prueba.gpkg"

def exportSubLayerToGPKG(self, file_path, sub_layer_name, gpkg_path):
        # Cargar sub capa
        sub_layer_uri = f"'{file_path}'|layername={sub_layer_name}"
        sub_layer = QgsVectorLayer(sub_layer_uri, sub_layer_name, "ogr")
        
        if not sub_layer.isValid():
            print(self, "Error", f"No se pudo cargar la sub capa {sub_layer_name}.")
            return
        
        # Definir el CRS para la capa
        crs = QgsCoordinateReferenceSystem("EPSG:4326")
        sub_layer.setCrs(crs)
        
        # Exportar a GeoPackage
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = "GPKG"
        options.layerName = sub_layer_name
        options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
        
        error = QgsVectorFileWriter.writeAsVectorFormat(sub_layer, gpkg_path, options)
        
        if error[0] != QgsVectorFileWriter.NoError:
            print("Error", f"Error al exportar la sub capa {sub_layer_name} a GeoPackage.")
            return
        
# Importa datos
def importDWG(file_path):
    # Usar QGIS para cargar y convertir DWG/DXF
    print(os.path.join(os.getcwd(),file_path))
    file_path = os.path.join(os.getcwd(),file_path)
    
    print (os.path.basename(file_path))
    
    layer = QgsVectorLayer(f"CAD:{file_path}|layername=entities", os.path.basename(file_path), "ogr")
    print(layer)
    
    #QgsProject.instance().addMapLayer(layer)
    
    # Listar las capas dentro del DWG/DXF
    sub_layers = layer.dataProvider().subLayers()
    print(sub_layers)
    sub_layer_names = [sub_layer.split(':')[-1] for sub_layer in sub_layers]
    
    # Seleccionar ruta para guardar el GeoPackage
    #gpkg_path, _ = QFileDialog.getSaveFileName(self, "Guardar como GeoPackage", "", "GeoPackage (*.gpkg)")
    print("RUTA")
    print(gpkg_path)
    if gpkg_path:
        # Iterar sobre sub capas y exportarlas
        print(sub_layer_names)
        for sub_layer_name in sub_layer_names:
            print("NOMBRES")
            print(sub_layer_name)
            exportSubLayerToGPKG(file_path, sub_layer_name, gpkg_path)
            
        print("Éxito", f"El archivo {file_path} se ha convertido exitosamente a {gpkg_path}.")

    
# Lista todos los archivos DWG o DXF
def listDWGFiles():
    listWidget = []    
    # Listar archivos DWG/DXF en la carpeta
    dwg_files = [f for f in os.listdir(path_folder) if f.endswith('.dwg') or f.endswith('.dxf')]
    # path_files = [f for f in os.listdir(path_folder) if f.lower().endswith(('.dwg', '.dxf'))]
    for dwg_file in dwg_files:
        listWidget.append(dwg_file)
    return listWidget

def main():
    print("* * * * * * * * * * * * * * * *")
    # Obtener la lista de archivos seleccionados
    pathDWGFiles = listDWGFiles()
    #selected_files = [item.text() for item in self.listWidget.selectedItems()]
    selected_files = [item for item in pathDWGFiles]    
    if not selected_files:
        print("Error")
        return
    
    for dwg_file in selected_files:
        file_path = os.path.join(path_folder, dwg_file)
        print(file_path)
        importDWG(file_path)

main()
"""
def importDWG(self, file_path):
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
            
        QMessageBox.information(self, "Éxito", f"El archivo {file_path} se ha convertido exitosamente a {gpkg_path}.")

def exportSubLayerToGPKG(self, file_path, sub_layer_name, gpkg_path):
    # Cargar sub capa
    sub_layer_uri = f"'{file_path}'|layername={sub_layer_name}"
    sub_layer = QgsVectorLayer(sub_layer_uri, sub_layer_name, "ogr")
    
    if not sub_layer.isValid():
        QMessageBox.critical(self, "Error", f"No se pudo cargar la sub capa {sub_layer_name}.")
        return
    
    # Definir el CRS para la capa
    crs = QgsCoordinateReferenceSystem("EPSG:4326")
    sub_layer.setCrs(crs)
    
    # Exportar a GeoPackage
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GPKG"
    options.layerName = sub_layer_name
    options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
    
    error = QgsVectorFileWriter.writeAsVectorFormat(sub_layer, gpkg_path, options)
    
    if error[0] != QgsVectorFileWriter.NoError:
        QMessageBox.critical(self, "Error", f"Error al exportar la sub capa {sub_layer_name} a GeoPackage.")
        return
"""