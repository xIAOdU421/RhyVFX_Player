#
import random
import sys

from ursina import *

game = Ursina()
import settings
from ui import *
from player import *
from ursina.shaders import camera_vertical_blur_shader
from player.player import *
# EditorCamera()

sys.stdout = open('stdout','w')

window.borderless = False

gameSurface = GameSurface(songName='raining',surfaceLength=500,unitDis=0.003)

camera.z = 0



game.run()