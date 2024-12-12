const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d');

let isDrawing = false;
let isFillMode = false;
let isTextMode = false;
let isImageMode = false;
let startX, startY;

const penColorPicker = document.getElementById('penColor');
const penWidthInput = document.getElementById('penWidth');
const imageUpload = document.getElementById('imageUpload');

// 선 그리기
canvas.addEventListener('mousedown', (e) => {
    if (isFillMode || isTextMode || isImageMode) return;
    isDrawing = true;
    startX = e.offsetX;
    startY = e.offsetY;
});

canvas.addEventListener('mousemove', (e) => {
    if (!isDrawing || isFillMode || isTextMode || isImageMode) return;
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

// 채우기
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
    const text = document.getElementById('textInput').value;
    const fontSize = document.getElementById('fontSize').value;
    const x = e.offsetX;
    const y = e.offsetY;

    if (text) {
        ctx.font = `${fontSize}px Arial`;
        ctx.fillStyle = penColorPicker.value;
        ctx.fillText(text, x, y);
    }
});

// 이미지 삽입
imageUpload.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
        const img = new Image();
        img.onload = () => {
            canvas.addEventListener('click', function insertImage(event) {
                if (!isImageMode) return;
                const x = event.offsetX;
                const y = event.offsetY;

                const scale = prompt("이미지 크기 비율을 입력하세요 (예: 0.5 = 50%)", "1");
                const width = img.width * parseFloat(scale);
                const height = img.height * parseFloat(scale);
                ctx.drawImage(img, x, y, width, height);

                canvas.removeEventListener('click', insertImage); // 한 번 삽입 후 이벤트 제거
            });
        };
        img.src = reader.result;
    };
    reader.readAsDataURL(file);
});

// 채우기 모드 전환
function toggleFillMode() {
    isFillMode = !isFillMode;
    isTextMode = false;
    isImageMode = false;
    document.getElementById('textControls').style.display = 'none';
    imageUpload.style.display = 'none';
    alert(isFillMode ? '채우기 모드가 활성화되었습니다.' : '채우기 모드가 비활성화되었습니다.');
}

// 텍스트 삽입 모드 전환
function enableTextMode() {
    isTextMode = true;
    isFillMode = false;
    isImageMode = false;
    document.getElementById('textControls').style.display = 'block';
    imageUpload.style.display = 'none';
    alert('텍스트 삽입 모드가 활성화되었습니다.');
}

// 이미지 삽입 모드 전환
function enableImageMode() {
    isImageMode = true;
    isTextMode = false;
    isFillMode = false;
    document.getElementById('textControls').style.display = 'none';
    imageUpload.style.display = 'block';
    alert('이미지 삽입 모드가 활성화되었습니다. 이미지를 선택한 후 캔버스를 클릭하세요.');
}

// 캔버스 초기화
function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
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
