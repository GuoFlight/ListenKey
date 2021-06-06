from pynput.keyboard import Listener
import os
import time
from multiprocessing import Pool

#####################################
# 程序作用：监听键盘，若输入了指定的字符串，则执行相应的动作
# 作者：京城郭少
#####################################

class ListenKey:
    def __init__(self, listenStr="", actionFunc=None):
        self.listenStr = listenStr
        self.actionFunc = actionFunc
        self.index = 0

    def on_press(self, key):
        # print("监听到了",key)  # DEBUG
        if self.listenStr == "" or self.actionFunc == None:
            return
        pressKey = None
        try:
            pressKey = key.char
        except AttributeError:
            pressKey = key
        if pressKey == self.listenStr[self.index]:
            # print("本次按键符合条件")  # DEBUG
            if self.index == len(self.listenStr) - 1:
                self.index = 0
                self.actionFunc()
                now = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime())
                print("【%s】执行动作" % (now))  # DEBUG
            else:
                self.index = (self.index + 1) % (len(self.listenStr))
                # print("index+1:",self.index)    #DEBUG
        else:
            self.index = 0
            # print("index变为0")   #DEBUG

    def on_release(self, key):
        # print("已经释放:", format(key)) #DEBUG
        return

    def start_listen(self):
        # print("开始监听")       #DEBUG
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

#指定动作
def actionFunc():
    #os.system("shutdown -s now")
    print("hello")

if __name__ == '__main__':
    keywords = ["jichi", "qingdajia", "dajia", "weizheng"]
    listenKey = []
    for i in keywords:
        listenKey.append(ListenKey(i, actionFunc))

    p = Pool(6)  # 最多同时执行4个进程(一般为CPU核数),有进程运行完腾出的空间再分配给其他进程运行
    for i in listenKey:
        p.apply_async(i.start_listen)  # 在进程池中添加进程
    p.close()  # 执行join()前必须执行close(),表示不能继续添加新的Process了
    p.join()  # 等待子进程结束再往下执行
