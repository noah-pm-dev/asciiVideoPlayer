# Ascii Video Player
This python program allows any video to be played as ascii in the terminal. This program supports any platform where you can install the necessary tools, but has only been tested on linux.

## Installation
Clone repository, then run `pip install -r requirements.txt`\
You will also need `portaudio`, installed with `apt-get install portaudio19-dev` on Debian/Ubuntu, and `ffmpeg`

## Usage
Run the encoding script on any video file, and specify the fps:
```
python3 src/encode.py path/to/video.mkv 30
```

If you do not know the fps, you can find it by running `ffmpeg -i video.mkv`, and looking for this line:
```
 Stream #0:0(eng): Video: vp9 (Profile 0), yuv420p(tv), 960x720, SAR 1:1 DAR 4:3, 30 fps, 30 tbr, 1k tbn, 1k tbc (default)
```
here you can find the `30 fps` listed between `DAR 4:3` and `30 tbr`.

The encoder will output a `.ascv` file. Play this file with:
```
python3 src/play.py video.ascv
```
The `.ascv` file contains both video and audio.


#### A sample `.ascv` of the "Bad Apple" music video is included in the repository.