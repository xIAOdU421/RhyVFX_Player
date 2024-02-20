from ursina import *
from player.player import *
from ursina.camera import *

gameSurface = GameSurface(songName='raining',surfaceLength=500,unitDis=0.003)

class Flash(Entity):
    def __init__(self,time,initColor,finishColor,**kwargs):
        super().__init__(
            model='quad',
            color=initColor,
            parent=camera.ui,
            scale=2
        )
        self.animate_color(finishColor,duration=time)

Flash(3,color.black,color.clear)



