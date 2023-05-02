

color_associations = {}

print("Loading Associtations...")
with open("full_color_association_list.txt") as file:
    for line in file.readlines():
        color, names = line.split(";")
        color = eval(color)
        names = eval(names)
        color_associations[color] = names

spawn_pixels = {}

print("Loading spawn pixel types...")
with open("spawn_pixel_list.txt") as file:
    with open("material_pixel_list.txt") as file2:
        for line in tuple(file.readlines()) + tuple(file2.readlines()):
            color, names = line.split(";")
            color = eval(color)
            names = eval(names)
            for n in names:
                spawn_pixels.setdefault(color, []).append(n)


spawn_pixel_colors = list(spawn_pixels.keys())
spawn_pixel_colors.sort(key = lambda a: a[0]*65536 + a[1]*256 + a[2])

with open("spawn_pixel_assoc_list.txt", "w") as file:
    for color in spawn_pixel_colors:
        file.write(f"{color} ; {color_associations.get(color,'<undefined>')} ; {spawn_pixels[color]}\n")


