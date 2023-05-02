

color_associations = {}

print("Processing script colors...")
with open("color_association_list.txt") as file:
    for line in file.readlines():
        color, names = line.split(";")
        color = eval(color)
        names = list(eval(names))
        names = list(map(lambda n: "script:"+n, names))
        for n in names:
            color_associations.setdefault(color, []).append(n)

print("Processing material colors...")
with open("material_color_association_list.txt") as file:
    for line in file.readlines():
        color, names = line.split(";")
        color = eval(color)
        names = eval(names)
        names = list(map(lambda n: "material:"+n, names))
        for n in names:
            color_associations.setdefault(color, []).append(n)


print("Processing Noita wang scripts...")
with open("C:\\Users\\tobi1\\Documents\\GitHub\\noita-data\\scripts\\wang_scripts.csv") as file:
    for line in file.readlines()[1:]:
        parts = line.split(",")
        color_val = eval("0x"+parts[0])
        color = ((color_val >> 16) & 0xff, (color_val >> 8) & 0xff, color_val & 0xff, (color_val >> 24) & 0xff)
        name = "wang_script:"+parts[1]
        color_associations.setdefault(color, []).append(name)

print("Processing Noita removed wang scripts...")
with open("C:\\Users\\tobi1\\Documents\\GitHub\\noita-data\\scripts\\wang_scripts_removed.txt") as file:
    for line in file.readlines():
        color,name = line.split(" ")
        color_val = eval("0x"+color)
        color = ((color_val >> 16) & 0xff, (color_val >> 8) & 0xff, color_val & 0xff, (color_val >> 24) & 0xff)
        name = "wang_script_removed:"+name
        color_associations.setdefault(color, []).append(name)
        


colors = list(color_associations.keys())
colors.sort(key = lambda a: a[0]*65536 + a[1]*256 + a[2])

with open("full_color_association_list.txt", mode="w") as file:
    for color in colors:
        file.write(f"{color} ; {color_associations[color]}\n")
