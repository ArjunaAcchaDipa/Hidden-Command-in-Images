# Hidden Command in Images

Hidden Command in Images is using **LSB (Least Significant Bytes)** type of **Steganography** to hide the command inside the image (encode) and **automatically** run the command from the image (decode).

This repository was made to fulfill the assignment of **Programming of Penetration Testing**.

## Table of Contents
* [Prerequisite and Technology](#prerequisite-and-technology)
* [Installation](#installation)
* [References](#references)

## Prerequisite and Technology
- Python 3 libraries
    - base64
    - png
    - decouple
    - selenium
    - imgurpython
    - os
    - subprocess
- Imgur API

## Installation

From your command line, clone and run **Hidden-Command-in-Images**:
```bash
$ git clone https://github.com/ArjunaAcchaDipa/Hidden-Command-in-Images.git

# Change directory using your terminal or cmd.
$ cd Hidden-Command-in-Images/

# Copy the example env file and make the required configuration changes in the .env file.
$ cp .env.example .env

# Make Imgur account and request API
# Set up the needed API in .env

# Run the program using python3.
$ python3 steganography.py
```

## References
- [https://docs.replit.com/tutorials/13-steganography](https://docs.replit.com/tutorials/13-steganography)
- [https://github.com/vprusso/youtube_tutorials/blob/master/imgur_python](https://github.com/vprusso/youtube_tutorials/blob/master/imgur_python)