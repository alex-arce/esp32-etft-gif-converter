# eTFT GIF Converter

GIF to header (.h) generator for the ESP32 eTFT screens. [WIP]

## Pre-requisites

Resize the gif or video and crop it with any tool for example with:


### ImageMagic:

```bash
convert walk.gif -resize 25% walk-resized.gif
```

### ffmpeg:

For example for a TFT display of 240x135 size:
```bash
ffmpeg -i video.mp4 -r 4 -vf scale=240:-1 video.gif
```

## Usage

```bash
./eTFT-gif-converter.py -i <RESIZED_AND_CROPPED_ANIM.gif> -o <HEADER_NAME>.h
```

### Complete Example

```bash
git clone https://github.com/alex-arce/esp32-etft-gif-converter.git
cd esp32-etft-gif-converter.git
cp example/starcraft.gif .
./eTFT-gif-converter.py -i starcraft.gif -o animation.h
```

### Adding it to Arduino / PlatformIO / C++ 

You could be use the **animation.h** header generated like this:

```C++

#include "animation.h"

void loop() {
    if(shutdown++ > 5) espDeepSleep();
    for (int i = 0; i < frames; i++) {
        tft.pushImage(
          2,                   // x position
          0,                   // y position
          animation_width, 
          animation_height, 
          animation[i]
        );
        delay(120);
    }
}
```

Full implementation example [here](https://github.com/hpsaturn/esp32-etft-gif-animation-test)

<a href="https://github.com/hpsaturn/esp32-etft-gif-animation-test" target="_blank"><img src="https://raw.githubusercontent.com/hpsaturn/esp32-etft-gif-animation-test/master/images/ttgo-tdisplay-demo.gif"></a>

### Thanks
Thanks a lot to [Antonio Vanegas - hpsaturn](https://github.com/hpsaturn) for his tests and his help :-D
