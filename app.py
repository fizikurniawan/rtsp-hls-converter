import time
from ffmpeg_worker import start_ffmpeg

if __name__ == "__main__":
    start_ffmpeg()

    while True:
        time.sleep(60)