import tkinter
import Errors
import math
from tkinter import *
from Connect4Logic import StandardRules,FiveInARow,PlayWithAI
from PIL import ImageTk,Image
from time import sleep



class GraphicalInterfaceForGame:
    '''
    Klasa odpowiedzialna za graficzna implementacje gry connect4 z modulu Connect4Logic
    '''
    def __init__(self):
        self._mainWindow = Tk()
        self._mainWindow.title("Connect 4 by Radoslaw Suder")
        self._gameMode = "Klasyczna" #uruchamiana na poczatku klasyczna wersja gry
        self.GraphicForClassicGame()
        self._mainWindow.mainloop()


    def ChangeGameMode(self,gameMode):
        '''
        Zmiana trybu gry na inny
        :param gameMode: tryb gry na ktory zmienia sie gra
        '''
        if gameMode == "Klasyczna":
            self._gameMode = gameMode
        elif gameMode == "Pięć w rzędzie":
            self._gameMode = gameMode
        elif gameMode == "Gra z Komputerem":
            self._gameMode = gameMode


    def GraphicForClassicGame(self):
        '''
        Tryb graficzny dla podstawowego(klasycznego) trybu gry
        '''
        self._logic = StandardRules() #utworzenie obiektu z logika dla standardowego trybu
        self._mainWindow.geometry("700x660")
        self._mainWindow.resizable(0, 0)

        self._header = self._CreateHeader(75) #utworzenie górnego paska gry z przyciskami

        self._blueImage = Image.open("images\\red_full.png") #wczytanie obrazkow do uzycia w spuszczaniu monet
        self._yellowImage = Image.open("images\\yellow_full.png")
        self._resized_image1 = self._blueImage.resize((20, 20), Image.ANTIALIAS)
        self._resized_image2 = self._yellowImage.resize((20, 20), Image.ANTIALIAS)
        self._image1 = ImageTk.PhotoImage(self._resized_image1)
        self._image2 = ImageTk.PhotoImage(self._resized_image2)

        self._barToDropCoins = self._CreateBarToDropCoins() #utworzenie paska do spuszczania monet
        self.ChangeColorOfCoinsInHeader()
        self._board = self._CreateBoard(700,600) #utworzenie graficznej interpretacji pola gry
        self._endGameWithTie = None

    def GraphicsForFiveInARow(self):
        '''
        Tryb graficzny dla gry z wieksza plansza(połacz 5)
        '''
        self._logic = FiveInARow() #utworzenie obiektu z logika dla trybu z wieksza plansza
        self._mainWindow.geometry("900x660")
        self._mainWindow.resizable(0, 0)

        self._header = self._CreateHeader(100) #utworzenie górnego paska gry z przyciskami

        self._blueImage = Image.open("images\\red_full.png") #wczytanie obrazkow do uzycia w spuszczaniu monet
        self._yellowImage = Image.open("images\\yellow_full.png")
        self._resized_image1 = self._blueImage.resize((20, 20), Image.ANTIALIAS)
        self._resized_image2 = self._yellowImage.resize((20, 20), Image.ANTIALIAS)
        self._image1 = ImageTk.PhotoImage(self._resized_image1)
        self._image2 = ImageTk.PhotoImage(self._resized_image2)

        self._barToDropCoins = self._CreateBarToDropCoins() #utworzenie paska do spuszczania monet
        self.ChangeColorOfCoinsInHeader()
        self._board = self._CreateBoard(900,600) #utworzenie graficznej interpretacji pola gry
        self.PrintCoins() #wywolanie funkcji rysujacej monety zgodnie z logika
        self._endGameWithTie = None

    def GraphicsForPlayWithAi(self):
        '''
        Tryb graficzny dla gry z komputerem
        '''
        self._logic = PlayWithAI() #utworzenie obiektu z logika dla trybu gry z komputerem

        self._mainWindow.geometry("700x660")
        self._mainWindow.resizable(0, 0)

        self._header = self._CreateHeader(68) #utworzenie górnego paska gry z przyciskami

        self._blueImage = Image.open("images\\red_full.png")
        self._yellowImage = Image.open("images\\yellow_full.png")
        self._resized_image1 = self._blueImage.resize((20, 20), Image.ANTIALIAS)
        self._resized_image2 = self._yellowImage.resize((20, 20), Image.ANTIALIAS)
        self._image1 = ImageTk.PhotoImage(self._resized_image1)
        self._image2 = ImageTk.PhotoImage(self._resized_image2)

        self._barToDropCoins = self._CreateBarToDropCoins()  #utworzenie paska do spuszczania monet
        self.ChangeColorOfCoinsInHeader()
        self._board = self._CreateBoard(700,600) #utworzenie graficznej interpretacji pola gry
        self._endGameWithTie = None


    def _CreateHeader(self,widthOfLabel) -> LabelFrame:
        '''
        Tworzenie gornego paska z przyciskami do resetu gry i wyobr trybu oraz wyswietlanei aktualnego gracza
        :param widthOfLabel: szerokosc tworzeonego paska
        :return: obiekt utworzonego paska do pozniejszej obslugi
        '''
        headerFrame = LabelFrame(self._mainWindow)
        headerFrame.place(x= 0, y = 0, height = 200, width = self._mainWindow.winfo_width())
        headerFrame.pack()
        clicked = StringVar()
        clicked.set(self._gameMode)
        ''' Przycisk z wyborem trybu gry'''
        dropOptionsMenu = OptionMenu(headerFrame,clicked,"Klasyczna", "Pięć w rzędzie","Gra z Komputerem", command= lambda s:[self.ChangeGameMode(s),self.Restart()])
        dropOptionsMenu.grid(row = 0, column = 0)
        '''Pasek z pokazaniem ktory gracz ma aktualnie ture '''
        whosTurnLabel = Label(headerFrame, text = "Tura Gracza " + str(self._logic.ActivePlayer), width = widthOfLabel,
                              bg = self._logic.ColorOfActivePlayer)
        whosTurnLabel.grid(row = 0, column = 1)
        '''Przycisk do resetowania gry'''
        resetButton = Button(headerFrame,text = "Restart Gry", command = lambda:self.Restart())
        resetButton.grid(row =0, column = 2 )

        return headerFrame

    def _CreateBarToDropCoins(self) -> Frame:
        '''
        Tworzenie paska z przyciskami do upuszczania monet
        :return: obiekt utworzonego paska do pozniejszej obslugi
        '''

        coinTossFrame = Frame(self._mainWindow,bg = "black")
        coinTossFrame.place(x=0,y = 0, height = 100,width = self._mainWindow.winfo_width())

        for eachColumn in range(0, self._logic.NumberOfCols):
            if self._gameMode == "Gra z Komputerem": #tworzenie przyciskow przy grze z komputerem
                button = Button(coinTossFrame, bg="black",
                                command=lambda columnToDropCoin=eachColumn + 1: [self.DropCoin(columnToDropCoin),
                                                                                 self.DropCoinAI()] )
            else: #tworzenie przyciskow do gry bez komputera
                button = Button(coinTossFrame,bg = "black",
                            command = lambda columnToDropCoin = eachColumn +1 : self.DropCoin(columnToDropCoin)  )
            button.grid(row=0, column=eachColumn, padx= 37)

        coinTossFrame.pack()
        return coinTossFrame




    def _CreateBoard(self,widthOfWindow,heightOfWindow) -> Canvas:
        '''
        Tworzenie graficznej interpretacji pola gry, rysowany jest niebieski prostokat i wyciane sa z niego kola o bialum kolorze
        :param widthOfWindow: szerokosc rysowanego prostokata
        :param heightOfWindow:  wysokosc rysowanego prostokata
        :return: obiekt pola gry do pozniejszej obslugi
        '''
        boardGraphical = Canvas(self._mainWindow,width = widthOfWindow, height = heightOfWindow, bg = "blue")
        boardGraphical.pack()

        for coinsForColums in range(0, self._logic.NumberOfCols):
            for coinsForRows in range(0, self._logic.NumberOfRows):
                coord = (coinsForColums*100,coinsForRows*100,coinsForColums*100 +100,coinsForRows*100 +100)
                l = boardGraphical.create_oval(coord, fill = "white")

        return boardGraphical


    def DropCoin(self,columnToDropCoin):
        '''
        Upuszczenie monety do wybranej kolumny, wykorzystywane przy grze bez komputera
        :param columnToDropCoin: kolumna do ktorej zostanie upuszczona moneta, 1-pierwsza kolumna
        :return:
        '''
        self.BlockButtonsForDroppingCoins() #zablokowanie przyciskow do upuszczania monet

        try:
            self._logic.DropCoin(columnToDropCoin) #wrzuceinie monety do kolumny
        except Errors.FullColumnException: #sprawdzenie czy kolumna jest pelna
            self.PopupFullColumn()
            return
        except Errors.FullGameBoardException: #sprawdzenie czy wykonano ostatni ruch
            self._endGameWithTie = True

        self.AnimateDropingCoin(columnToDropCoin) #animacja spadajacej monety
        self.PrintCoins()   #narysowanie aktualnej pozycji monet na planszy

        self._logic.CheckWin() #sprawdzenie czy ktos wygral
        if self._logic.WhoWins() == 1 or self._logic.WhoWins() == 2:
            win = self.PopupForWinner()
            self._mainWindow.wait_window(win)
            return

        if self._endGameWithTie == True: #sprawdzenie czy jest remis
            full = self.PopupFullGameBoard()
            self._mainWindow.wait_window(full)
            return

        self._logic.ChangeActivePlayer() #zmiana aktywnego gracza

        self._header.winfo_children()[1].configure(text = "Tura Gracza " + str(self._logic.ActivePlayer),
                                                   bg = self._logic.ColorOfActivePlayer)

        self.ChangeColorOfCoinsInHeader()
        self.UnlockButtonsForDroppingCoins() #odblokowanie mozliwosci upuszczenia monet

    def DropCoinAI(self):
        '''
        Upuszczenie monety do wybranej kolumny, wykorzystywane przy grze z komputerem
        :return:
        '''
        aiWillDropCoinAtColumn = self._logic.AiMove() #obliczenie kolumny do ktorej komputer wrzuci monete
        self.BlockButtonsForDroppingCoins()

        try:
            self._logic.DropCoin(aiWillDropCoinAtColumn) #wrzucenie monety do kolumny
        except Errors.FullGameBoardException: #sprawdzenie czy wykonano ostatni ruch
            self._endGameWithTie = True

        self.AnimateDropingCoin(aiWillDropCoinAtColumn) #animacja spadajacej monety
        self.PrintCoins() #narysowanie aktualnej pozycji monet na planszy

        self._logic.CheckWin() #sprawdzenie czy ktos wygral
        if self._logic.WhoWins() == 1 or self._logic.WhoWins() == 2:
            win = self.PopupForWinner()
            self._mainWindow.wait_window(win)
            return

        if self._endGameWithTie == True: #sprawdzenie czy jest remis
            full = self.PopupFullGameBoard()
            self._mainWindow.wait_window(full)
            return

        self._logic.ChangeActivePlayer() #zmiana aktywnego gracza

        self._header.winfo_children()[1].configure(text="Tura Gracza " + str(self._logic.ActivePlayer),
                                                   bg=self._logic.ColorOfActivePlayer)

        self.ChangeColorOfCoinsInHeader()
        self.UnlockButtonsForDroppingCoins() #odblokowanie mozliwosci upuszczenia monet






    def BlockButtonsForDroppingCoins(self):
        '''
        Zablokowanie przyciskow do upuszczania monet
        :return:
        '''
        for child in self._barToDropCoins.winfo_children():
            child.configure(state='disable')

    def UnlockButtonsForDroppingCoins(self):
        '''
        Odblokowanie mozliwosci upuszczania monet
        :return:
        '''
        for child in self._barToDropCoins.winfo_children():
            child.configure(state='normal')


    def ChangeColorOfCoinsInHeader(self):
        '''
        Zmiana koloru przyciskow do upuszczania monet
        :return:
        '''
        for numberOfButtons in range(0, self._logic.NumberOfCols):
            if self._logic.ActivePlayer == 1:
                self._barToDropCoins.winfo_children()[numberOfButtons].configure(image = self._image1)
            else:
                self._barToDropCoins.winfo_children()[numberOfButtons].configure(image = self._image2)


    def PrintCoins(self):
        '''
        Narysowanie na planszy monet wedlug tablicy przekazanej z modulu logicznego
        :return:
        '''
        iter = 0 #wspolrzene y do rysowania monet
        iter2= 0 #wpolrzedne x do rysowania monet

        '''
        monety rysowane sa od gory pola gry a wedlug modulu logicznego pierwsza lista jest dolem pola gry dlatego rysuje po liscie od tylu
        '''
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
        '''
        Animacja opadajacych monet
        :param column: Kolumna do ktorej upuszczane sa monety, 1-pierwsza kolumna
        :return:
        '''
        iter = 0 #wwspolrzedna y aktualiujaca sie wraz z opadaniem monety
        for eachRow in self._logic.Board[::-1]:
            if eachRow[column-1] is not None:
                coordStart = ((column-1) * 100, 0, ((column-1) * 100) + 100, 100)
                coin = self._board.create_oval(coordStart, fill = self._logic.ColorOfActivePlayer)

                for elem in range(0, iter * 100):
                    self._board.move(coin, 0, 1)
                    self._mainWindow.update()
                break
            iter += 1

    def PopupForWinner(self):
        '''
        Okno pojawiajace sie w przypadku wygranej ktoregos gracza
        :return:
        '''
        top = Toplevel(width = 300, height = 100, bg = self._logic.ColorOfActivePlayer)
        top.resizable(0,0)
        top.title("Wygrana")
        congrats = Label(top, text = "Wygrał Gracz "  + str(self._logic.WhoWins()), font = ("Arial",31),
                         bg = self._logic.ColorOfActivePlayer)
        congrats.place(x=0, y=0)
        okButton =  Button(top,text = "Zakończ" , command = lambda:[top.destroy(),self.Restart()] )
        okButton.place(x=125,y=60)

    def PopupFullColumn(self):
        '''
        Okno pojawiajace sie gdy wrzuci sie monete do pelnej kolumny
        :return:
        '''
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
        '''
        Okno wyswietlajace sie w przypadku zapelnienia planszy/remisu
        :return:
        '''

        windowForTie = Toplevel(width = 300, height = 100, bg = "blue" )
        windowForTie.resizable(0,0)
        windowForTie.title("Remis")
        tieLabel = Label(windowForTie, text = "Remis " ,font = ("Arial",31),
                         bg = "blue"  )
        tieLabel.place(x=80, y=0)
        okButton =  Button(windowForTie,text = "Zakończ" , command = lambda:[windowForTie.destroy(),self.Restart()] )
        okButton.place(x=125,y=60)


    def Restart(self):
        '''
        Restartowanie pola gry i wywolywanie aktualnie wybranego trybu
        :return:
        '''
        self._board.destroy()
        self._barToDropCoins.destroy()
        self._header.destroy()

        if self._gameMode == "Klasyczna":
            self.GraphicForClassicGame()
        elif self._gameMode == "Pięć w rzędzie":
            self.GraphicsForFiveInARow()
        elif self._gameMode == "Gra z Komputerem":
            self.GraphicsForPlayWithAi()











