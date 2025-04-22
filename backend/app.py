from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from cartoonizer import cartoonize_video
import os

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads/'
RESULT_FOLDER = 'results/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['video']
    filename = file.filename
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    result_path = cartoonize_video(path, filename)
    return jsonify({"video_url": f"/result/{filename}"})

@app.route('/result/<filename>')
def result(filename):
    return send_file(os.path.join(RESULT_FOLDER, filename), as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render provides the PORT environment variable
    app.run(host="0.0.0.0", port=port)
