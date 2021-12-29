import tkinter
from tkinter import *


class GraphicalInterfaceForGame:
    def __init__(self,numberOfCols,numberOfRows):
        self._numberOfCols = numberOfCols
        self._numberOfRows = numberOfRows
        self._mainWindow = Tk()
        self._mainWindow.title("Connect 4 by Radoslaw Suder")
        self._mainWindow.geometry("640x480")
        self._CreateHeader()
        self._CreateBoard()

    def _CreateHeader(self):
        headerFrame = LabelFrame(self._mainWindow, bg = "green")
        headerFrame.place(x= 0, y = 0, height = 200, width = self._mainWindow.winfo_width())
        headerFrame.pack()

        clicked = StringVar()
        clicked.set("Klasyczna")
        dropOptionsMenu = OptionMenu(headerFrame,clicked,"Klasyczna","Opcja1")
        dropOptionsMenu.grid(row = 0, column = 0)

        whosTurnLabel = Label(headerFrame, text = "Gracz1")
        whosTurnLabel.grid(row = 0, column = 1)

        resetButton = Button(headerFrame,text = "Restart Gry")
        resetButton.grid(row =0, column = 3 )

    def _CreateBoard(self):





    def mainLoop(self):
        self._mainWindow.mainloop()









