# importing integrated modules
import os
import re
from datetime import datetime, timedelta
from pandas import *
from gtts import gTTS
from moviepy.editor import  AudioFileClip,vfx

import pandas as pd
import numpy as np
# initializing subtitle list length in seconds


# intializing .txt file locared in the same folder as this python script
inputtxt = 'temp_files/output.txt'
subpath = os.path.join(os.path.dirname(__file__), inputtxt)
subtxt = open(subpath).read()

# splitting paragraphs into list items with regex
par = re.split('\n{2,}', subtxt)

# pulling number of paragraphs in a text doc
npar = len(par)

# creating a list of timedeltas
tdlist = []

# initializing starting subtitle and subtitile duration
temp_audio = gTTS(text=par[0], lang='en', slow=False).save("temp_files/temp.mp3")
tdstart = timedelta(hours=0, seconds= 0)
tdlist.append(tdstart)


for i in range(1,npar):
    
    temp_audio = gTTS(text=par[i], lang='en', slow=False).save("temp_files/temp.mp3")
  
    tdstart = tdstart + timedelta(seconds= round(AudioFileClip("temp_files/temp.mp3").fx(vfx.speedx,1.2).duration))
    tdlist.append(tdstart)

temp_audio = gTTS(text=par[npar-1], lang='en', slow=False).save("temp_files/temp.mp3")
tdstart = tdstart + timedelta(seconds= round(AudioFileClip("temp_files/temp.mp3").fx(vfx.speedx,1.2).duration))
tdlist.append(tdstart)


# combining created list into a string in accordance with .srt formatting
lcomb = []
for i in range(npar):
   
        lcomb.append(str(i+1) + '\n' + str(tdlist[i]) + ',000 --> ' + str(
        tdlist[i+1]) + ',000' + '\n' + par[i] + '\n')

# converting the list into a string with the delimiter '\n'
srtstring = '\n'.join(lcomb)

# adding '0' to single digit hours
pat = r'^(\d:)'
repl = '0\\1'
srtstring2 = re.sub(pat, repl, srtstring, 0, re.MULTILINE)

# writing the string to a new file
srtout = os.path.join(os.path.dirname(__file__), 'temp_files/subtitles.srt')
with open(srtout, 'w') as newfile:
    newfile.write(srtstring2)
