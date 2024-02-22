import settings
from importlib import import_module
from ursina import *

class Mod(Entity):
    def __init__(self):
        super().__init__()
        self.startText = Text('Press any key to start',scale=1.2,origin=(0,0,0))
        self.started = False
        self.mod = None

    def input(self,event):
        if event and not self.started:
            destroy(self.startText)
            self.mod = import_module(f'assets.mods.{settings.currentSong}.main')
            self.started = True