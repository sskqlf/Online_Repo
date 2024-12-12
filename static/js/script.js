const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d');

let isDrawing = false;
let isFillMode = false;
let isTextMode = false;
let startX, startY;

const penColorPicker = document.getElementById('penColor');
const penWidthInput = document.getElementById('penWidth');
const imageUpload = document.getElementById('imageUpload');

// 선 그리기
canvas.addEventListener('mousedown', (e) => {
    if (isFillMode || isTextMode) return;
    isDrawing = true;
    startX = e.offsetX;
    startY = e.offsetY;
});

canvas.addEventListener('mousemove', (e) => {
    if (!isDrawing || isFillMode || isTextMode) return;
    const x = e.offsetX;
    const y = e.offsetY;
    ctx.strokeStyle = penColorPicker.value;
    ctx.lineWidth = penWidthInput.value;
    ctx.beginPath();
    ctx.moveTo(startX, startY);
    ctx.lineTo(x, y);
    ctx.stroke();
    ctx.closePath();
    startX = x;
    startY = y;
});

canvas.addEventListener('mouseup', () => {
    isDrawing = false;
});

// 이미지 업로드
imageUpload.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
        const img = new Image();
        img.onload = () => {
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        };
        img.src = reader.result;
    };
    reader.readAsDataURL(file);
});

// 캔버스 초기화
function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

// 저장
function saveCanvas() {
    const link = document.createElement('a');
    link.download = 'drawing.png';
    link.href = canvas.toDataURL();
    link.click();
}
