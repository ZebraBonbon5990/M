import tkinter as tk
import random as rd
import playsound as ps
from functools import partial

window = tk.Tk()
window.attributes("-fullscreen", True)
window.title("Minesweeper")
window.iconbitmap("mine.ico")

flag = True
revealedButtons = list()


def getMineCoords(amount):
    mineCoords = list()
    i = 0
    while i < amount:
        toappend = rd.randint(0, 79)
        if toappend in mineCoords:
            continue
        else:
            mineCoords.append(toappend)
            i += 1
    return mineCoords


def buttonExitClick():
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
    toCheck = list()
    upperCorners = [0, 1, 2, 3, 4, 5, 6, 7]
    lowerCorners = [72, 73, 74, 75, 76, 77, 78, 79]
    leftCorners = [0, 8, 16, 24, 32, 40, 48, 56, 64, 72]
    rightCorners = [7, 15, 23, 31, 39, 47, 55, 63, 71, 79]
    if True:
        if not n in upperCorners:
            toCheck.append(n-8)
        if not n in leftCorners:
            toCheck.append(n-1)
        if not n in rightCorners:
            toCheck.append(n+1)
        if not n in lowerCorners:
            toCheck.append(n+8)
        if not n in upperCorners and not n in leftCorners:
            toCheck.append(n-9)
        if not n in upperCorners and not n in rightCorners:
            toCheck.append(n-7)
        if not n in lowerCorners and not n in leftCorners:
            toCheck.append(n+7)
        if not n in lowerCorners and not n in rightCorners:
            toCheck.append(n+9)
    
    val = 0
    for mineCheck in toCheck:
        if buttons[mineCheck]["Type"] == "Mine":
            val += 1
        else:
            continue
    
    return val


def buttonClicked(n):
    if not buttons[n]["Revealed"] and not flag:
        buttons[n]["Revealed"] = True
        revealedButtons.append(n)
        buttons[n]["Button"]["bg"] = "white"
        if buttons[n]["Type"] == "Mine":
            ps.playsound("Sounds/explosion.wav")
            exit()
        if len(revealedButtons) > 69:
            tl = tk.Toplevel()
            label = tk.Label(master=tl, text="You won!", fg="green").pack()
            tl.mainloop()
        buttons[n]["Value"] = getValue(n)
        if not buttons[n]["Value"] == 0:
            buttons[n]["Button"]["text"] = buttons[n]["Value"]
        if buttons[n]["Button"]["text"] == 1:
            buttons[n]["Button"].config(fg="#3240a8")
        print(n)
    elif flag:
        if not buttons[n]["Flagged"]:
            buttons[n]["Flagged"] = True
            buttons[n]["Button"].config(fg="red", text="F")
        elif buttons[n]["Flagged"]:
            buttons[n]["Flagged"] = False
            buttons[n]["Button"].config(text="", fg="black")


mineCoords = getMineCoords(10)
mineCoords.sort(key=lambda x: x)

exitButton = tk.Button(master=window, text="Exit", bg="red", command=buttonExitClick)
exitButton.place(x=1470, y=5, width=60, height=30)
switchButton = tk.Button(master=window, text="Flag", bg="yellow", command=buttonSwitchClick)
switchButton.place(x=770, y=5, width=60, height=30)

buttons = list()
for n in range(80):
    buttons.append({"Button": tk.Button(master=window, text="", bg="gray", command=partial(buttonClicked, n), font=("Arial", 20)), "Revealed": False, "Flagged": False})
    if n in mineCoords:
        buttons[n]["Type"] = "Mine"
    else:
        buttons[n]["Type"] = "Number"
        buttons[n]["Value"] = 0


line = 1
y = 1
for x in range(80):
    if line == 9:
        y += 1
        line = 1
    buttons[x]["Button"].place(x=line*60+500, y=y*60, width=60, height=60)
    line += 1

window.mainloop()
