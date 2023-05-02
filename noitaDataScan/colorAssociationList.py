import os

SEARCH_PATH = "C:\\Users\\tobi1\\Documents\\GitHub\\noita-data\\scripts\\biomes"

EXCLUDES = ["debug_biomes.lua"]

color_associations = {}
color_associations_full = {}

for root, subdirs, files in os.walk(SEARCH_PATH):
    for filename in files:
        full_path = os.path.join(root,filename)
        part_path = full_path.replace(SEARCH_PATH+"\\", "")

        excluded = False
        for exclude in EXCLUDES:
            if exclude in full_path:
                excluded = True
        if excluded:
            continue
            
        if ".lua" in filename:
            print(part_path, len(color_associations.keys()))
            color_assocs = []
            
            with open(full_path) as file:
                for line in file.read().split("\n"):
                    if "RegisterSpawnFunction" in line:
                        color = None
                        name = None
                        for sect in line.split(" "):
                            if "0x" in sect:
                                color_val = eval(sect[:-1])
                                color = ((color_val >> 16) & 0xff, (color_val >> 8) & 0xff, color_val & 0xff, (color_val >> 24) & 0xff)
                            elif "\"" in sect:
                                name = sect[1:-1]

                        color_assocs.append((color,name))

            for color, name in color_assocs:
                color_associations.setdefault(color, set()).add(name)
                color_associations_full.setdefault(color, set()).add(name+f" ({part_path})")

colors = list(color_associations.keys())
colors.sort(key = lambda a: a[0]*65536 + a[1]*256 + a[2])

with open("color_association_list.txt", mode="w") as file:
    for color in colors:
        file.write(f"{color} ; {color_associations[color]}\n")

with open("color_association_with_script_names_list.txt", mode="w") as file:
    for color in colors:
        file.write(f"{color} ; {color_associations_full[color]}\n")
                                
                                
