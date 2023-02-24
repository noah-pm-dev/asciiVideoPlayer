import os, shutil, subprocess
from sys import argv
from PIL import Image

def imageToAscii(image_path):
    '''Converts an image to ascii'''
    # Open the image file
    image = Image.open(image_path)
    
    # Resize the image to fit the terminal window
    new_width = 80
    aspect_ratio = image.height / image.width
    new_height = int(aspect_ratio * new_width)
    image = image.resize((new_width, new_height))

    # Create a list of ASCII characters to represent the image, going from least to most light
    ascii_characters = " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    step = 255.0 / len(ascii_characters)

    # Convert the image to ASCII art
    ascii_image = []
    for y in range(image.height):
        row = ""
        for x in range(image.width):
            r, g, b = image.getpixel((x, y))
            gray = int(0.2989 * r + 0.5870 * g + 0.1140 * b)
            index = int(gray / step)
            row += ascii_characters[index] * 2
        ascii_image.append(row)

    # Assemble string from rows
    string = '\n'.join(ascii_image)
    
    return string + '\n'

def splice(video):
    '''Splits video into audio and frames'''
    if 'tmp' in os.listdir():
        shutil.rmtree('tmp')
    os.makedirs('tmp/audio')
    os.makedirs('tmp/frames')

    subprocess.run(['ffmpeg', '-i', video, '-vn', '-c:a', 'libvorbis', '-q:a', '5', 'tmp/audio/tmp_output.ogg']) # Splice out audio
    subprocess.run(['ffmpeg', '-i', video, '-q:v', '1', 'tmp/frames/tmp_frame_%d.jpg']) # Splice out frames

def header(frame, fps):
    '''Append the frame height and fps of video to start of ascv file'''

    ascii_frame_height = frame.count('\n')

    header = 'fc' + str(len(os.listdir('tmp/frames/'))) + 'fh' + str(ascii_frame_height) + 'fps' + str(fps)

    putText(header)
    

def putText(text):
    with open('output.ascv', 'a') as ascv:
        ascv.write(text)

def writeAudio(audio):
    with open('output.ascv', 'ab') as ascv:
        with open(audio, 'rb') as a:
            audio_bytes = a.read()
        
        ascv.write(bytes('ae', 'utf-8') + audio_bytes + bytes('eae', 'utf-8'))



splice(argv[1])

for frame_num in range(1, len(os.listdir('tmp/frames/'))):
    ascii = imageToAscii(('tmp/frames/tmp_frame_%d.jpg' % (frame_num + 1)))

    if frame_num == 1:
        header(ascii, argv[2])
    
    putText(ascii)

writeAudio('tmp/audio/tmp_output.ogg')






