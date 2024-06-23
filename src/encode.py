import os, shutil, subprocess
from sys import argv, stdout
from PIL import Image

PROGRESS_BAR = "[..................................................]"

def image_to_ascii(image_path):
    '''Converts an image to ascii'''
    # Open the image file
    image = Image.open(image_path)
    
    # Resize the image to fit the terminal window
    vw, vh = [os.get_terminal_size().columns, os.get_terminal_size().lines]
    v_aspect_ratio = vw/vh
    image_aspect_ratio = image.width/image.height
    if image_aspect_ratio > v_aspect_ratio:
        scaling_factor = vw/image.width
    elif image_aspect_ratio <= v_aspect_ratio:
        scaling_factor = vh/image.height
    
    new_width = int(image.width * scaling_factor)
    new_height = int(image.height * scaling_factor)
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
    
    return string + '\nf#e!'

def splice(video):
    '''Splits video into audio and frames'''
    if 'tmp' in os.listdir():
        shutil.rmtree('tmp')
    os.makedirs('tmp/audio')
    os.makedirs('tmp/frames')
    subprocess.run(['ffmpeg', '-i', video, '-vn', '-c:a', 'libvorbis', '-q:a', '5', 'tmp/audio/tmp_output.ogg']) # Splice out audio
    subprocess.run(['ffmpeg', '-i', video, '-q:v', '1', 'tmp/frames/tmp_frame_%d.jpg']) # Splice out frames

def header(fps, video):
    '''Append the frame height and fps of video to start of ascv file'''

    duration = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video]).decode('utf-8'))
    header = str(fps) + '%!%' + str(duration) + '\n'

    put_text(header)
    

def put_text(text):
    ascv.write(bytes(text, 'utf-8'))

def write_audio(audio):
    with open(audio, 'rb') as a:
        audio_bytes = a.read()
    
    ascv.write(bytes('v#e!', 'utf-8') + audio_bytes)

def update_progress(count):
    stdout.write('\r')
    stdout.write(PROGRESS_BAR.replace('.', '=', count))
    stdout.flush()

name = argv[1].split('.', 1)[0]

splice(argv[1])

frames = len(os.listdir('tmp/frames/'))
progress_fraction = round(frames/50)

stdout.write('\n' + 'WRITING FRAMES' + '\n' + PROGRESS_BAR)
stdout.flush()

count = 0
with open(name + '.ascv', 'wb') as ascv:
    for frame_num in range(1, frames):
        ascii = image_to_ascii(('tmp/frames/tmp_frame_%d.jpg' % (frame_num)))

        if frame_num == 1:
            header(argv[2], argv[1])
        
        put_text(ascii)

        if (frame_num) % progress_fraction == 0:
            count += 1
            update_progress(count)

    write_audio('tmp/audio/tmp_output.ogg')

shutil.rmtree('tmp')

print()
