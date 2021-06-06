from pynput.keyboard import Listener
import os
import time
from multiprocessing import Pool

#####################################
# �������ã��������̣���������ָ�����ַ�������ִ����Ӧ�Ķ���
# ���ߣ����ǹ���
#####################################

class ListenKey:
    def __init__(self, listenStr="", actionFunc=None):
        self.listenStr = listenStr
        self.actionFunc = actionFunc
        self.index = 0

    def on_press(self, key):
        # print("��������",key)  # DEBUG
        if self.listenStr == "" or self.actionFunc == None:
            return
        pressKey = None
        try:
            pressKey = key.char
        except AttributeError:
            pressKey = key
        if pressKey == self.listenStr[self.index]:
            # print("���ΰ�����������")  # DEBUG
            if self.index == len(self.listenStr) - 1:
                self.index = 0
                self.actionFunc()
                now = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime())
                print("��%s��ִ�ж���" % (now))  # DEBUG
            else:
                self.index = (self.index + 1) % (len(self.listenStr))
                # print("index+1:",self.index)    #DEBUG
        else:
            self.index = 0
            # print("index��Ϊ0")   #DEBUG

    def on_release(self, key):
        # print("�Ѿ��ͷ�:", format(key)) #DEBUG
        return

    def start_listen(self):
        # print("��ʼ����")       #DEBUG
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

#ָ������
def actionFunc():
    #os.system("shutdown -s now")
    print("hello")

if __name__ == '__main__':
    keywords = ["jichi", "qingdajia", "dajia", "weizheng"]
    listenKey = []
    for i in keywords:
        listenKey.append(ListenKey(i, actionFunc))

    p = Pool(6)  # ���ͬʱִ��4������(һ��ΪCPU����),�н����������ڳ��Ŀռ��ٷ����������������
    for i in listenKey:
        p.apply_async(i.start_listen)  # �ڽ��̳�����ӽ���
    p.close()  # ִ��join()ǰ����ִ��close(),��ʾ���ܼ�������µ�Process��
    p.join()  # �ȴ��ӽ��̽���������ִ��
