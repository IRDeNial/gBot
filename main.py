import string
import ctypes
import os

# For headless browsing.  Life made easy.
from splinter import Browser

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

# Style?  Idk, but this is cool
from ttk import Style

class Application(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def addDebug(self,parent,text):
        parent.insert('end',"%s\n" % (text))

    def doPosting(self,debugLogger,username,password,output,num,delay):
        self.addDebug(debugLogger.insert('end',"%s\n"))

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

        # Delay Between Posts
        L5 = Label(self, text="Delay (seconds)")
        L5.grid(row=4, column=0, sticky=E, pady=1)
        S2 = Spinbox(self, from_=0, to=120, width=28)
        S2.grid(row=4, column=1, ipady=1, sticky=E)
        
        # Post Input
        T1 = Text(self, width=30)
        T1.grid(row=5, columnspan=2, sticky=W+E, pady=1)
        
        # Start button
        B1 = Button(self, text="Start Posting", lambda:do)
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