from PIL import Image
from sys import stdout, argv
from os import listdir, getcwd
import time, subprocess, threading

def imageToAscii(image_path):
    # Open the image file
    image = Image.open(image_path)
    
    # Resize the image to fit the terminal window
    new_width = 80
    aspect_ratio = float(image.height) / float(image.width)
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
    
    return string


def showFrame(text):
    stdout.write('\033[3J')
    stdout.write('\033[H')
    stdout.write(text)

def video():
    frames_path = getcwd() + '/video/img/'
    frames = listdir(frames_path)
    fps = int(argv[1])

    start_time = time.time()
    frame = 0
    for num in range(len(frames)):
        frame += 1
        ascii = imageToAscii(frames_path + 'frame_%d.jpg' % (frame))
        showFrame(ascii)
        time.sleep(1/fps - abs(time.time() - start_time))
        start_time = time.time()



def audio():
    audio_path = getcwd() + '/video/audio/'
    subprocess.run(["play", audio_path + listdir(audio_path)[0]], capture_output=True)

playVideo = threading.Thread(target=video)
playAudio = threading.Thread(target=audio)
playVideo.start()
playAudio.start()



