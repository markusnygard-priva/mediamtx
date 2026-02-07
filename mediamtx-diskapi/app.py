from flask import Flask, jsonify
import shutil
import os
import re
import glob
import time
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/disk-space', methods=['GET'])
def disk_space():
    # Path to the recordings directory
    path = '/recordings'
    total, used, free = shutil.disk_usage(path)
    return jsonify({
        'total': total,
        'used': used,
        'free': free
    })

@app.route('/recording-files/<stream_name>', methods=['GET'])
def list_recording_files(stream_name):
    # Adjust this path if your recordings are elsewhere
    base_path = '/recordings'
    stream_path = os.path.join(base_path, stream_name)
    if not os.path.exists(stream_path):
        return jsonify([])

    # Find .fmp4 and .mp4 files
    files = glob.glob(os.path.join(stream_path, '*.fmp4')) + glob.glob(os.path.join(stream_path, '*.mp4'))
    result = []
    now = time.time()
    for file_path in files:
        stat = os.stat(file_path)
        # Exclude files modified in the last 30 seconds (likely still recording)
        if now - stat.st_mtime < 30:
            continue
        result.append({
            'name': os.path.basename(file_path),
            'size': stat.st_size,
            'modified': time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(stat.st_mtime))
        })
    return jsonify(result)

@app.route('/recording-files-metadata/<stream_name>', methods=['GET'])
def list_recording_files_metadata(stream_name):
    base_path = '/recordings'  # Adjust if your recordings are elsewhere
    stream_path = os.path.join(base_path, stream_name)
    if not os.path.exists(stream_path):
        return jsonify([])

    files = glob.glob(os.path.join(stream_path, '*.fmp4')) + glob.glob(os.path.join(stream_path, '*.mp4'))
    result = []
    now = time.time()
    filename_regex = re.compile(r'(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})-(\d+)')
    for file_path in files:
        stat = os.stat(file_path)
        if now - stat.st_mtime < 30:
            continue
        fname = os.path.basename(file_path)
        match = filename_regex.search(fname)
        start_time = None
        if match:
            year, month, day, hour, minute, second, ms = map(int, match.groups())
            start_time = datetime(year, month, day, hour, minute, second, ms // 1000).isoformat()
        result.append({
            'name': fname,
            'size': stat.st_size,
            'modified': time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(stat.st_mtime)),
            'start_time': start_time
        })
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
