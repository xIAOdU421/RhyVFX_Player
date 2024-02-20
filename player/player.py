#
import time

from ursina import *
from functools import partial
import settings
from ui import *
from .textures import *
from .chart import *
from .attrs import *
from .entity import *


class HealthBars(Entity):

    def __init__(self,length):
        super().__init__(model='quad',
            texture='assets/images/ui/healthBar.png',
            parent=gameUi,
            position=(0,-.168,0),
            scale=(length,0.01,1))

        self.health_self = 50
        self.health_enemy = 50

        self.damage = 5
        self.length = length

        self.healthBar_outLine = Entity(

        )

        self.healthBar_enemy = Entity(
            model='quad',
            color=color.red,
            parent=self,
            scale=(0.5, 1, 1),
            origin_x=-0.5,
            position=(-0.5,
                      0,
                      0.00001
                      )
        )
        self.healthBar_self = Entity(
            model='quad',
            color=color.green,
            parent=self,
            scale=(0.5, 1, 1),
            origin_x=0.5,
            position=(0.5,
                      0,
                      0.00001
                      )
        )

    def update(self):
        self.healthBar_self.scale_x = 0.5 * self.health_self / 50
        self.healthBar_enemy.scale_x = 0.5 * self.health_enemy / 50
        if self.health_self >= 100:
            self.health_self = 100
        if self.health_enemy >= 100:
            self.health_enemy = 100

    def input(self,event):
        if debugMode:
            if event == 's':
                self.damage_enemy()
            if event == 'd':
                self.damage_self()

    def damage_self(self):
        if self.health_enemy + self.damage >= 100:
            self.health_enemy = 100
            self.health_self = 0
        else:
            self.health_self -= self.damage
            self.health_enemy += self.damage

    def damage_enemy(self):
        if self.health_self + self.damage >= 100:
            self.health_self = 100
            self.health_enemy = 0
        else:
            self.health_self += self.damage
            self.health_enemy -= self.damage


healthBars = HealthBars(0.4)

class PressAnimation(Entity):
    def __init__(self,arrowId,aniTime,aniTextures,parent,**kwargs):
        super().__init__()
        self.arrowId = arrowId
        self.aniTime = aniTime
        self.aniTextures = aniTextures
        self.parent = parent

        self.aniLast = time.time()
        self.currentFrame = 0

    def update(self):
        if held_keys[settings.keys[self.arrowId]]:
            if time.time() >= self.aniLast + 0.01:
                if self.currentFrame + 1 <= len(self.aniTextures) - 1:
                    self.currentFrame += 1
                self.aniLast = time.time()
        else:
            self.currentFrame = 0
        self.parent.texture = self.aniTextures[self.currentFrame]


class Arrow(Entity):
    def __init__(self,arrowId,parent,timeList,trackLength,unitDis,**kwargs):
        super().__init__()
        self.textures = [
            arrowTextures.arrows.LEFT,
            arrowTextures.arrows.DOWN,
            arrowTextures.arrows.UP,
            arrowTextures.arrows.RIGHT
        ]
        self.pressTextures = [arrowTextures.press.LEFT,
                             arrowTextures.press.DOWN,
                             arrowTextures.press.UP,
                             arrowTextures.press.RIGHT]
        self.pressTexture = self.pressTextures[arrowId]
        self.model = 'quad'
        self.texture = self.textures[arrowId]

        self.y = 0.15
        self.scale = 0.057
        self.originX = -0.075
        self.arrowId = arrowId
        self.x = self.originX + self.scale_x * self.arrowId



        self.arrowAni = partial(
            PressAnimation,
            arrowId=self.arrowId,
            aniTime=0.8,
            aniTextures=[
                self.textures[arrowId],
                self.pressTextures[arrowId][0],
                self.pressTextures[arrowId][1],
                self.pressTextures[arrowId][2],
                self.pressTextures[arrowId][3],
            ],
            parent=self
        )
        self.parent = parent

        self.timeListForSelf = timeList[arrowId]
        self.trackLength = trackLength
        self.unitDis = unitDis
        self.started = False
        self.gameLast = time.time()
        self.currentChart = 0


    def update(self):

        if settings.debugMode:
            self.x += held_keys['d'] * 0.001
            self.x -= held_keys['a'] * 0.001
            self.y += held_keys['w'] * 0.001
            self.y -= held_keys['s'] * 0.001
        # print(time.time()-self.gameLast,self.timeListForSelf[self.currentChart])

        if self.currentChart < len(self.timeListForSelf):
            if time.time()-self.gameLast >= list(self.timeListForSelf.keys())[self.currentChart]:
                tailLength = self.timeListForSelf[list(self.timeListForSelf.keys())[self.currentChart]]
                Chart(
                    bindArrow=self,
                    originY=self.unitDis*self.trackLength,
                    speed=self.unitDis,parent=self.parent,
                    tailLength=tailLength,
                    trackId=self.arrowId
                )


                self.currentChart += 1


    def input(self,event):

        if event == settings.keys[self.arrowId]:

            self.arrowAni()
            try:
                chart = find_nearest_specific_entity(self)
                chart.chartPress()
            except Exception:
                pass



