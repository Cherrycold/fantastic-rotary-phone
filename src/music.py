'''
@Author: your name
@Date: 2020-04-02 13:54:57
@LastEditTime: 2020-08-14 17:53:10
@LastEditors: your name
@Description: 
@FilePath: \learnlua\a.py
'''
# encoding:utf-8
import time
import os
from pygame import mixer
import time
import random
from tkinter import *
import tkinter.scrolledtext as scrolledtext
import _thread
 
def file_name(path): 
    list=[]
    for _,_,t in os.walk(path):
        for name in t :
            if "mp3" in name :
                list.append(name)
    return list

def log(outstr):
    return "[ "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+" ] : "\
        + outstr + "\n"

class Player(object):
    def __init__(self):
        self.flag = TRUE
        self.path = "F:/test"
        self.wks = file_name(self.path)
        mixer.init()

    def playMp3(self):
        self.flag = TRUE
        num = random.randint(0,len(self.wks)-1)
        self.scr.insert(END,log("Play "+self.wks[num]))
        mixer.music.load(self.path+"/"+self.wks[num])
        mixer.music.play(1)

    def playMp3_2(self):
        if self.flag == FALSE:
            mixer.music.unpause()
            self.flag = TRUE
            self.scr.insert(END,log("Unpause"))
            return
        mixer.music.pause()
        self.scr.insert(END,log("Pause"))
        self.flag = FALSE

    def start(self):
        self.playMp3()
        while True:
            time.sleep(10)
            if self.flag and not mixer.music.get_busy():
                self.playMp3()
    def painter(self):
        frame1 = Tk()
        sw = frame1.winfo_screenwidth()
        sh = frame1.winfo_screenheight()
        ww = 640
        wh = 480
        frame1.geometry("%dx%d+%d+%d" %(ww,wh,(sw-ww) / 2,(sh-wh) / 2))            #设置窗口的大小为640*480
        frame1.resizable()                                  #窗口大小可以通过鼠标拖动改变，app.master.resizable(0,0)则表示窗口大小不可改变
        frame1.title("Windows")                             #设置窗口的名称         
        

        self.scr = scrolledtext.ScrolledText(frame1, width=70, height=13)  #滚动文本框（宽，高（这里的高应该是以行数为单位），字体样式）
        self.scr.place(x=50, y=50) #滚动文本框在页面的位置

        start = Button(frame1, text="开始播放",height = 2, width=12, command=player.playMp3)
        start.place(x=70,y=329)
        
        over = Button(frame1, text="停止/继续播放",height = 2, width=12, command=player.playMp3_2)
        over.place(x=440,y=329)

        # def callback(event): 
        #     print("当前位置：",event.x,event.y)
        # frame1.bind("<Button-1>",callback)
        frame1.mainloop()
if __name__ =='__main__':
    player = Player()
    player.painter()
