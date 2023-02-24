from sys import stdout, argv
from sys import stdout, argv
from os import listdir, getcwd
import time, subprocess, threading, re

def showFrame(text):
    stdout.write('\033[3J')
    stdout.write('\033[H')
    stdout.write(text)

def video(ascv):
    with open(ascv, 'rb') as av:
        frame_count = re.search(r'(?<=fc)\d+', av.read())
        frame_height = re.search(r'(?<=fh)\d+', av.read())
        print(frame_count, ';', frame_height)

        frames = []
        line = None
        for line_num, line in enumerate(av):
            if line_num == 0:
                continue
            elif bytes('ae', 'utf-8') in line:
                break
            else:
                frames.append(line)
    
    for f in range(0, frame_count, frame_height):
        frame = ''
        for l in range(frame_height):
            frame += frames[l]
            frames.pop(l)
        
        showFrame(frame)




#def audio(ascv):


ascv = argv[1]

playVideo = threading.Thread(target=video(ascv))
#playAudio = threading.Thread(target=audio(ascv))
playVideo.start()
#playAudio.start()



