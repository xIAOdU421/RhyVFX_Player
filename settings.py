#
import json

with open('./sets.json','r') as f:
    setDatas = json.load(f)

keys = setDatas['keys']
gameUi_style = setDatas['gameUi_style']
arrowsStyle = setDatas['arrowsStyle']

with open('./projectSettings.json','r') as f:
    currentSong = json.load(f)['currentSong']


debugMode = False