class GameSurface(Entity):
    def __init__(self,songName,surfaceLength,unitDis,botplay=False,):
        super().__init__(z=1.2)
        self.songName = songName
        self.surfaceLength = surfaceLength
        self.unitDis = unitDis
        self.botplay = botplay
        self.timeList = unit2time(songName)
        self.started = False
        self.startLast = time.time()
        self.offset = self.surfaceLength/200

        self.arrow1 = Arrow(0,parent=self,timeList=self.timeList,trackLength=surfaceLength,unitDis=unitDis)
        self.arrow2 = Arrow(1,parent=self,timeList=self.timeList,trackLength=surfaceLength,unitDis=unitDis)
        self.arrow3 = Arrow(2,parent=self,timeList=self.timeList,trackLength=surfaceLength,unitDis=unitDis)
        self.arrow4 = Arrow(3,parent=self,timeList=self.timeList,trackLength=surfaceLength,unitDis=unitDis)

        # Entity(model='quad',
        #        # parent=self,
        #        scale=(30,0.001,1),
        #        z=self.world_position.z,
        #        y=self.arrow1.y - (self.unitDis * (ranks['sick']/ 1000 * 200)))
        # #
        # Entity(model='quad',
        #        # parent=self,
        #        scale=(30,0.001,1),
        #        z=self.world_position.z,
        #        y=self.arrow1.y - (self.unitDis * (ranks['good']/ 1000 * 200)))
        # Entity(model='quad',
        #        # parent=self,
        #        scale=(30,0.001,1),
        #        z=self.world_position.z,
        #        y=self.arrow1.y - (self.unitDis * (ranks['bad']/ 1000 * 200)))
        # Entity(model='quad',
        #        # parent=self,
        #        scale=(30,0.001,1),
        #        z=self.world_position.z,
        #        y=self.arrow1.y - (self.unitDis * (ranks['shit']/ 1000 * 200)))

        # a = Entity(model='quad',
        #        scale=(30,0.001,1),
        #        y=self.arrow1.y - (self.unitDis*ranks['miss']*0.001/200),
        #        z = self.z,
        #        parent=self
        # )
        # print(a.y)


    def update(self):
        if settings.debugMode:
            print_on_screen(self.arrow1.x)

        if not self.started and time.time() >= self.startLast + self.offset:
            # print(True)
            self.sound = Audio(f'./assets/Musics/{self.songName}/Inst.ogg')
            self.started = True

    # def update(self):
    #     self.rotation_z += 1



# gameSuface2 = GameSurface()
# gameSuface.x = -0.2
# gameSuface2.x = 0.2

class RankText(Entity):
    def __init__(self,rank,score,**kwargs):
        super().__init__(
            model='quad',
            parent=gameUi,
            scale=(0.12,0.05)
        )
        self.textures = {
            'sick':'./assets/images/sick.png',
            'good': './assets/images/good.png',
            'bad': './assets/images/bad.png',
            'shit': './assets/images/shit.png'
        }
        self.texture = self.textures[rank]
        self.animate_position((
            self.x,self.y-0.05,self.z
        ),duration=0.5,curve=curve.in_back)
        self.aniLast = time.time()

    def update(self):
        self.alpha = 1 - (time.time() - self.aniLast)*2

        if self.alpha < 0:
            destroy(self)
        # print_on_screen(self.alpha)





