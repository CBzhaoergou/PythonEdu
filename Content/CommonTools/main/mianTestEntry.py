#!/usr/bin/env python3

#描述:简单的UI与逻辑分离模型
#创建人:cbZhaoErGou
#创建时间:2018.1.11

import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext

#tkinter Ui部分
class Gui():

    def __init__(self,root):
        self.root = root
        self.buttonCallBack = self.__defultFun

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
        frame.scr = scrolledtext.ScrolledText(frame, width=scrolW, height=scrolH, wrap=tk.WORD,bg = '#f2f2f2') 
        frame.scr.grid(column=0, row=12,columnspan=10,rowspan=6,padx = 10,sticky=tk.E + tk.W + tk.S)
        
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
        self.colored_btn.grid(column=9, row=0,rowspan=3)
    
    def setButtonCallBack(self,callback):
        self.buttonCallBack = callback


#核心逻辑部分
class Logic():
    def __init__(self,id):
        print("我是逻辑:%d" % id)

    def myTestFunc(self):
        print("hello")
        

#业务类
class MyTest():
    def __init__(self,root):
        self.gui = Gui(root)
        self.logic = Logic(1)
        self.__linkGuiAndLogic()

    def __linkGuiAndLogic(self):
        self.gui.setButtonCallBack(self.logic.myTestFunc)
       
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

    

 
    

   