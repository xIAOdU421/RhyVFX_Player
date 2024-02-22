import random

from ursina import *



class Cities(Entity):
    def __init__(self,z,x_offset=0):
        super().__init__(
            model='quad',
            texture=f'./assets/images/cities{random.randint(1,5)}.png',
            scale=(20,5,1),
            z=z,
            y=-3,
            x=0
        )
        self.x += random.uniform(0,x_offset)


if __name__ == '__main__':
    app = Ursina()
    window.borderless = False

    Cities(1)
    app.run()
