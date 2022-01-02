import tkinter
import Errors
from tkinter import *
from Connect4Logic import StandardRules,FiveInARow
from PIL import ImageTk,Image
from time import sleep


class GraphicalInterfaceForGame:
    def __init__(self):
        self._mainWindow = Tk()
        self._mainWindow.title("Connect 4 by Radoslaw Suder")
        self._gameMode = "Klasyczna"
        self.GraphicForClassicGame()
        self._mainWindow.mainloop()


    def ChangeGameMode(self,gameMode):
        if gameMode == "Klasyczna":
            self._gameMode = gameMode
        elif gameMode == "Pięć w rzędzie":
            self._gameMode = gameMode


    def GraphicForClassicGame(self):
        self._logic = StandardRules()

        self._mainWindow.geometry("700x660")
        self._mainWindow.resizable(0, 0)

        self._header = self._CreateHeader(75)

        self._blueImage = Image.open("images\\red_full.png")
        self._yellowImage = Image.open("images\\yellow_full.png")
        self._resized_image1 = self._blueImage.resize((20, 20), Image.ANTIALIAS)
        self._resized_image2 = self._yellowImage.resize((20, 20), Image.ANTIALIAS)
        self._image1 = ImageTk.PhotoImage(self._resized_image1)
        self._image2 = ImageTk.PhotoImage(self._resized_image2)

        self._barToDropCoins = self._CreateBarToDropCoins()
        self.ChangeColorOfCoinsInHeader()
        self._board = self._CreateBoard(700,600)
        self._endGameWithTie = None

    def GraphicsForFiveInARow(self):
        self._logic = FiveInARow()
        self._mainWindow.geometry("900x660")
        self._mainWindow.resizable(0, 0)

        self._header = self._CreateHeader(100)

        self._blueImage = Image.open("images\\red_full.png")
        self._yellowImage = Image.open("images\\yellow_full.png")
        self._resized_image1 = self._blueImage.resize((20, 20), Image.ANTIALIAS)
        self._resized_image2 = self._yellowImage.resize((20, 20), Image.ANTIALIAS)
        self._image1 = ImageTk.PhotoImage(self._resized_image1)
        self._image2 = ImageTk.PhotoImage(self._resized_image2)

        self._barToDropCoins = self._CreateBarToDropCoins()
        self.ChangeColorOfCoinsInHeader()
        self._board = self._CreateBoard(900,600)
        self.PrintCoins()
        self._endGameWithTie = None


    def _CreateHeader(self,widthOfLabel):
        headerFrame = LabelFrame(self._mainWindow)
        headerFrame.place(x= 0, y = 0, height = 200, width = self._mainWindow.winfo_width())
        headerFrame.pack()
        clicked = StringVar()
        clicked.set(self._gameMode)
        dropOptionsMenu = OptionMenu(headerFrame,clicked,"Klasyczna", "Pięć w rzędzie", command= lambda s:[self.ChangeGameMode(s),self.Restart()])
        dropOptionsMenu.grid(row = 0, column = 0)
        whosTurnLabel = Label(headerFrame, text = "Tura Gracza " + str(self._logic.ActivePlayer),width = widthOfLabel,
                              bg = self._logic.colorOfActivePlayer)
        whosTurnLabel.grid(row = 0, column = 1)
        resetButton = Button(headerFrame,text = "Restart Gry", command = lambda:self.Restart())
        resetButton.grid(row =0, column = 2 )

        return headerFrame

    def _CreateBarToDropCoins(self):

        coinTossFrame = Frame(self._mainWindow,bg = "black")
        coinTossFrame.place(x=0,y = 0, height = 100,width = self._mainWindow.winfo_width())

        for eachColumn in range(0,self._logic.numberOfCols):
            button = Button(coinTossFrame,bg = "black",
                            command = lambda columnToDropCoin = eachColumn +1 : self.DropCoin(columnToDropCoin)  )
            button.grid(row=0, column=eachColumn, padx= 37)

        coinTossFrame.pack()
        return coinTossFrame



    def _CreateBoard(self,widthOfWindow,heightOfWindow):
        boardGraphical = Canvas(self._mainWindow,width = widthOfWindow, height = heightOfWindow, bg = "blue")
        boardGraphical.pack()

        for coinsForColums in range(0,self._logic.numberOfCols):
            for coinsForRows in range(0,self._logic.numberOfRows):
                coord = (coinsForColums*100,coinsForRows*100,coinsForColums*100 +100,coinsForRows*100 +100)
                l = boardGraphical.create_oval(coord, fill = "white")

        return boardGraphical


    def DropCoin(self,columnToDropCoin):
        self.BlockButtonsForDroppingCoins()

        try:
            self._logic.DropCoin(columnToDropCoin)
        except Errors.FullColumnException:
            self.PopupFullColumn()
            return
        except Errors.FullGameBoardException:
            self._endGameWithTie = True

        self.AnimateDropingCoin(columnToDropCoin)
        self.PrintCoins()

        self._logic.CheckWin()
        if self._logic.WhoWins() == 1 or self._logic.WhoWins() == 2:
            win = self.PopupForWinner()
            self._mainWindow.wait_window(win)
            return

        if self._endGameWithTie == True:
            full = self.PopupFullGameBoard()
            self._mainWindow.wait_window(full)
            return

        self._logic.ChangeActivePlayer()

        self._header.winfo_children()[1].configure(text = "Tura Gracza " + str(self._logic.ActivePlayer),
                                               bg = self._logic.colorOfActivePlayer)

        self.ChangeColorOfCoinsInHeader()
        self.UnlockButtonsForDroppingCoins()



    def BlockButtonsForDroppingCoins(self):
        for child in self._barToDropCoins.winfo_children():
            child.configure(state='disable')

    def UnlockButtonsForDroppingCoins(self):
        for child in self._barToDropCoins.winfo_children():
            child.configure(state='normal')





    def ChangeColorOfCoinsInHeader(self):
        for numberOfButtons in range(0,self._logic.numberOfCols):
            if self._logic.ActivePlayer == 1:
                self._barToDropCoins.winfo_children()[numberOfButtons].configure(image = self._image1)
            else:
                self._barToDropCoins.winfo_children()[numberOfButtons].configure(image = self._image2)


    def PrintCoins(self):
        iter = 0
        iter2= 0

        for eachRow in self._logic.Board[::-1]:
            for oneElemInRow in eachRow:
                if oneElemInRow == 1:
                    coord = ( iter2 * 100, iter*100, iter2*100 +100, iter * 100 + 100)
                    self._board.create_oval(coord, fill ="red")

                if oneElemInRow == 2:
                    coord = (iter2 * 100, iter * 100, iter2 * 100 + 100, iter * 100 + 100)
                    self._board.create_oval(coord, fill="yellow")
                iter2 += 1
            iter2 = 0
            iter += 1


    def AnimateDropingCoin(self,column):
        iter = 0
        for eachRow in self._logic.Board[::-1]:
            if eachRow[column-1] is not None:
                coordStart = ((column-1) * 100, 0, ((column-1) * 100) + 100, 100)
                coin = self._board.create_oval(coordStart, fill = self._logic.colorOfActivePlayer)

                for elem in range(0, iter * 100):
                    self._board.move(coin, 0, 1)
                    self._mainWindow.update()
                break
            iter += 1

    def PopupForWinner(self):
        top = Toplevel(width = 300, height = 100, bg = self._logic.colorOfActivePlayer )
        top.resizable(0,0)
        top.title("Wygrana")
        congrats = Label(top, text = "Wygrał Gracz "  + str(self._logic.WhoWins()) ,font = ("Arial",31),
                         bg = self._logic.colorOfActivePlayer   )
        congrats.place(x=0, y=0)
        okButton =  Button(top,text = "Zakończ" , command = lambda:[top.destroy(),self.Restart()] )
        okButton.place(x=125,y=60)

    def PopupFullColumn(self):
        popUpFull = Toplevel(width=300, height=100, bg="white")
        popUpFull.resizable(0, 0)
        popUpFull.title("Kolumna Pełna")
        fullColumnLabel = Label(popUpFull, text="Nie można wrzucić monety do pełnej kolumny", font=("Arial", 10),
                         bg="white")
        fullColumnLabel.place(x=0, y=0)
        okButton = Button(popUpFull, text="Rozumiem", command=lambda: [popUpFull.destroy(),
                                                                       self.UnlockButtonsForDroppingCoins()])
        okButton.place(x=125, y=60)

    def PopupFullGameBoard(self):

        windowForTie = Toplevel(width = 300, height = 100, bg = "blue" )
        windowForTie.resizable(0,0)
        windowForTie.title("Remis")
        tieLabel = Label(windowForTie, text = "Remis " ,font = ("Arial",31),
                         bg = "blue"  )
        tieLabel.place(x=80, y=0)
        okButton =  Button(windowForTie,text = "Zakończ" , command = lambda:[windowForTie.destroy(),self.Restart()] )
        okButton.place(x=125,y=60)


    def Restart(self):
        self._board.destroy()
        self._barToDropCoins.destroy()
        self._header.destroy()

        if self._gameMode == "Klasyczna":
            self.GraphicForClassicGame()
        elif self._gameMode == "Pięć w rzędzie":
            self.GraphicsForFiveInARow()











