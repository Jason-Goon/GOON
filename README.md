# GOON Discord Bot

GOON is a Discord bot that can join voice channels, play audio from YouTube, and record audio. The bot is currently tested on Linux platforms only.

## Features

- Join and leave voice channels
- Play audio from YouTube links
- Record audio from voice channels

## System Dependencies

Before you can run the bot, make sure you have the following dependencies installed:

- Python 3.12 or higher
- FFmpeg
- yt-dlp (YouTube-DL fork)

## Installation Guide

### Arch Linux

1. **Update your system:**

    ```sh
    sudo pacman -Syu
    ```

2. **Install Python and pip:**

    ```sh
    sudo pacman -S python python-pip
    ```

3. **Install FFmpeg:**

    ```sh
    sudo pacman -S ffmpeg
    ```

4. **Install yt-dlp:**

    ```sh
    sudo pacman -S yt-dlp
    ```

5. **Clone the repository and install Python dependencies:**

    ```sh
    git clone https://github.com/yourusername/goon.git
    cd goon
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

### Gentoo

1. **Update your system:**

    ```sh
    sudo emerge --sync
    sudo emerge --update --deep --with-bdeps=y @world
    ```

2. **Install Python and pip:**

    ```sh
    sudo emerge dev-lang/python
    sudo emerge dev-python/pip
    ```

3. **Install FFmpeg:**

    ```sh
    sudo emerge media-video/ffmpeg
    ```

4. **Install yt-dlp:**

    ```sh
    sudo emerge net-misc/yt-dlp
    ```

5. **Clone the repository and install Python dependencies:**

    ```sh
    git clone https://github.com/yourusername/goon.git
    cd goon
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Usage
1. **Replace TOKEN in bot.run('TOKEN'):**
   get a token from the discord developer dashboard and replace TOKEN in the last line with your token 
    
3. **Activate the virtual environment:**

    ```sh
    source venv/bin/activate
    ```

4. **Run the bot:**

    ```sh
    python gooner.py
    ```

## OpenBSD License

This project is licensed under the Zero-Clause BSD License - see the LICENSE file for details.

