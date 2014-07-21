#!/usr/bin/env python

import string
import ctypes
import os
from threading  import Thread
from time import sleep

# For headless browsing.  Life made easy.
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# Tkinter main
from Tkinter import Tk, Frame
# Tkinter GUI widgets
from Tkinter import Button, Text, Entry, Label, Toplevel, Spinbox
# Tkinter alignment options
from Tkinter import LEFT, RIGHT, BOTH, CENTER
# Tkinter directions W=West, E=East, etc...
from Tkinter import N, NE, E, SE, S, SW, W, NW
# Tkinter state options
from Tkinter import DISABLED, NORMAL
# Tkinter position options
from Tkinter import END

# Style?  Idk, but this is cool
from ttk import Style

class Application(Frame):
    threadRunning = False

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def threadded(self,*config):
        self.threadRunning = True

        debugger = config[5]

        self.addDebug(debugger,"Posting thread started")

        self.addDebug(debugger,"  - Configuration:")
        self.addDebug(debugger,"      Output Path: %s" % (config[3]))
        self.addDebug(debugger,"      # of Posts: %d" % (int(config[4])))

        driver = webdriver.PhantomJS('phantomjs')
        self.addDebug(debugger,"  - Driver successfully loaded")

        driver.get('https://accounts.google.com/ServiceLogin?service=oz&continue=https://plus.google.com/')
        self.addDebug(debugger,"  - Successfully navigated to G+ login page")
        
        driver.find_element_by_id("Email").send_keys(config[0])
        driver.find_element_by_id("Passwd").send_keys(config[1])
        driver.find_element_by_name("signIn").click()
        self.addDebug(debugger,"  - Attempting to log in")
        
        if driver.current_url != "https://plus.google.com/":
            self.addDebug(debugger,"  - Incorrect username/password")
        else:
            self.addDebug(debugger,"  - Successfully logged in")

            for x in range(0,int(config[4])):
                self.addDebug(debugger,"  - Searching for text input")

                tempHolder = driver.find_elements_by_tag_name("body")

                profile = ""

                for element in driver.find_elements_by_tag_name("a"):
                    if element.get_attribute("aria-label") == "Profile":
                        profile = element.get_attribute("href")
                        break

                for element in driver.find_elements_by_tag_name("div"):
                    if element.get_attribute("guidedhelpid") == "sharebox_textarea":
                        element.click()
                        break

                sleep(5)

                for element in driver.find_elements_by_tag_name("div"):
                    if element.get_attribute("guidedhelpid") == "sharebox_editor":
                        tempHolder = element
                        break

                for element in tempHolder.find_elements_by_tag_name("div"):
                    if element.get_attribute("role") == "textbox":
                        self.addDebug(debugger, "  - Found it!")
                        self.addDebug(debugger,"  - Inputting Text")
                        element.send_keys(config[2])
                        break

                self.addDebug(debugger,"  - Searching for submit button")
                for element in driver.find_elements_by_tag_name("div"):
                    if element.get_attribute("guidedhelpid") == "shareboxcontrols":
                        tempHolder = element
                        break

                for element in tempHolder.find_elements_by_tag_name("div"):
                    if element.get_attribute("guidedhelpid") == "sharebutton":
                        self.addDebug(debugger, "  - Found it!")
                        element.click()
                        break

                self.addDebug(debugger,"  - Searching for post")

                for element in driver.find_elements_by_tag_name("a"):
                    if element.getAttribute("target") == "_blank":
                        if profile + "/posts/" in element.getAttribute("href"):
                            self.addDebug(debugger,"  - %s" % (element.getAttribute("href")))
                            break

                self.addDebug(debugger,"  - Waiting 5 seconds before another post")
                sleep(5)
        
        self.addDebug(debugger,"Posting thread finished")
        self.threadRunning = False

    def addDebug(self,parent,text):
        parent.insert('end',"%s\n" % (text))

    def doPosting(self,me,debugLogger,username,password,message,output,num):
        if self.threadRunning != True:
            settings = [
                username,
                password,
                message,
                output,
                num,
                debugLogger
            ]

            thread = Thread(target=self.threadded, args=(settings))
            thread.start()
        else:
            self.addDebug(debugLogger,"Attempted to start another posting thread.  Bad.")

    def initUI(self):
        # Main Window
        self.parent.title("gBot")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        # Debug Window
        Toplevel1 = Toplevel(self)
        Toplevel1.title("gBot Debug Console")
        self.pack(fill=BOTH, expand=1)
        TL_T1 = Text(Toplevel1, width=50)
        TL_T1.pack()
        Toplevel1.state("withdrawn")
        Toplevel1.protocol('WM_DELETE_WINDOW', lambda:Toplevel1.state("withdrawn"))
        Toplevel1.attributes("-topmost", True)

        # Username Input
        L1 = Label(self, text="G+ User Name")
        L1.grid(row=0, column=0, sticky=E, ipady=1)
        E1 = Entry(self, width=30)
        E1.grid(row=0, column=1, ipady=1, sticky=E)

        # Password Input
        L2 = Label(self, text="G+ Password")
        L2.grid(row=1, column=0, sticky=E, ipady=1)
        E2 = Entry(self, width=30)
        E2.grid(row=1, column=1, ipady=1, sticky=E)

        # Output Path Input
        L3 = Label(self, text="Output Path")
        L3.grid(row=2, column=0, sticky=E, pady=1)
        E3 = Entry(self, width=30)
        E3.grid(row=2, column=1, ipady=1, sticky=E)
        E3.insert(0, "%s\links.txt" % (os.getcwd()))

        # Num Posts
        L4 = Label(self, text="# Of Posts")
        L4.grid(row=3, column=0, sticky=E, pady=1)
        S1 = Spinbox(self, from_=1, to=9999999, width=28)
        S1.grid(row=3, column=1, ipady=1, sticky=E)
        
        # Post Input
        T1 = Text(self, width=30)
        T1.grid(row=5, columnspan=2, sticky=W+E, pady=1)
        
        # Start button
        B1 = Button(self, text="Start Posting", command=lambda:self.doPosting(B1,TL_T1,E1.get(),E2.get(),T1.get(1.0,END),E3.get(),S1.get()))
        B1.grid(row=6,columnspan=2, sticky=W+E)

        # Debug button
        B2 = Button(self, text="Debug log", command=lambda:Toplevel1.state("normal"))
        B2.grid(row=7, columnspan=2, sticky=W+E)

        self.addDebug(TL_T1,"Started successfully")


def main():
    root = Tk()
    root.resizable(0,0)
    root.wm_iconbitmap("bytecon.ico")
    app = Application(root)
    root.mainloop()

def messageBox(title, text):
    ctypes.windll.user32.MessageBoxA(0, text, title, 1)

if __name__ == '__main__':
    main()