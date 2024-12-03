# tkinter를 사용하기 위한 import
from tkinter import *
from tkinter import ttk
from tkinter.colorchooser import *
from tkinter.simpledialog import *

# tkinter 객체 생성
window = Tk()

# 사용자 id와 password를 저장하는 변수 생성
user_id, password = StringVar(), StringVar()

# 사용자 id와 password를 비교하는 함수
def check_data():
    if user_id.get() == "Passing" and password.get() == "Story":
        print("Logged IN Successfully")
        window.destroy()
    else:
        print("Check your Usernam/Password")

# id와 password, 그리고 확인 버튼의 UI를 만드는 부분
ttk.Label(window, text = "Username : ").grid(row = 0, column = 0, padx = 10, pady = 10)
ttk.Label(window, text = "Password : ").grid(row = 1, column = 0, padx = 10, pady = 10)
ttk.Entry(window, textvariable = user_id).grid(row = 0, column = 1, padx = 10, pady = 10)
ttk.Entry(window, textvariable = password).grid(row = 1, column = 1, padx = 10, pady = 10)
ttk.Button(window, text = "Login", command = check_data).grid(row = 2, column = 1, padx = 10, pady = 10)

window.mainloop()

#함수 선언 부분
id = str(input)
def mouseClick(event) :
    global x1, y1, x2, y2
    x1 = event.x
    y1 = event.y
def mouseDrop(event) :
    global x1, y1, x2, y2, penWidth, penColor
    x2 = event.x
    y2 = event.y
    canvas.create_line(x1, y1, x2 ,y2, width = penWidth, fill = penColor)
def getColor() :
    global penColor
    color = askcolor()
    penColor = color[1]
def getWidth() :
    global penWidth
    penWidth = askinteger("선 두꼐", "선 두께(1~10)를 입력하세요.",
                          minvalue = 1, maxvalue = 10)

#전역 변수 선언 부분
window = None
canvas = None
x1, x2 ,y1, y2 = None, None, None, None  #선의 시작점과 끝점
penColor = 'black'
penWidth = 5

#메인 코드 부분
if __name__ == "__main__" :
    window = Tk()
    window.title("그림판 비슷한 프로그램")
    canvas = Canvas(window, height = 300, width = 300)
    canvas.bind("<Button -1>", mouseClick)
    canvas.bind("<ButtonRelease-1>", mouseDrop)
    canvas.pack()
    mainMenu = Menu(window)
    window.config(menu = mainMenu)
    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label = "설정", menu = fileMenu)
    fileMenu.add_command(label = "선 색상 선택", command = getColor)
    fileMenu.add_separator()
    fileMenu.add_command(label = "선 두께 설정", command = getWidth)

    window.mainloop()