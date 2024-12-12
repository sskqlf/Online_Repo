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

// 채우기 기능
canvas.addEventListener('click', (e) => {
    if (!isFillMode) return;

    const fillColor = penColorPicker.value;
    const x = e.offsetX;
    const y = e.offsetY;

    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const targetColor = getPixelColor(imageData, x, y);
    const fillColorRGB = hexToRgb(fillColor);

    floodFill(imageData, x, y, targetColor, fillColorRGB);
    ctx.putImageData(imageData, 0, 0);
});

// 텍스트 삽입
canvas.addEventListener('click', (e) => {
    if (!isTextMode) return;

    const textInput = document.getElementById('textInput').value;
    const fontSize = document.getElementById('fontSize').value;
    const x = e.offsetX;
    const y = e.offsetY;

    if (textInput) {
        ctx.font = `${fontSize}px Arial`;
        ctx.fillStyle = penColorPicker.value;
        ctx.fillText(textInput, x, y);
    }
});

// 이미지 업로드
imageUpload.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
        const img = new Image();
        img.onload = () => {
            const x = canvas.width / 4;
            const y = canvas.height / 4;
            const width = img.width / 2;
            const height = img.height / 2;
            ctx.drawImage(img, x, y, width, height);
        };
        img.src = reader.result;
    };
    reader.readAsDataURL(file);
});

// 채우기 모드 전환
function toggleFillMode() {
    isFillMode = !isFillMode;
    isTextMode = false;
    document.getElementById('textControls').style.display = 'none';
    alert(isFillMode ? '채우기 모드가 활성화되었습니다.' : '채우기 모드가 비활성화되었습니다.');
}

// 텍스트 삽입 모드 전환
function enableTextMode() {
    isTextMode = true;
    isFillMode = false;
    document.getElementById('textControls').style.display = 'block';
    alert('텍스트 삽입 모드가 활성화되었습니다.');
}

// 캔버스 초기화
function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

// 캔버스 저장
function saveCanvas() {
    const link = document.createElement('a');
    link.download = 'drawing.png';
    link.href = canvas.toDataURL();
    link.click();
}

// Flood Fill 알고리즘
function floodFill(imageData, x, y, targetColor, fillColor) {
    const stack = [[x, y]];
    const width = imageData.width;
    const height = imageData.height;

    while (stack.length) {
        const [px, py] = stack.pop();
        const index = (py * width + px) * 4;

        if (
            px >= 0 && px < width &&
            py >= 0 && py < height &&
            colorsMatch(targetColor, [
                imageData.data[index],
                imageData.data[index + 1],
                imageData.data[index + 2],
                imageData.data[index + 3],
            ])
        ) {
            imageData.data[index] = fillColor[0];
            imageData.data[index + 1] = fillColor[1];
            imageData.data[index + 2] = fillColor[2];
            imageData.data[index + 3] = 255;

            stack.push([px + 1, py]);
            stack.push([px - 1, py]);
            stack.push([px, py + 1]);
            stack.push([px, py - 1]);
        }
    }
}

function getPixelColor(imageData, x, y) {
    const index = (y * imageData.width + x) * 4;
    return [
        imageData.data[index],
        imageData.data[index + 1],
        imageData.data[index + 2],
        imageData.data[index + 3],
    ];
}

function colorsMatch(color1, color2) {
    return color1[0] === color2[0] && color1[1] === color2[1] && color1[2] === color2[2] && color1[3] === color2[3];
}

function hexToRgb(hex) {
    const bigint = parseInt(hex.slice(1), 16);
    const r = (bigint >> 16) & 255;
    const g = (bigint >> 8) & 255;
    const b = bigint & 255;
    return [r, g, b];
}
