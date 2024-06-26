import subprocess
import os
import time

RTSP_BASE_URL = "103.150.190.86:4001"
CHANNELS = [
    {"id": "1adc157f-3054-4a03-b1da-3a8c69a25e1f", "name": "Camera 142"},
    {"id": "cbe0a11c-c41d-449d-97e1-fe4221ac642f", "name": "Camera 101"},
    {"id": "170de892-4abf-47d8-af9f-0659a31ae5e8", "name": "Camera 104"},
    {"id": "db9fec4f-d847-4e40-85bf-bd1cb738865d", "name": "Camera 105"},
    {"id": "628066c5-0593-48ab-a4f0-fe7f9b4474a1", "name": "Camera 106"},
    {"id": "1b1bb05a-c002-4fd3-9355-0a25ad058345", "name": "Camera 107"},
    {"id": "8aa8c5d3-d428-4150-9567-35fb60e89609", "name": "Camera 109"},
    {"id": "5f5680b4-2db1-4ef7-a57e-29215d7174a6", "name": "Camera 112"},
    {"id": "7bd1934c-3d05-498f-a90b-68a56e405a21", "name": "Camera 103"},
    {"id": "b446feae-1f16-42fc-a430-0146cca2dac3", "name": "Camera 102"},
    {"id": "6aba75ea-0e3b-486b-847c-6f67a3da80c9", "name": "Camera 114"},
    {"id": "699ed228-0987-498a-8351-be68c90b2842", "name": "Camera 115"},
    {"id": "7d2c0291-0cd1-4a96-8fb8-4d570d974079", "name": "Camera 116"},
    {"id": "d1863e5c-0c86-4dc5-aa0f-82fb19fc3ac3", "name": "Camera 117"},
    {"id": "b298cb47-7078-47c4-b326-2fc0513683c9", "name": "Camera 118"},
    {"id": "aa87dd52-b30e-486f-b84b-1c8aac1ba917", "name": "Camera 120"},
    {"id": "d4cdfcff-dc6f-4b4c-bfa8-da15ce16e6ef", "name": "Camera 126"},
    {"id": "e75b8270-bd0d-4491-a050-ad2caa8e43f9", "name": "Camera 123"},
    {"id": "fa50e378-5cc2-4f6d-bdeb-24da0e01c536", "name": "Camera 113"},
    {"id": "dcd684a9-8fbe-47d1-baf7-de93f0264971", "name": "Camera 144"},
    {"id": "91d006fd-005d-45cd-a618-57536c72198b", "name": "Camera 143"},
    {"id": "e7a1226d-875f-4ff4-9342-b9491ff9f6d5", "name": "Camera 141"},
    {"id": "bf93631f-5459-4c43-9c22-5039643dcafb", "name": "Camera 11"},
    {"id": "eaad8f31-9369-4fef-9868-7f6dfd657498", "name": "Camera 12"},
    {"id": "ae2a57dd-7faf-430d-8ff6-d6272b16cf4d", "name": "Camera 13"},
    {"id": "7fb39283-3659-43b4-b582-628ecc7e0da5", "name": "Camera 14"},
    {"id": "d3458ce5-b84a-4b5b-8502-aedecfced82f", "name": "Camera 15"},
    {"id": "7edb65a7-89ec-42a5-b273-f52df7befdc5", "name": "Camera 16"},
    {"id": "e9192eb9-da4e-4ae1-95e5-19298166a346", "name": "Camera 17"},
    {"id": "e1794711-41bb-4e30-ae04-24e21a3c566d", "name": "Camera 18"},
    {"id": "46cb5528-2bde-4912-8938-2a755881b11e", "name": "Camera 19"},
    {"id": "151c38cf-c49b-4374-b5a5-027c4aa9a0d4", "name": "Camera 20"},
    {"id": "fc7492af-0e52-4f55-b476-9ce1ada5f0d4", "name": "Camera 21"},
    {"id": "2f7a47d5-964a-4789-a8d8-642d100ac2cc", "name": "Camera 22"},
    {"id": "458c33dc-c041-4b10-8811-49688293bb74", "name": "Camera 23"},
    {"id": "ad6832d7-f15f-4694-827c-d5a14245e8fa", "name": "Camera 24"},
    {"id": "5bb8c9fa-17f3-477c-9350-a43494f4742e", "name": "Camera 25 - POS 10"},
    {"id": "bab5459e-5844-42e4-9e6f-4547465e1122", "name": "Camera 26 - POS 30"},
    {"id": "fd1ed985-b4cb-4ab7-9cf3-2e5ef41aa9ce", "name": "Camera 27"},
    {"id": "9dfd58fc-30c3-4915-838b-f1e543c83ce8", "name": "Camera 28"},
    {"id": "1884745d-c100-4869-a8e1-78be3a19c0bf", "name": "Camera 29"},
    {"id": "42cfc7cb-b59f-47bb-86d8-9ecdc4cdfc99", "name": "Camera 30"},
    {"id": "3f66636c-0370-4507-8f0a-8e572de2100e", "name": "Camera 31"},
    {"id": "22248956-99aa-4ad9-b88b-b410e4d54c13", "name": "Camera 32 - POS 20"},
    {"id": "e726acdf-6194-4471-88f7-159790713a23", "name": "Camera 33 - POS 10"},
    {"id": "a9eb0f08-12bd-47ab-b009-1dc7cf71af83", "name": "Camera 34"},
    {"id": "b24c5382-df7d-42a0-b117-56a3c7ea253e", "name": "Camera 35"},
    {"id": "7282a72b-4128-438b-a2cf-4df323e92d25", "name": "Camera 36"},
    {"id": "dab37d61-c7d2-43c8-921e-1fa70078e8ae", "name": "Camera 37"},
]


def start_hls_conversion(rtsp_url, output_dir, channel_name):
    hls_filename = f"{channel_name}.m3u8"
    hls_output_path = os.path.join(output_dir, hls_filename)
    ffmpeg_cmd = [
        "ffmpeg",
        "-i",
        rtsp_url,
        "-c:v",
        "copy",
        "-c:a",
        "copy",
        "-hls_time",
        "4",
        "-hls_list_size",
        "10",
        "-hls_flags",
        "delete_segments",
        hls_output_path,
    ]
    process = subprocess.Popen(
        ffmpeg_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=os.environ.copy(),
    )
    return process, hls_output_path


def stop_hls_conversion(process):
    process.terminate()
    try:
        process.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()


if __name__ == "__main__":
    output_dir = "output"
    processes = []

    for channel in CHANNELS:
        channel_id = channel["id"]
        channel_name = channel["name"]
        rtsp_url = f"rtsp://root:@{RTSP_BASE_URL}/rtsp?channelid={channel_id}"
        print(f"Starting HLS conversion for {channel_name}...")
        process, hls_output_path = start_hls_conversion(
            rtsp_url, output_dir, channel_id
        )
        if process:
            processes.append(process)
            print(
                f"HLS conversion started for {channel_name}. Output file: {hls_output_path}"
            )
        else:
            print(f"Failed to start HLS conversion for {channel_name}")

    try:
        # Keep the script running
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        # Clean up all subprocesses on termination
        for process in processes:
            stop_hls_conversion(process)
