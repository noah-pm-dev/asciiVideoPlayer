from sys import stdout, argv
from time import sleep, time
from threading import Thread
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO

def test_print_time(frame):
    start = time()
    show_frame(frame)
    return time() - start

def show_frame(text):
    stdout.write('\033[H')
    stdout.write(text)

def v(frames, fps, print_time):  
    for frame in frames:
        show_frame(frame)
        sleep((1/fps) - print_time)

def a(audio):
    play(audio)

def video_init(data):
    header, frames = data.decode().split('\n', 1)
    return [frame for frame in frames.split('f#e!')], int(header.split('fps', 1)[1].rstrip())

def audio_init(audio):
    return AudioSegment.from_file(BytesIO(audio), format="ogg").set_sample_width(2)


    

ascv = argv[1]

with open(ascv, 'rb') as av:
    b = av.read()
    video, audio = [i for i in b.split(bytes('v#e!', 'utf-8'))]

frames, fps = video_init(video)
audio_segment = audio_init(audio)

print_time = test_print_time(frames[0])

playVideo = Thread(target=v, args=(frames, fps, print_time))
playAudio = Thread(target=a, args=(audio_segment, ))
playVideo.start()
playAudio.start()



