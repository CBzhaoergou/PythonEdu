#!/usr/bin/env python3

#描述:简单的UI与逻辑分离模型
#创建人:cbZhaoErGou
#创建时间:2018.1.11

import os
import sys
import base64
import hashlib
import tkinter as tk
import tkinter.ttk as ttk
import subprocess 
import time
from tkinter import scrolledtext
import threading
import re
import sqlite3
import importlib
import queue
from tkinter.filedialog import askdirectory
from tkinter import messagebox
from tkinter import Toplevel
import math
import traceback

#增加搜索路径
sys.path.append("./CommonTools/ui/")
import mtk_Dalog


#tkinter Ui部分
class Gui():

    def __init__(self,root):
        self.root = root
        self.buttonCallBack = self.__defultFun
        self.entry1Value = tk.StringVar()

        self.__crateMianPage()

    def __defultFun(self):
        print("这里是默认的回调函数")
    
    def __crateMianPage(self):
        # Tab Control introduced here --------------------------------------  
        tabControl = ttk.Notebook(self.root)           # Create Tab Control  

        self.tab1 = ttk.Frame(tabControl)            # Create a tab   
        tabControl.add(self.tab1, text='test1')      # Add the tab
       
        self.tab2 = ttk.Frame(tabControl)            # Add a second tab  
        tabControl.add(self.tab2, text='test2')      # Make second tab visible 
     
        self.tab3 = ttk.Frame(tabControl)            # Add a third tab  
        tabControl.add(self.tab3, text='test3')      # Make second tab visible
        self.__createTest1Ui()

        tabControl.pack(expand=1, fill="both")  # Pack to make visible
          
    def __createTest1Ui(self):
        frame = self.tab1
        scrolW  = 102; scrolH  = 24  
        frame.scr = scrolledtext.ScrolledText(frame, width=scrolW, height=scrolH, wrap=tk.WORD,bg = '#f2f2f2',state = "disabled") 
        frame.scr.grid(column=0, row=12,columnspan=10,rowspan=6,padx = 10,sticky=tk.E + tk.W + tk.S)
        self.scr = frame.scr

        tmpFrame = tk.Frame(frame, width=800, height=160,bg='#ffffe0')
        tmpFrame.grid(row=2, column=0,columnspan=10,sticky=tk.W)

        style = ttk.Style()
        style.map("C.TButton",
            foreground=[('pressed', 'black'), ('active', 'black')],
            background=[('pressed', '!disabled', 'blue'), ('active', 'blue')],
            width = [('pressed', 120), ('active', 120)],
            height = [('pressed', '!disabled', 50), ('active', 50)],
        )
        
        self.colored_btn = ttk.Button(frame,text="测试", style="C.TButton",command = lambda:self.buttonCallBack())
        self.colored_btn.grid(row=0,column=9,rowspan=2)


        self.rebtn = ttk.Button(frame,text="刷新", style="C.TButton",command = lambda:self.resumedApp())
        self.rebtn.grid(row=5,column=9,rowspan=1)


        #只允许输入数字的输入框
        def validatecommand():
            pattern = re.compile(r"\D")
            if ord(self.mC) == 127:
                return True
        
            if re.match(pattern,self.mC):
                return False
            else:
                return True
        def key(event):
            self.mC = event.char
            # print(repr(self.mC))
        def actionCmd(event):
            self.buttonCallBack()
            pass
        entry1 = tk.Entry(frame, textvariable = self.entry1Value,width = 10,validate = "key",validatecommand = validatecommand )
        entry1.grid(row = 0, column = 8,rowspan=2,sticky = tk.W+ tk.E)
        entry1.bind('<Return>',actionCmd)
        entry1.bind('<Key>',key)

    def __insertInfoToScr(self,scrObj,pos,text,color = None):
        scrObj.configure(state='normal',foreground = 'black')
        scrObj.update_idletasks()
        if color!=None:
            scrObj.tag_add(color,pos)
            scrObj.tag_config(color,foreground = color)
            scrObj.insert(pos,text,(color,))
        else:
            scrObj.insert(pos,text)
        scrObj.see(pos)
        scrObj.configure(state='disabled',foreground = 'black')
        
    
    def setButtonCallBack(self,callback):
        self.buttonCallBack = callback

    #获得EntryData数据
    def getEntryData(self):
        if self.entry1Value.get() != "":
            return int(self.entry1Value.get())
        return None

    def showDataToUi(self,strText):
        self.__insertInfoToScr(self.scr,tk.END,strText + "\n")
        pass

    def resumedApp(self):
        self.root.quit()
        obj1 = subprocess.Popen("python myTest.py",
                            shell = True,
                            # cwd = ,
                            stdin = subprocess.PIPE,
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE,
                            universal_newlines = True)
        obj1.stdin.close()
        obj1.stdout.close()
        obj1.stderr.close()

#数据处理
class Logic():
    def __init__(self):
        # print("初始化数据处理类")
        pass
       
    def calculateData(self,param):
        return param*param
        
#业务逻辑
class MyTest():
    def __init__(self,root):
        self.root = root
        self.gui = Gui(root)
        self.logic = Logic()
        self.__linkGuiAndLogic()

    def __linkGuiAndLogic(self):
        self.gui.setButtonCallBack(self.showDalog)

    def showDalog(self):
        self.calculate()
        pass

    def calculate(self):
        tmpvalue = self.gui.getEntryData()
        if tmpvalue == None:
           tmpStr = "无效值"
        else:
           tmpStr = str("%d的平方等于:%d" % (tmpvalue, self.logic.calculateData(tmpvalue)))
        self.gui.showDataToUi(tmpStr)

    

def main():
    
    root = tk.Tk() # 这里
    #fix the root window size
    root.minsize(840, 600)
    root.maxsize(840, 600) #这里主要是控制窗口的大小，让窗口大小不能改变
    root.title('测试环境') #设置主窗口的标题
    mytools = MyTest(root)

    root.mainloop()   # 这里进入顶层窗口的循环

if __name__ == '__main__':
    main()

    

 
    

   