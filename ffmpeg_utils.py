import subprocess
import os
from config import OUTPUT_DIR, CHANNELS, RTSP_BASE_URL


def start_ffmpeg():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for channel in CHANNELS:
        channel_id = channel["id"]
        title = channel["name"]
        print("processing: ", channel_id)
        url = RTSP_BASE_URL + channel_id

        ffmpeg_cmd = [
            "ffmpeg",
            "-y",
            "-fflags",
            "nobuffer",
            "-rtsp_transport",
            "tcp",
            "-i",
            url,
            "-f",
            "lavfi",
            "-i",
            "anullsrc=channel_layout=stereo:sample_rate=44100",
            "-vsync",
            "0",
            "-copyts",
            "-vcodec",
            "libx264",
            "-movflags",
            "frag_keyframe+empty_moov",
            "-an",
            "-metadata",
            f"title={title}",
            "-hls_flags",
            "delete_segments+append_list",
            "-f",
            "hls",
            "-segment_list_flags",
            "live",
            "-hls_time",
            "1",
            "-hls_list_size",
            "3",
            os.path.join(OUTPUT_DIR, f"{channel_id}.m3u8"),
        ]
        subprocess.Popen(ffmpeg_cmd)
