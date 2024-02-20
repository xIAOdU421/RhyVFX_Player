import settings
from importlib import import_module

class Mod():
    def __init__(self):
        self.mod = import_module(f'assets.data.{settings.currentSong}.main')
