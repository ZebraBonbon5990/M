import tkinter as tk
import random as rd
#import playsound as ps
from functools import partial


def initiate(mode):
    global flag
    window = tk.Tk()
    window.attributes("-fullscreen", True)
    window.title("Minesweeper - {0}".format(mode))
    window.iconbitmap("mine.ico")

    revealedButtons = list()

    if mode == "easy":
        mineAmount = 10
        width = 8
        height = 10
        buttonSize = 60
    elif mode == "medium":
        mineAmount = 15
        width = 10
        height = 12
        buttonSize = 50
    elif mode == "hard":
        mineAmount = 30
        width = 14
        height = 16
        buttonSize = 40


    def getSurrounding(n):
        upperCorners = [i for i in range(width)]
        lowerCorners = [width*height - (i+1) for i in range(width)]
        leftCorners = [width*i for i in range(height)]
        rightCorners = [(width*(i+1))-1 for i in range(height)]
        toReveal = list()
        if not n in upperCorners:
                            toReveal.append(n-width)
        if not n in leftCorners:
                            toReveal.append(n-1)
        if not n in rightCorners:
                            toReveal.append(n+1)
        if not n in lowerCorners:
                            toReveal.append(n+width)
        if not n in upperCorners and not n in leftCorners:
                            toReveal.append(n-(width+1))
        if not n in upperCorners and not n in rightCorners:
                            toReveal.append(n-(width-1))
        if not n in lowerCorners and not n in leftCorners:
                            toReveal.append(n+(width-1))
        if not n in lowerCorners and not n in rightCorners:
                            toReveal.append(n+(width+1))
        return toReveal


    def getMineCoords(amount, n):
        mineCoords = list()
        i = 0
        surrounding = getSurrounding(n)
        while i < amount:
            toAppend = rd.randint(0, width*height-1)
            if toAppend in mineCoords or toAppend in surrounding:
                continue
            else:
                mineCoords.append(toAppend)
                i += 1
        return mineCoords
    

    def exitWindow():
        window.destroy()


    def buttonSwitchClick():
        global flag
        if not flag:
            flag = True
            switchButton.config(text="Flag")
        elif flag:
            flag = False
            switchButton.config(text="Reveal")


    def getValue(n):
        toCheck = getSurrounding(n)
        
        val = 0
        for mineCheck in toCheck:
            if buttons[mineCheck]["Type"] == "Mine":
                val += 1
            else:
                continue
        
        return val


    def buttonClicked(n, ignoreFlags=False):
        if revealedButtons == []:
            mineCoords = getMineCoords(mineAmount, n)
            mineCoords.sort(key=lambda x: x)
            for i in range(height*width):
                if i in mineCoords:
                    buttons[i]["Type"] = "Mine"
                else:
                    buttons[i]["Type"] = "Number"
                    buttons[i]["Value"] = 0
        if not buttons[n]["Revealed"] and not flag:
            if not buttons[n]["Flagged"] or ignoreFlags:
                buttons[n]["Revealed"] = True
                revealedButtons.append(n)
                buttons[n]["Button"].config(fg="black", text="")
                buttons[n]["Button"]["bg"] = "white"
                if buttons[n]["Type"] == "Mine":
                    #ps.playsound("explosion.wav")
                    window.destroy()
                buttons[n]["Value"] = getValue(n)
                if not buttons[n]["Value"] == 0:
                    buttons[n]["Button"]["text"] = buttons[n]["Value"]
                else:
                    toReveal = getSurrounding(n)
                    for i in toReveal:
                        buttonClicked(i, ignoreFlags=True)
                if len(revealedButtons) > width*height - mineAmount - 1:
                    tl = tk.Toplevel(master=window)
                    label = tk.Label(master=tl, text="You won!", fg="green").pack()
                    tl.mainloop()
                if buttons[n]["Button"]["text"] == 1:
                    buttons[n]["Button"].config(fg="blue")
                if buttons[n]["Button"]["text"] == 2:
                    buttons[n]["Button"].config(fg="green")
                if buttons[n]["Button"]["text"] == 3:
                    buttons[n]["Button"].config(fg="red")
                if buttons[n]["Button"]["text"] == 4:
                    buttons[n]["Button"].config(fg="purple")
                if buttons[n]["Button"]["text"] == 5:
                    buttons[n]["Button"].config(fg="yellow")
        elif flag:
            if not buttons[n]["Revealed"]:
                if not buttons[n]["Flagged"]:
                    buttons[n]["Flagged"] = True
                    buttons[n]["Button"].config(fg="red", text="F")
                elif buttons[n]["Flagged"]:
                    buttons[n]["Flagged"] = False
                    buttons[n]["Button"].config(text="", fg="black")


    def wrap(n):
        def wrapper(n=n):
            buttonClicked(n)
        return wrapper

    exitButton = tk.Button(master=window, text="Exit", bg="red", command=exitWindow)
    exitButton.place(x=1470, y=5, width=60, height=30)
    switchButton = tk.Button(master=window, text="Flag", bg="yellow", command=buttonSwitchClick)
    if not flag:
        flag = True
    switchButton.place(x=200, y=200, width=300, height=300)

    line = 1
    y = 1
    buttons = list()
    for n in range(height*width):
        if line == width+1:
            y += 1
            line = 1
        buttons.append({"Button": tk.Button(master=window, text="", bg="gray", command=wrap(n), font=("Arial", 20)), "Revealed": False, "Flagged": False})
        buttons[n]["Button"].place(x=line*buttonSize+500, y=y*buttonSize, width=buttonSize, height=buttonSize)
        line += 1


    window.mainloop()


def switchFullscreen():
    global fullscreen
    if fullscreen:
        mainWindow.attributes("-fullscreen", False)
        fullscreen = False
    else:
        mainWindow.attributes("-fullscreen", True)
        fullscreen = True


fullscreen = True
mainWindow = tk.Tk()
mainWindow.title("Minesweeper - Menu")
mainWindow.iconbitmap("mine.ico")
mainWindow.geometry("500x500")

fullScreenButton = tk.Button(master=mainWindow, text=""" ^ 
< >
 V""", command=switchFullscreen).place(x=30, y=30, width=40, height=40)

mainWindow.attributes("-fullscreen", True)

startButtonEasy = tk.Button(master=mainWindow, text="Start easy mode", command=partial(initiate, "easy"), bg="green", font=("Arial", 20)).place(x=100, y=250, width=300, height=300)
startButtonMedium = tk.Button(master=mainWindow, text="Start Medium mode", command=partial(initiate, "medium"), bg="green", font=("Arial", 20)).place(x=500, y=250, width=300, height=300)
startButtonHard = tk.Button(master=mainWindow, text="Start Hard mode", command=partial(initiate, "hard"), bg="green", font=("Arial", 20)).place(x=900, y=250, width=300, height=300)

mainExitButton = tk.Button(master=mainWindow, text="Exit", command=mainWindow.destroy, bg="red")
mainExitButton.place(x=1470, y=5, width=60, height=30)

flag = True

mainWindow.mainloop()
