import tkinter as tk, random as rd

window = tk.Tk()
window.attributes("-fullscreen", True)


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


print(getMineCoords(10))


def buttonExitClick():
    window.destroy()


exitButton = tk.Button(master=window, text="Exit", bg="red", command=buttonExitClick)
exitButton.place(x=1470, y=5, width=60, height=30)

buttons = dict()
for n in range(80):
    buttons[n] = tk.Button(master=window, text="", bg="gray")


line = 1
row = 1
y = 1
for x in range(80):
    if row == 9:
        y += 1
        row = 1
        line = 1
    buttons[x].place(x=line*60+500, y=y*60, width=60, height=60)
    row += 1
    line += 1

window.mainloop()
