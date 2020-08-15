from tkinter import *
import tkinter.scrolledtext as scrolledtext
import time
import threading
import queue
from video import Video

class Painter(object):
    def __init__(self):
        self.window = Tk()
        self.window.title("视频")
        self.buttonlist = {}
        self.toplist = {}
        self.textlist = {}
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        ww = 640
        wh = 480
        self.allnum = 0
        self.num = 0
        self.window.geometry("%dx%d+%d+%d" %(ww,wh,(sw-ww) / 2,(sh-wh) / 2))
        self.window.resizable(0,0)
        self.nf_queue = queue.Queue()
    def process_msg(self):
        while True:
            time.sleep(0.3)
            if not self.nf_queue.empty():
                msg = self.nf_queue.get()
                if msg == 1:
                    self.edit()
                elif msg == 2:
                    self.delprogressing()
    def start(self):
        start = Button(self.window, text='启动进度条', command=self.progressing)
        start.place(x=400, y=105)
        over = Button(self.window, text='停止进度条', command=self.delprogressing)
        over.place(x=200, y=105)
        self.buttonlist["start"] = start
        self.buttonlist["over"] = over
        #启动一个线程，去监听数据
        t1 = threading.Thread(target=self.process_msg)
        t1.setDaemon(True)
        t1.start()
        self.window.mainloop()
    def sync_windows(self,event=None):
        #需要一个管理器，统一挪位置
        width = event.width
        height = event.height
        x = event.x
        y = event.y
        for _,top in self.toplist.items():
            top.geometry("320x110+"+str(int(x+width/2))+"+"+str(int(y+height/2)))
    def edit(self):
        self.num = self.num + 1
        top = self.toplist["progressing"]
        T = self.textlist["progressing"]
        fill_line = top.canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")
        # for n in range (self.num, self.allnum+1) :
        text = str(int(self.num)) + "/" +str(int(self.allnum))
        T.configure(text=text)
        s = self.num
        if self.num != 0:
            s = 265 / 100 * self.num
        top.canvas.coords(fill_line, (0, 0, s, 60))
        self.window.update()
        # time.sleep(0.02)  # 控制进度条流动的速度
    def test(self):
        self.window.attributes("-disabled", 1) #禁止主窗口
        # time.sleep(1)
        # self.delprogressing()
        # # 清空进度条
        # fill_line = top.canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="white")
        # x = 500  # 未知变量，可更改
        # n = 465 / x  # 465是矩形填充满的次数
    
        # for t in range(x):
        #     n = n + 465 / x
        #     # 以矩形的长度作为变量值更新
        #     top.canvas.coords(fill_line, (0, 0, n, 60))
        #     self.window.update()
        #     time.sleep(0)  # 时间为0，即飞速清空进度条
    def progressing(self):
        #start process video
        top = Toplevel()
        self.toplist["progressing"] = top
        top.resizable(0,0)
        top.overrideredirect(True)
        curWidth = top.winfo_width()
        curHeight = top.winfo_height()
        x = self.window.winfo_x()
        y = self.window.winfo_y()
        # scnWidth, scnHeight = self.window.winfo_geometry()
        top.geometry("320x110+"+str(int(x+320-50))+"+"+str(int(y+240)))

        text = str(int(self.num)) + "/" +str(int(self.allnum))
        T = Label(top, text=text)
        self.textlist["progressing"] = T
        T.place(x=50, y=60)
        top.canvas = Canvas(top, width=565, height=22, bg="white")
        top.canvas.place(x=110, y=60)

        self.window.bind("<Configure>", self.sync_windows)
        self.test()
        
        self.buttonlist["start"].place_forget()
        self.buttonlist["over"].place_forget()
        vd = Video(self.nf_queue)
        self.allnum = vd.get_num()
        t1 = threading.Thread(target=vd.start)
        t1.setDaemon(True)
        t1.start()
        top.mainloop()
    def delprogressing(self):
        top = self.toplist["progressing"]
        top.destroy()
        self.window.attributes("-disabled", 0)
        self.buttonlist["start"].place(x=400, y=105)
        self.buttonlist["over"].place(x=200, y=105)

if __name__ =='__main__':
    painter = Painter()
    painter.start()