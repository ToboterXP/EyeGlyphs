import xml.dom.minidom as xml


material_file = xml.parse("C:\\Users\\tobi1\\Documents\\GitHub\\noita-data\\materials.xml")


material_nodes = list(material_file.getElementsByTagName("CellData")) + list(material_file.getElementsByTagName("CellDataChild"))

color_associations = {}

for node in material_nodes:
    color_val = eval("0x"+node.getAttribute("wang_color"))
    color = ((color_val >> 16) & 0xff, (color_val >> 8) & 0xff, color_val & 0xff, (color_val >> 24) & 0xff)
    name = node.getAttribute("name")

    print(name, len(color_associations.keys()))

    color_associations.setdefault(color, []).append(name)

colors = list(color_associations.keys())
colors.sort(key = lambda a: a[0]*65536 + a[1]*256 + a[2])

with open("material_color_association_list.txt", mode="w") as file:
    for color in colors:
        file.write(f"{color} ; {color_associations[color]}\n")
