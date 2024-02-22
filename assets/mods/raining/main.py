from ursina import *
from player.player import *
from ursina.camera import *
from .decorations import *

gameSurface = GameSurface(songName='raining', surfaceLength=500, unitDis=0.003, autoplay=True)

class Flash(Entity):
    def __init__(self,time,initColor,finishColor,**kwargs):
        super().__init__(
            model='quad',
            color=initColor,
            parent=camera.ui,
            scale=2
        )
        self.animate_color(finishColor,duration=time)

# Flash(10,color.black,color.clear)
for i in range(20):
    Cities(z=i,x_offset=1)



