import os
import sys
import tkinter as tk
from PIL import Image, ImageTk
import random
import pygame

# 打包命令
# pyinstaller -F --hidden-import=os,sys,tkinter,PIL,random,pygame --path=E:\Anaconda\pkgs\pygame-2.5.0-py311h4246bbb_0\Lib\site-packages -w --icon=黑洞.ico --add-data "D:\pythonProject\扫雷;." 扫雷.py

# 从临时区设置相对路径
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class Button(tk.Button):
    def __init__(self, window, bg="blue", image="", width=50, height=50, textsize=20, bg2="white", AllButton=None, flagImg=None):
        super().__init__(window, bg=bg, width=width, height=height)
        self.count = 0
        self.visualization, self.flag = False, False
        self.image, self.flagImg = image, flagImg
        self.width = width
        self.height = height
        self.textsize = textsize
        self.bg, self.bg2 = bg, bg2
        self.AllButton = AllButton
        self.bind("<Enter>", self.button_enter)
        self.bind("<Leave>", self.button_leave)
        self.bind("<Button-1>", self.show)
        self.bind("<Button-3>", self.place_flag)

    def set_pos(self, pos):
        self.pos = pos

    def show_img(self):
        if self.count == 0:
            self.config(bg="white")
        elif self.count > 0:
            self.config(text=self.count, bg="white", fg="black", font=("Arial", self.textsize))
        else:
            self.config(image=self.image, bg="white")
        self.visualization = True

    def button_enter(self, event=None):
        if not self.visualization and not self.flag:
            self.config(bg=self.bg2)

    def button_leave(self, event=None):
        if not self.visualization and not self.flag:
            self.config(bg=self.bg)

    def show(self, event=None):
        if self.flag or self.visualization:
            return
        if self.count < 0:
            end(self.AllButton)
        else:
            sound("厉不厉害 你坤哥_[cut_1sec].mp3")
            self.detect(self)

    def detect(self, butt):
        if butt.visualization or butt.count < 0 or butt.flag:
            return
        butt.show_img()
        if butt.count > 0:
            return
        a, b = [1, 0, -1, 0, 1, 1, -1, -1], [0, 1, 0, -1, 1, -1, 1, -1]
        # 递归位置的顺序
        # 8️ 3️ 7️
        # 4️    2️
        # 6️ 1️ 5️
        for i in range(8):
            if 0 <= butt.pos[0] + a[i] < 12 and 0 <= butt.pos[1] + b[i] < 20:
                butt.detect(self.AllButton[(butt.pos[0] + a[i]) * 20 + butt.pos[1] + b[i]])

    def place_flag(self, event=None):
        if self.visualization:
            return
        if not self.flag:
            self.config(image=self.flagImg)
            self.flag = True
        else:
            self.config(image="", bg=self.bg)
            self.flag = False


