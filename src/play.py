from sys import stdout, argv
from time import sleep, time
from threading import Thread
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO
from re import sub

def decompress(frame):
    '''Finds any occurence of one or more integers followed by a character, and substitutes for that many characters,
    e.g. 4k becomes kkkk'''
    return sub(r'(\d+)(.)', lambda match: match.group(2) * int(match.group(1)), frame)

def show_frame(text):
    '''Clears screen and displays frame'''

    stdout.write('\033[2J\033[H') # Clear the screen and reset cursor to home 
    stdout.write(text) # Print frame

def v(frames, fps):
    '''Display each frame, delays each frame by 1/fps.
    Because the video gets off sync, it is re-synced after a certain number of frames according to the fps, usually every 30 frames.
    At 30 fps, 1 second SHOULD have elapsed after 30 frames, however it will be off, so subtracting 1 from the true elapsed time
    produces either a positive or negative desync value. If the video is going too slow, the desync value will be positive. Adding a positive value to
    correctedfps makes the fractional second passed to sleep() smaller, making the video run faster. If the video is going too fast, the opposite will happen'''

    correctedfps = fps
    start = time()
    for num, frame in enumerate(frames):
        show_frame(frame)
        if (num + 1) % fps == 0: # Run this block every # of frames according to fps, usually every 30 frames
            desync = (time() - start) - 1 # Find current desync
            correctedfps += desync # Adjust fps by desync
            start = time()
        sleep(1/correctedfps)
    
    # Clear the screen and reset cursor to home after video is done
    stdout.write('\033[2J\033[H')

def video_init(data):
    '''Separates the header and video data, returns a list of frames split at the frame end indicator, along with the integer fps value'''

    header, frames = data.decode().split('\n', 1)
    return [decompress(frame) for frame in frames.split('f#e!')], int(header.split('fps', 1)[1])

def a(audio):
    '''Playes given audio using pydub.playback'''

    play(audio)



    

ascv = argv[1] # ascv file to play

# Read bytes of ascv file (necessary because the audio is in bytes)
with open(ascv, 'rb') as av:
    b = av.read()
    video, audio = [i for i in b.split(bytes('v#e!', 'utf-8'))] # Split video and audio at video end indicator

frames, fps = video_init(video)

# Create AudioSegment from audio bytes
audio_segment = AudioSegment.from_file(BytesIO(audio), format="ogg").set_sample_width(2) 

# Run video and audio on separate threads so they can run simultaneously
playVideo = Thread(target=v, args=(frames, fps))
playAudio = Thread(target=a, args=(audio_segment, ))
playVideo.start()
playAudio.start()

