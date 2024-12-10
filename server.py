from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

# 전역 이미지 변수
img = np.ones((600, 800, 3), dtype=np.uint8) * 255  # 흰 배경
pen_color = (0, 0, 0)  # 검은색
pen_width = 5

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/draw', methods=['POST'])
def draw():
    global img, pen_color, pen_width
    data = request.json
    x1, y1 = data['x1'], data['y1']
    x2, y2 = data['x2'], data['y2']
    
    # 선 그리기
    cv2.line(img, (x1, y1), (x2, y2), pen_color, pen_width)
    return jsonify({"message": "Line drawn"})

@app.route('/save', methods=['POST'])
def save():
    global img
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.png')
    cv2.imwrite(save_path, img)
    return jsonify({"message": "Image saved", "path": save_path})

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='0.0.0.0', port=5000, debug=True)
