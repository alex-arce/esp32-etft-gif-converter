# eTFT GIF Converter

GIF to header (.h) generator for the ESP32 eTFT screens. [WIP]

## Pre-requisites

Resize the gif or video and crop it with any tool for example with:


### ImageMagic

```bash
convert walk.gif -resize 25% walk-resized.gif
```

### ffmpeg

For example for a TFT display of 240x135 size:
```bash
ffmpeg -i video.mp4 -r 4 -vf scale=240:-1 video.gif
```

## Usage

```bash
./eTFT-gif-converter.py -i <RESIZED_AND_CROPPED_ANIM.gif> -o <HEADER_NAME>.h
```

