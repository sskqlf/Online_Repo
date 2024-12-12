const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d');
let drawing = false;
let x1, y1;

canvas.addEventListener('mousedown', (e) => {
    drawing = true;
    x1 = e.offsetX;
    y1 = e.offsetY;
});

canvas.addEventListener('mousemove', (e) => {
    if (!drawing) return;
    const x2 = e.offsetX;
    const y2 = e.offsetY;
    drawLine(x1, y1, x2, y2);
    x1 = x2;
    y1 = y2;
});

canvas.addEventListener('mouseup', () => {
    drawing = false;
});

function drawLine(x1, y1, x2, y2) {
    // 캔버스에 그리기
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.strokeStyle = 'black';
    ctx.lineWidth = 5;
    ctx.stroke();
    ctx.closePath();

    // Flask API 호출
    fetch('/draw', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ x1, y1, x2, y2 }),
    });
}

function saveImage() {
    fetch('/save', { method: 'POST' })
        .then((response) => response.json())
        .then((data) => {
            alert(data.message);
            window.open(data.path, '_blank');
        });
}

// 이미지 업로드 기능 추가
const imageInput = document.getElementById('imageUpload');
imageInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
        const img = new Image();
        img.onload = () => {
            // 캔버스에 이미지 그리기
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        };
        img.src = event.target.result;
    };
    reader.readAsDataURL(file);
});
