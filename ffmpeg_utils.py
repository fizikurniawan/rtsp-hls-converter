import subprocess
import os
from config import OUTPUT_DIR, CHANNELS, RTSP_BASE_URL
from flask import send_from_directory
from flask_cors import cross_origin


def start_ffmpeg():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for channel in CHANNELS:
        channel_id = channel["id"]
        print("processing: ", channel_id)
        url = RTSP_BASE_URL + channel_id
        ffmpeg_cmd = [
            "ffmpeg",
            "-i",
            url,
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-strict",
            "-2",
            "-hls_time",
            "10",
            "-hls_list_size",
            "6",
            "-hls_flags",
            "delete_segments",
            "-f",
            "hls",
            os.path.join(OUTPUT_DIR, f"{channel_id}.m3u8"),
        ]
        subprocess.Popen(ffmpeg_cmd)