class Button_canvas:
    def __init__(self, canvas,
                 x, y, length, width=0,
                 delta=3, thick=2,
                 text="", TextSize=1,
                 outline="white", fill='white', outline2="black", fill2="black",
                 font="Arial", shape="rectangle", image="",
                 music=None, loops=0,
                 func=None):
        self.canvas = canvas
        self.x1, self.y1, self.length = x, y, length
        self.width = width if width == 0 else length
        self.delta = delta
        self.shape = shape
        self.music, self.loops = music, loops
        self.outline, self.fill, self.outline2, self.fill2 = outline, fill, outline2, fill2
        self.text = canvas.create_text((x + x + length) // 2, (y + y + width) // 2,
                                       text=text, font=(font, TextSize), fill=fill)
        if shape == "rectangle":
            self.r1 = canvas.create_rectangle(x, y, x + length, y + width, width=thick, outline=outline)
            self.r2 = canvas.create_rectangle(x + delta, y + delta, x + length - delta, y + width - delta,
                                              width=thick, outline=outline)
            self.frame = canvas.create_rectangle(x, y, x + length, y + width, width=0)

        elif shape == "oval":
            self.r1 = canvas.create_oval(x, y, x + length, y + length, width=thick, outline=outline)
            self.r2 = canvas.create_oval(x + delta, y + delta, x + length - delta, y + width - delta, width=thick,
                                         outline=outline)
            self.frame = canvas.create_oval(x, y, x + length, y + length, width=0)

        self.canvas.create_image((x + x + length) // 2, (y + y + width) // 2, image=image)
        self.canvas.tag_bind(self.frame, "<Enter>", self.enter)
        self.canvas.tag_bind(self.frame, "<Leave>", self.leave)
        self.canvas.tag_bind(self.frame, "<Button-1>", lambda event: func())

    def enter(self, event):
        if self.music:
            self.music.play(loops=self.loops)
        if self.shape == "rectangle":
            self.canvas.itemconfig(self.r1, outline=self.outline2)
            self.canvas.itemconfig(self.r2, outline=self.outline2)
            self.canvas.itemconfig(self.text, fill=self.fill2)
        elif self.shape == "oval":
            self.canvas.itemconfig(self.r1, outline=self.outline2)
            self.canvas.itemconfig(self.r2, outline=self.outline2)
            self.canvas.itemconfig(self.text, fill=self.fill2)

    def leave(self, event):
        if self.shape == "rectangle":
            self.canvas.itemconfig(self.r1, outline=self.outline)
            self.canvas.itemconfig(self.r2, outline=self.outline)
            self.canvas.itemconfig(self.text, fill=self.fill)
        elif self.shape == "oval":
            self.canvas.itemconfig(self.r1, outline=self.outline)
            self.canvas.itemconfig(self.r2, outline=self.outline)
            self.canvas.itemconfig(self.text, fill=self.fill)

def sound(path, loops=0, play=True, volume=None):
    path = get_resource_path(path)
    music = pygame.mixer.Sound(path)
    if play:
        music.play(loops=loops)
    volume = volume if volume else pygame.mixer.music.get_volume()
    music.set_volume(volume)
    return music

def create_img(path, size=None):
    img = Image.open(get_resource_path(path))
    if size:
        img = img.resize(size)
    img = ImageTk.PhotoImage(img)
    return img


def init():
    canvas = tk.Canvas(window, width=1200, height=600)
    canvas.pack()
    canvas.create_image(0, 0, image=menu_bg, anchor=tk.NW)
    canvas.create_text(600, 90, text="扫肥雷💣GAME", font=("楷体", 60), fill="#66ffff")
    Button_canvas(canvas, 500, 170, 200, 60,
                  text="⬆ 开始游戏 ⬆", TextSize=20, fill2="cyan", outline2="red",
                  music=sound("Menu Selection Click.wav", play=False), func=start)
    create_butt(canvas, x1=1150, y1=430, x2=1150, y2=530, x3=1150, y3=480, x4=1150, y4=380, d=40,
                image1=sound_plus, image2=sound_minus, image3=sound_img)
    sound("【蔡徐坤】鸡花瓷.mp3", loops=-1)


def restart(event):
    pygame.mixer.stop()
    clean(window)
    init()

def clean(window):
    for widget in window.winfo_children():
        widget.destroy()

def create_butt(root=None, x1=0, y1=0, x2=0, y2=0, d=0, x3=0, y3=0, x4=0, y4=0,
                image1=None, image2=None, image3=None):

    root.create_oval(x1, y1, x1 + d, y1 + d, fill="white", outline="white")
    root.create_oval(x2, y2, x2 + d, y2 + d, fill="white", outline="white")
    root.create_oval(x3, y3, x3 + d, y3 + d, fill="white", outline="black")
    root.create_oval(x4, y4, x4 + d, y4 + d, fill="white", outline="white")
    root.create_image(x3 + d // 2, y3 + d // 2, image=image3)
    plus = root.create_image(x1 + d // 2, y1 + d // 2, image=image1)
    minus = root.create_image(x2 + d // 2, y2 + d // 2, image=image2)
    text = root.create_text(x4 + d // 2, y4 + d // 2, text=round(pygame.mixer.music.get_volume() * 100),
                            font=("楷体", 17), fill="black")
    root.tag_bind(plus, "<Button-1>", lambda event: volume_plus(root, text))
    root.tag_bind(minus, "<Button-1>", lambda event: volume_minus(root, text))

def volume_plus(canvas, text):
    if pygame.mixer.music.get_volume() < 1:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.05)
        volume = pygame.mixer.music.get_volume()
        for i in range(pygame.mixer.get_num_channels()):
            pygame.mixer.Channel(i).set_volume(volume)
        canvas.itemconfig(text, text=round(volume * 100))

def volume_minus(canvas, text):
    if pygame.mixer.music.get_volume() > 0:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.05)
        volume = pygame.mixer.music.get_volume()
        for i in range(pygame.mixer.get_num_channels()):
            pygame.mixer.Channel(i).set_volume(volume)
        canvas.itemconfig(text, text=round(volume * 100))

def start(event=None):
    clean(window)
    pygame.mixer.stop()
    sound("【蔡徐坤】鸡花瓷.mp3", loops=-1)
    button = [Button(window, width=50, height=50, bg="#9bafbb", bg2="#d1dbe0", flagImg=flag_img) for i in range(240)]
    for butt in button:
        butt.AllButton = button
        i = button.index(butt) // 20
        j = button.index(butt) % 20
        butt.set_pos((i, j))
        butt.place(x=50 * j, y=50 * i, width=butt.width, height=butt.height)
    global right_bg, right_obj
    right_bg = tk.Canvas(window, width=300, height=600)
    right_bg.place(x=900, y=0)
    right_obj = right_bg.create_image(0, 0, image=right_img, anchor=tk.NW)
    bomb = random.sample(button, 45)
    a, b = [1, 0, -1, 0, 1, 1, -1, -1], [0, 1, 0, -1, 1, -1, 1, -1]
    for i in bomb:
        i.count = -9
        i.image = bomb_img
        for j in range(8):
            if 0 <= i.pos[0] + a[j] < 12 and 0 <= i.pos[1] + b[j] < 20:
                button[(i.pos[0] + a[j]) * 20 + i.pos[1] + b[j]].count += 1
    create_butt(right_bg, x1=250, y1=430, x2=250, y2=530, x3=250, y3=480, x4=250, y4=380, d=40,
                image1=sound_plus, image2=sound_minus, image3=sound_img)
    Button_canvas(right_bg, 50, 200, 200, 50, text="重新开始", TextSize=20, fill="#0073e6", outline="#0073e6",
                  music=sound("Menu Selection Click.wav", play=False), func=start, fill2="cyan", outline2="cyan")
    Button_canvas(right_bg, 50, 270, 200, 50, text="返回主界面", TextSize=20, fill="#0073e6", outline="#0073e6",
                  music=sound("Menu Selection Click.wav", play=False), func=restart, fill2="cyan", outline2="cyan")
    Button_canvas(right_bg, 50, 340, 200, 50, text="退出游戏", TextSize=20, fill="#0073e6", outline="#0073e6",
                  music=sound("Menu Selection Click.wav", play=False), func=window.quit, fill2="cyan", outline2="cyan")

def end(button):
    pygame.mixer.stop()
    sound("【蔡徐坤】爱鸡.mp3", loops=-1)
    for butt in button:
        if not butt.visualization:
            butt.show_img()
    right_bg.itemconfig(right_obj, image=right_img_smile)


window = tk.Tk()
window.title("扫肥雷💣GAME")
window.iconbitmap(get_resource_path("黑洞.ico"))
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = 1200
window_height = 600
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2 - 50
window.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))
window.resizable(False, False)
flag_img = create_img("旗子.gif", (50, 50))
bomb_img = create_img("炸弹(1比1).gif", (50, 50))
menu_bg = create_img("主界面背景(2比1).gif", (1200, 600))
right_img = create_img("游戏界面右侧背景(1比2).gif", (300, 600))
right_img_smile = create_img("游戏界面右侧背景(1比2).gif", (300, 600))
sound_img = create_img("音量.gif", (40, 40))
sound_plus = create_img("加号.gif", (40, 40))
sound_minus = create_img("减号.gif", (40, 40))
pygame.mixer.init()
pygame.mixer.music.set_volume(0.2)
init()

window.mainloop()
