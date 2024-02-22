#
from ursina import *

import settings
from settings import *


class GameUi_basic(Entity):

    def __init__(self):
        super().__init__()
        self.z = 1.2
        self.parent = camera.ui
        # self.scale=10
        self.texts = {
            'score':'Score:0',
            'misses':'Misses:0',
            'accuracy':'Accuracy:0',
            'rating':'None'
        }
        self.uiPos = {
            # 'score':(-.168,-.18,0),
            'score':(-.068,-.17,0),
            'misses':(.032,-.17,0),
            # 'rating':(.132,-.18,0),
            # 'rating':(.132,-.18,0),
            'rating': (114, 514, 0),
            'accuracy':(191,9810,0)
        }

        self.uiStyle = {
            'textScale':0.4,
        }

        self.scale = 2.5

        self.score = Text(text=self.texts['score'],
                          position=self.uiPos['score'],
                          parent=self,
                          scale=self.uiStyle['textScale']
                          )
        self.misses = Text(text=self.texts['misses'],
                          position=self.uiPos['misses'],
                          parent=self,
                           scale=self.uiStyle['textScale']
                           )
        self.accuracy = Text(text=self.texts['accuracy'],
                          position=self.uiPos['accuracy'],
                          parent=self,
                             scale=self.uiStyle['textScale']
                          )
        self.rating = Text(text=self.texts['rating'],
                          position=self.uiPos['rating'],
                          parent=self,
                           scale=self.uiStyle['textScale']
                          )
        # self.startButton = Button('Start!')


if __name__ == '__main__':
    app = Ursina()
    window.borderless = False
    EditorCamera()
    camera.z = 0
    # tester = Entity(model='cube')



if settings.gameUi_style == 'basic':
    gameUi = GameUi_basic()


if __name__ == '__main__':
    app.run()


