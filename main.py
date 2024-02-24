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

# sys.stdout = open('stdout','w')
# EditorCamera()
window.borderless = False

from mod import *

mod = Mod()
# camera.fov = 60
camera.shader = camera_vertical_blur_shader
camera.z = 0



game.run()