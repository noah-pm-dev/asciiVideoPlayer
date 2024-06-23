from sys import stdout, argv
from time import sleep, time
from threading import Thread
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO
from re import sub

def decompress(frame):
    return sub(r'(\d+)(.)', lambda match: match.group(2) * int(match.group(1)), frame)

def test_print_time(frame):
    start = time()
    show_frame(frame)
    return time() - start

def show_frame(text):
    stdout.write('\033[2J')
    stdout.write('\033[H')
    stdout.write(text)

def v(frames, fps, print_time):
    correctedfps = fps
    start = time()
    for num, frame in enumerate(frames):
        if (num + 1) % fps == 0:
            desync = (time() - start) - 1
            correctedfps += desync
            start = time()
        show_frame(frame)
        sleep((1/correctedfps) - print_time)
    
    stdout.write('\033[2J\033[H')

def video_init(data):
    header, frames = data.decode().split('\n', 1)
    return [decompress(frame) for frame in frames.split('f#e!')], int(header.split('fps', 1)[1])

def a(audio):
    play(audio)



    

ascv = argv[1]

with open(ascv, 'rb') as av:
    b = av.read()
    video, audio = [i for i in b.split(bytes('v#e!', 'utf-8'))]

frames, fps = video_init(video)

audio_segment = AudioSegment.from_file(BytesIO(audio), format="ogg").set_sample_width(2)

print_time = test_print_time(frames[0])

playVideo = Thread(target=v, args=(frames, fps, print_time))
playAudio = Thread(target=a, args=(audio_segment, ))
playVideo.start()
playAudio.start()

