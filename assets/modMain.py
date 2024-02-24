from ursina import *
from player.player import *
from ursina.camera import *
from .decorations import *

window.color = color.black

gameSurface = GameSurface(songName='raining', surfaceLength=500, unitDis=0.006, autoplay=True)

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
genInterval = 10
last = time.time()

for i in range(3,23):
    Cities(z=i,x=0,x_offset=20)
    Cities(z=i,x=20,x_offset=20)


actions = {

}




class CameraShake(Entity):

    def __init__(self,shake_obj):
        super().__init__()
        self.amplitude = 0.02
        # self.duration = 0.4
        self.duration = 60 / 155.01 * 4
        self.curve = curve.in_out_sine

        self.rotate_amplitude = 5

        self.last = time.time()

        # self.shake_obj = Entity(model='cube',
        #                   color=color.orange)
        self.shake_obj = shake_obj
        self.shake_allowed = True

    def update(self):

        if time.time() >= self.last + self.duration and self.shake_allowed:
            self.shake_obj.animate_position((
                random.uniform(self.amplitude,-self.amplitude),
                random.uniform(self.amplitude,-self.amplitude),
                random.uniform(0+self.amplitude,0-self.amplitude)
            ),
            duration=self.duration,
            curve=self.curve)


            self.shake_obj.animate_rotation((
                # random.uniform(self.rotate_amplitude,-self.rotate_amplitude),
                # random.uniform(self.rotate_amplitude,-self.rotate_amplitude),
                0,
                0,
                random.uniform(self.rotate_amplitude,-self.rotate_amplitude)
            ),
            duration=self.duration,
            curve=self.curve)
            # print(camera.fov)


            self.last = time.time()





class GameLoop(Entity):
    def update(self):
        global last
        if time.time() >= last+5:
            for i in range(3,23):
                Cities(z=i,x=20,x_offset=20)
            last = time.time()

        # cameraShadow.world_position = camera.world_position
        # cameraShadow.world_rotation = -camera.world_rotation
        # print_on_screen(cameraShadow.world_rotation)


CameraShake(camera)
GameLoop()
cameraShadow = Entity(
    model='quad',
    parent=camera.ui,
    texture='./assets/images/camera_shadow.png',
    scale=(2,1,1),
    color=(50,50,50)
)




