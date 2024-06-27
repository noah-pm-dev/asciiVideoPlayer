import os, shutil, subprocess
from sys import argv, stdout
from PIL import Image
from re import sub

PROGRESS_BAR = "[..................................................]"

def compress(string):
    '''Finds any character followed by at least 2 more of the same character,
    then substitutes it for {count}{char}, e.g. ##### becomes 5#'''
    return sub(r'(.)\1{2,}', lambda match: f'{len(match.group(0))}{match.group(0)[0]}', string)

def image_to_ascii(image_path):
    '''Converts an image to ascii'''
    # Open the image file
    image = Image.open(image_path)
    
    # Resize the image to fit the terminal window
    vw, vh = [os.get_terminal_size().columns/2, os.get_terminal_size().lines] # Get width (vw) and height (vh) of terminal
    v_aspect_ratio = vw/vh # Terminal aspect ratio
    image_aspect_ratio = image.width/image.height # Image aspect ratio
    # If the image's aspect ratio is larger than the terminal, then image.width > vw, 
    # so scale the width
    if image_aspect_ratio > v_aspect_ratio: 
        scaling_factor = vw/image.width
    
    # Otherwise, scale the height
    elif image_aspect_ratio <= v_aspect_ratio:
        scaling_factor = vh/image.height
    
    new_width = int(image.width * scaling_factor)
    new_height = int(image.height * scaling_factor)
    # print('vw:', vw, ';vh:', vh, ';imgwidth:', image.width, ';imgheight:', image.height)
    # print('newW:', new_width, 'newH:', new_height)
    # exit(0)
    image = image.resize((new_width, new_height))

    # Create a list of ASCII characters to represent the image, going from least to most light
    # The list excludes integers to not mess up compression
    ascii_characters = " .'`^\",:;Il!i><~+_-?][}{)(|\/tfjrxnuvczXYUJCLQOZmwqpdbkhao*#MW&%B@$"

    step = 255.0 / len(ascii_characters) # The step is the slice of the grayscale spectrum each ascii character represents

    # Convert the image to ASCII
    ascii_image = []
    for y in range(image.height): # Iterate through rows
        row = ""
        for x in range(image.width): # Iterate through pixels in row
            r, g, b = image.getpixel((x, y)) # Get rgb value of pixel as three separate variables
            gray = int(0.2989 * r + 0.5870 * g + 0.1140 * b) # Formula for converting to grayscale
            index = int(gray / step) # Choose ascii character
            row += ascii_characters[index] * 2 # Add two copies of chosen character to row, so each pixel = two characters
        ascii_image.append(row)

    # Assemble string from rows
    string = '\n'.join(ascii_image)
    
    # Return compressed frame with frame end indicator
    return compress(string) + '\nf#e!'

def splice(video):
    '''Splits video into audio and frames'''
    if 'tmp' in os.listdir():
        shutil.rmtree('tmp')
    os.makedirs('tmp/audio')
    os.makedirs('tmp/frames')
    subprocess.run(['ffmpeg', '-i', video, '-vn', '-c:a', 'libvorbis', '-q:a', '5', 'tmp/audio/tmp_output.ogg']) # Splice out audio
    subprocess.run(['ffmpeg', '-i', video, '-q:v', '1', 'tmp/frames/tmp_frame_%d.jpg']) # Splice out frames

def header(fps):
    '''Append the fps to start of ascv file'''

    header = 'fps' + str(fps) + '\n'

    put_text(header)
    

def put_text(text):
    '''Write given text as bytes to ascv'''

    ascv.write(bytes(text, 'utf-8'))

def write_audio(audio):
    '''Read bytes of given audio and write to ascv, preceded by video end indicator'''

    with open(audio, 'rb') as a:
        audio_bytes = a.read()
    
    ascv.write(bytes('v#e!', 'utf-8') + audio_bytes)

def update_progress(count):
    '''Update progress bar with number of cells filled equal to count'''

    stdout.write('\r')
    stdout.write(PROGRESS_BAR.replace('.', '=', count))
    stdout.flush()

# color = False

# for arg in argv:
#     if '.' in arg:
#         name = arg.split('.', 1)[0]
#     elif arg == '-c':
#         color = True
#         print("color")
#         exit(0)
#     elif isinstance(int(arg), int):
#         fps = arg

name = argv[1].split('.', 1)[0] # Get name of video file



splice(argv[1])

frames = len(os.listdir('tmp/frames/')) # Number of frames
progress_fraction = round(frames/50) # Number of frames per cell of progress bar

stdout.write('\n' + 'WRITING FRAMES' + '\n' + PROGRESS_BAR)
stdout.flush()

count = 0
with open(name + '.ascv', 'wb') as ascv:
    for frame_num in range(1, frames):
        ascii = image_to_ascii(('tmp/frames/tmp_frame_%d.jpg' % (frame_num)))

        if frame_num == 1:
            header(argv[2])
        
        put_text(ascii)

        # If correct number of frames have been written, add one cell to progress bar
        if (frame_num) % progress_fraction == 0:
            count += 1
            update_progress(count)

    write_audio('tmp/audio/tmp_output.ogg')

shutil.rmtree('tmp')

print()
