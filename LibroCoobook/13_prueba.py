"""
list_lyr_2 = ["ramos", "mendoza", "heber", "daniel", "juan"]
list_lyr = ["juan"]

for item in list_lyr_2:
    if item not in list_lyr:
        list_lyr.append(item)

print(list_lyr)
"""


"""
list_lyr_2 = ["ramos", "mendoza", "heber", "daniel", "juan"]
list_lyr = [{
           "layer" : "ramos",
           "shp":"uno"
        }]
existing_layers = {item["layer"] for item in list_lyr}

for item in list_lyr_2:
    if item not in existing_layers:
        list_lyr.append({
           "layer" : item,
           "shp": "dos"
        })

print(list_lyr[0])
print(list_lyr[0]["layer"])
print(list_lyr[0]["shp"])
"""

input_list_files_extension = [
            { 
                "format": "KML"
                , "extension": "kml"
                , "download": ""
            }, {
                "format": "ESRI Shapefile"
                , "extension": "shp"
                , "download": ""
            }, { 
                "format": "GeoJSON"
                , "extension": "geojson"
                , "download": ""
            }, { 
                "format": "DXF"
                , "extension": "dxf"
                , "download": ""
            }
        ]
print(input_list_files_extension[0]["download"])

print("Prueba")
abc = 'epsg:32718'
a1, a2 = abc.split(':')
print(a1)
print(a2)