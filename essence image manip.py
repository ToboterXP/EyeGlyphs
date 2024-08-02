import pygame as pg
import time

pg.init()

#img = pg.image.load("essenceroom_visual.png")
oimg = pg.image.load("translateddiamond.png")

scale = 2

for i in (0,1,2):
    for b in range(8):
        img = oimg.copy()
        for x in range(img.get_width()):
            for y in range(img.get_height()):
                c = img.get_at((x,y))
                #t = c[i] & (1<<b)
                #if t:
                 #   c = (255,255,255)
                #else:
                #    c= (0,0,0)
                
                img.set_at((x,y),c)

        img = pg.transform.scale(img,(img.get_width()*scale, img.get_height()*scale))
        #pg.image.save(img, f"diamond dump/diamond_{'rgb'[i]}{b}.png")

        d = pg.display.set_mode(img.get_size())
        d.blit(img,(0,0))
        pg.display.flip()
        pg.event.pump()

        input(f"{'rgb'[i]}{b}")
