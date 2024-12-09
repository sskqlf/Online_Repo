from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.simpledialog import askinteger, askstring
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import cv2
import numpy as np

# 전역 변수 선언
window = None
canvas = None
penColor = 'black'
penColor_rgb = (0, 0, 0)
penWidth = 5
x1, y1 = None, None
img = np.ones((600, 800, 3), dtype=np.uint8) * 255
eraserMode = False
magnifier_active = False
magnifier_image = None
images = []
active_image = None
active_text = None
drawing_mode = True

# 함수 선언
def mouseClick(event):
    global x1, y1, active_image, active_text, drawing_mode
    x1, y1 = event.x, event.y
    clicked_item = canvas.find_overlapping(event.x, event.y, event.x, event.y)
    if clicked_item:
        for item in clicked_item:
            if "image" in canvas.gettags(item):
                active_image = item
                active_text = None
                drawing_mode = False
                return
            elif "text" in canvas.gettags(item):
                active_text = item
                active_image = None
                drawing_mode = False
                return
    active_image = None
    active_text = None
    drawing_mode = True

def mouseDrag(event):
    global x1, y1
    x2, y2 = event.x, event.y
    if eraserMode:
        erase_size = penWidth
        canvas.create_rectangle(x2 - erase_size, y2 - erase_size, x2 + erase_size, y2 + erase_size, fill="white", outline="white")
        cv2.rectangle(img, (x2 - erase_size, y2 - erase_size), (x2 + erase_size, y2 + erase_size), (255, 255, 255), -1)
    elif drawing_mode:
        canvas.create_line(x1, y1, x2, y2, width=penWidth, fill=penColor, capstyle=ROUND, smooth=True)
        cv2.line(img, (x1, y1), (x2, y2), penColor_rgb, thickness=penWidth)
    elif active_image:
        dx, dy = x2 - x1, y2 - y1
        canvas.move(active_image, dx, dy)
    elif active_text:
        dx, dy = x2 - x1, y2 - y1
        canvas.move(active_text, dx, dy)
    x1, y1 = x2, y2

def mouseDrop(event):
    global x1, y1
    x1, y1 = None, None

def addText():
    global penColor
    text = askstring("텍스트 입력", "추가할 텍스트를 입력하세요:")
    if text:
        x, y = 100, 100  # 기본 텍스트 위치
        text_id = canvas.create_text(x, y, text=text, fill=penColor, font=("Arial", 20), tags="text")

def changeTextColor():
    global active_text
    if active_text:
        color = askcolor()
        if color[1]:
            canvas.itemconfig(active_text, fill=color[1])

def changeTextSize():
    global active_text
    if active_text:
        size = askinteger("텍스트 크기 변경", "텍스트 크기를 입력하세요 (10~100):", minvalue=10, maxvalue=100)
        if size:
            canvas.itemconfig(active_text, font=("Arial", size))

def loadImage():
    global images
    file_path = askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if file_path:
        img_open = Image.open(file_path).resize((100, 100), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(img_open)
        image_id = canvas.create_image(150, 150, anchor=CENTER, image=tk_img, tags="image")
        canvas.image_list.append(tk_img)
        images.append((image_id, img_open))

def resizeImage():
    global active_image
    if active_image:
        new_width = askinteger("이미지 너비", "새로운 너비를 입력하세요:", minvalue=10, maxvalue=800)
        new_height = askinteger("이미지 높이", "새로운 높이를 입력하세요:", minvalue=10, maxvalue=800)
        if new_width and new_height:
            for image_id, original_img in images:
                if image_id == active_image:
                    resized_img = original_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    tk_resized_img = ImageTk.PhotoImage(resized_img)
                    canvas.itemconfig(active_image, image=tk_resized_img)
                    canvas.image_list.append(tk_resized_img)
                    images[images.index((image_id, original_img))] = (image_id, resized_img)
                    break

def getColor():
    global penColor, penColor_rgb
    color = askcolor()
    penColor = color[1]
    r, g, b = color[0]
    penColor_rgb = (int(b), int(g), int(r))

def fillColor(event):
    global img
    x, y = event.x, event.y
    if 0 <= x < img.shape[1] and 0 <= y < img.shape[0]:
        target_color = img[y, x].tolist()
        fill_color = askcolor()[0]
        if fill_color:
            fill_color_bgr = (int(fill_color[2]), int(fill_color[1]), int(fill_color[0]))
            mask = np.zeros((img.shape[0] + 2, img.shape[1] + 2), np.uint8)
            cv2.floodFill(img, mask, (x, y), fill_color_bgr, loDiff=(10, 10, 10), upDiff=(10, 10, 10))
            update_canvas()

def update_canvas():
    global img, canvas_image
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)
    canvas.itemconfig(canvas_image, image=img_tk)
    canvas.img_tk = img_tk

def getWidth():
    global penWidth
    penWidth = askinteger("선 두께", "선 두께(1~10)를 입력하세요.", minvalue=1, maxvalue=10)

def toggle_eraser():
    global eraserMode
    eraserMode = not eraserMode

# UI 초기화
if __name__ == "__main__":
    window = Tk()
    window.title("통합 그림판")
    canvas = Canvas(window, height=600, width=800, bg="white")
    canvas.pack()
    canvas.image_list = []
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)
    canvas_image = canvas.create_image(0, 0, anchor=NW, image=img_tk)
    canvas.img_tk = img_tk

    canvas.bind("<Button-1>", mouseClick)
    canvas.bind("<B1-Motion>", mouseDrag)
    canvas.bind("<ButtonRelease-1>", mouseDrop)
    canvas.bind("<Button-3>", fillColor)

    mainMenu = Menu(window)
    window.config(menu=mainMenu)

    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="설정", menu=fileMenu)
    fileMenu.add_command(label="선 색상 선택", command=getColor)
    fileMenu.add_command(label="선 두께 설정", command=getWidth)

    toolMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="도구", menu=toolMenu)
    toolMenu.add_command(label="이미지 불러오기", command=loadImage)
    toolMenu.add_command(label="이미지 크기 조정", command=resizeImage)
    toolMenu.add_command(label="텍스트 추가", command=addText)
    toolMenu.add_command(label="텍스트 색상 변경", command=changeTextColor)
    toolMenu.add_command(label="텍스트 크기 변경", command=changeTextSize)

    eraser_button = Button(window, text="지우개", command=toggle_eraser)
    eraser_button.pack(side=LEFT, padx=10)

    window.mainloop()
