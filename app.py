from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from config import PORT, OUTPUT_DIR
from ffmpeg_utils import start_ffmpeg


if __name__ == "__main__":
    app = Flask(__name__)
    CORS(app, origins="*")

    start_ffmpeg()

    @app.route("/<path:path>")
    def serve_hls(path):
        return send_from_directory(OUTPUT_DIR, path)

    @app.route(
        "/",
    )
    def login():
        return jsonify({"success": "ok"})

    app.run(port=PORT, host="0.0.0.0")
