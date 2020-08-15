import os
import re
import subprocess
import threading
import time

rootpath = "F:/video"
outpath = "F:/output"
temp = {"2020081506":1}

class Video(object):
    def __init__(self,_queue=None):
        self.path = "F:/test"
        self.queue = _queue
    def start(self):
        time.sleep(1)
        allpath = {"2020080106":1,"2020080809":1,"2020080808":1,"2020080807":1}
        lists = self.file_name2(rootpath)
        for name in lists:
            if name in allpath:
                continue
            outpath2 = outpath + "/" + name
            inputpath2 = rootpath + "/" + name
            files = self.file_name(inputpath2)
            self.RunScript(files,inputpath2,outpath2+"_")
        self.queue.put(2)
    # 格式转换
    def RunScript(self,files,inputpath, outpath):
        if not os.path.exists(outpath):
            os.makedirs(outpath)
        # ffmpeg -i 1.mp4 -vcodec h264 1.mov
        for name in files:
            code = "ffmpeg -i "
            codeMid = inputpath + "/" + name + " -vcodec h264 "
            subname = name.split(".")
            output = outpath + "/" +subname[0] + ".mov"
            finishcode = code + codeMid + output
            if not os.path.exists(output):
                os.system(finishcode)
                self.queue.put(1)

    def file_name(self,path): 
        list=[]
        for _,_,t in os.walk(path):
            for name in t :
                if "mp4" in name :
                    list.append(name)
        return list
    def file_name2(self,path): 
        list=[]
        for name,name2,t in os.walk(path):
            if len(temp) > 0:
                list.append("2020081506")
                return list
            for name in name2:
                list.append(name)
        return list
    def get_num(self):
        lists = self.file_name2(rootpath)
        outpath2 = outpath + "/" + "2020081506"
        inputpath2 = rootpath + "/" + "2020081506"
        files = self.file_name(inputpath2)
        return len(files)


if __name__ =='__main__':
    vd = Video()
    vd.get_num()