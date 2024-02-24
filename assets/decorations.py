import random

from ursina import *



class Cities(Entity):
    def __init__(self,z,x,x_offset=0):
        super().__init__(
            model='quad',
            texture=f'./assets/images/cities{random.randint(1,5)}.png',
            scale=(20,5,1),
            z=z,
            y=-3,
            x=x,
            alpha=0.6
        )
        self.x += random.uniform(0,x_offset)
        self.animate_position((self.x-60,self.y,self.z),duration=10,curve=curve.linear)
        self.startX = self.x

    def update(self):
        if self.x <= self.startX - 60:
            destroy(self)


if __name__ == '__main__':
    app = Ursina()
    window.borderless = False

    Cities(1)
    app.run()