class Chart(Entity):
    def __init__(self,bindArrow,originY,parent,speed,tailLength,trackId):
        super().__init__()
        self.noteTexture = [
            arrowTextures.note_alone.PURPLE,
            arrowTextures.note_alone.BLUE,
            arrowTextures.note_alone.GREEN,
            arrowTextures.note_alone.RED,
        ]
        self.model = 'quad'
        self.parent = parent
        # self.x = 1
        self.scale = bindArrow.scale
        self.texture = self.noteTexture[bindArrow.arrowId]
        self.y = bindArrow.y - originY
        self.bindArrow = bindArrow
        self.speed = speed
        self.originY = self.y
        self.x = bindArrow.x
        self.z = -0.000001
        self.speed = speed
        # self.unitId
        self.aniLast = time.time()
        self.missed = False
        self.trackId = trackId
        self.tail = Tail(bindObj=self, length_unit=tailLength, parent=self.parent, unitDis=self.speed)


        chartEntity.append(self)


    def update(self):

        global currentMisses
        global currentScore
        global currentDestroy
        # print_on_screen(currentDestroy)
        self.y = self.originY + (time.time()-self.aniLast)*200 * self.speed

        if self.y > self.bindArrow.y + (self.speed*ranks['miss']/1000*200) and not self.missed:


            currentMisses += 1
            healthBars.damage_self()
            currentScore += rankScore['miss']
            self.missed = True
        try:
            if self.y > self.bindArrow.y + (self.speed * ranks['miss'] / 1000 * 200) + self.tail.scale_y:
                destroy(self.tail)
                destroy(self)
                chartEntity.remove(self)
        except Exception:
            if self.y > self.bindArrow.y + (self.speed * ranks['miss'] / 1000 * 200):
                destroy(self)
                chartEntity.remove(self)


        # print(self.y)

    def input(self,event):
        global currentPressChart
        global currentDestroy

    def chartPress(self):
        global currentScore
        if self.y >= self.bindArrow.y - (self.speed*ranks['miss']/1000*200):

            self.tail.bindObj = self.bindArrow
            self.tail.needHold = True
            healthBars.damage_enemy()
            print(1)
            currentScore += 300 - int(abs(self.bindArrow.y - self.y) * 10)
            print(2)
            destroy(self)
            chartEntity.remove(self)



class Tail(Entity):
    def __init__(self,bindObj,length_unit,parent,unitDis):
        super().__init__()



        self.model = 'quad'
        self.origin_y = 0.5
        self.parent = parent

        # self.noteTexture = [
        #     arrowTextures.note_alone.PURPLE,
        #     arrowTextures.note_alone.BLUE,
        #     arrowTextures.note_alone.GREEN,
        #     arrowTextures.note_alone.RED,
        # ]

        self.textures = [
            arrowTextures.holds.PURPLE,
            arrowTextures.holds.BLUE,
            arrowTextures.holds.GREEN,
            arrowTextures.holds.RED
        ]
        self.texture = self.textures[bindObj.trackId]

        self.scale = (bindObj.scale_x * 0.3, length_unit * unitDis)
        self.bindObj = bindObj
        self.unitDis = unitDis
        self.needHold = False

        self.length_unit = length_unit
        self.needHoldLast = False
        self.missed = False



    def update(self):
        global currentScore
        global currentMisses

        # if self.scale_y <= 1 ^ 20:

        if self.scale_y <= 9.999999717180685e-9:
            destroy(self)
            return

        try:
            if not held_keys[settings.keys[self.bindObj.arrowId]]:
                self.needHold = False
        except Exception:
            pass


        if self.needHold and not self.needHoldLast:
            self.aniLast = time.time()
            self.scale_y -= (self.y - self.bindObj.y)
            self.aniStart = self.scale_y
            self.needHoldLast = True
            self.damageLast = time.time()


        if self.needHold:
            self.scale_y = (self.aniStart-((time.time()-self.aniLast)*200*self.unitDis))
            if time.time() >= self.damageLast + 0.3:
                healthBars.damage_enemy()
                currentScore += 50
                self.damageLast = time.time()


        elif not self.needHold and isinstance(self.bindObj,Arrow):
            if not self.missed:
                currentMisses += 1
                self.missed = True
            self.alpha -= 0.01
            if self.alpha <= 0.02:
                destroy(self)
                return

        self.x = self.bindObj.x
        self.z = self.bindObj.z
        self.y = self.bindObj.y

    def input(self,event):
        pass
        # print(event)







# Chart(gameSuface.arrow1,originY=5,speed=0.3)
# Chart(gameSuface.arrow2,originY=5,speed=0.3)
# Chart(gameSuface.arrow3,originY=5,speed=0.3)
# Chart(gameSuface.arrow4,originY=5,speed=0.3)

def update():
    global currentScore
    currentScore = int(currentScore)
    # print(currentScore)
    gameUi.score.text = 'Score:'+str(currentScore)
    gameUi.misses.text = 'Misses:'+str(currentMisses)







if __name__ == '__main__':
    app = Ursina()
    EditorCamera()

    window.borderless = False
    app.run()


