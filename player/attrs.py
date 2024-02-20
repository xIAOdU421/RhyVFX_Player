from .chart import *
import settings

chartData = getChartAttr(settings.currentSong)

ranks = {
    'sick':50,
    'good':100,
    'bad':150,
    'shit':200,
    'miss':300
}

rankScore = {
    'sick':300,
    'good':150,
    'bad':100,
    'shit':50,
    'miss':-100
}
currentScore = 0
currentMisses = 0
