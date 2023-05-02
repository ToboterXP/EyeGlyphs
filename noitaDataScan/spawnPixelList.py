import os
from PIL import Image

BIOME_IMPL_PATH = "C:\\Users\\tobi1\\Documents\\GitHub\\noita-data\\biome_impl"
WANG_PATH = "C:\\Users\\tobi1\\Documents\\GitHub\\noita-data\\wang_tiles"


EXCLUDES = ["biome_map","background","visual","logo","pillars","caves","hidden", \
            "right_entrance", "right_stub", "boss_arena_statue", "spliced", "mountain\\top", "right_bottom.png", "paneling", "drape_", "vault\\entrance"]

spawn_pixels = {}
material_pixels = {}

def scan_file(root, full_path, prefix):
    true_path = full_path
    full_path = prefix+full_path.replace(root+"\\", "")
        
    excluded = False
    for exclude in EXCLUDES:
        if exclude in full_path or exclude in filename:
            excluded = True
    if excluded:
        return
            
    if ".png" in full_path:
        print(full_path, len(spawn_pixels.keys()), len(material_pixels.keys()))
        found_colors = []
        discarded_colors = []
        
        image = Image.open(true_path)
        
        for x in range(image.size[0]):
            for y in range(image.size[1]):
                pixel = image.getpixel((x,y))

                if pixel in found_colors or pixel in discarded_colors:
                    continue

                if pixel[0] == pixel[1] and pixel[1] == pixel[2]:
                    continue

                spawn_pixel = True
                for xOff in range(-1,2):
                    for yOff in range(-1,2):
                        if xOff == 0 and yOff == 0:
                            continue

                        try:
                            if all(map(lambda a: a[0]==a[1], zip(pixel, image.getpixel((x+xOff, y+yOff))))):
                                spawn_pixel = False
                                break
                        except IndexError:
                            pass
                        
                    if not spawn_pixel:
                        break

                if spawn_pixel:
                    found_colors.append(pixel)
                else:
                    discarded_colors.append(pixel)

        for color in found_colors:
            if len(color) == 3:
                color += (255,)
            spawn_pixels.setdefault(color, []).append(full_path)
        for color in discarded_colors:
            if len(color) == 3:
                color += (255,)
            material_pixels.setdefault(color, []).append(full_path)
    

print("Scanning biome_impl ...")
for root, subdirs, files in os.walk(BIOME_IMPL_PATH):
    for filename in files:
        scan_file(BIOME_IMPL_PATH, os.path.join(root,filename), "biome_impl\\")

print("Scanning wang_tiles ...")
for root, subdirs, files in os.walk(WANG_PATH):
    for filename in files:
        scan_file(WANG_PATH, os.path.join(root,filename),"wang_tile\\")

        


spawn_pixel_colors = list(spawn_pixels.keys())
spawn_pixel_colors.sort(key = lambda a: a[0]*65536 + a[1]*256 + a[2])

with open("spawn_pixel_list.txt",mode="w") as file:
    for color in spawn_pixel_colors:
        file.write(f"{color} ; {spawn_pixels[color]}\n")

material_pixel_colors = list(material_pixels.keys())
material_pixel_colors.sort(key = lambda a: a[0]*65536 + a[1]*256 + a[2])

with open("material_pixel_list.txt",mode="w") as file:
    for color in material_pixel_colors:
        file.write(f"{color} ; {material_pixels[color]}\n")

print("Saved pixels")


print("Ambiguous pixels:")
for pixel in spawn_pixel_colors:
    if pixel in material_pixel_colors:
        print(f"{pixel} {spawn_pixels[pixel]} {material_pixels[pixel]}")
        
                


                                
            
            
            
        
