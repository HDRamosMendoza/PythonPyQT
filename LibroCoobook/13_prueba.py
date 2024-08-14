"""
list_lyr_2 = ["ramos", "mendoza", "heber", "daniel", "juan"]
list_lyr = ["juan"]

for item in list_lyr_2:
    if item not in list_lyr:
        list_lyr.append(item)

print(list_lyr)
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