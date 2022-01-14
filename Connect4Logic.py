import random
from Errors import *
import AI


class MainLogic:
    '''
    Klasa odpowiedzialna za glowna logige do gry Connect4
    '''
    def __init__(self,numberOfCols,numberOfRows):
        self._numberOfRows = numberOfRows             #ilosc wierszy w planszy
        self._numberOfCols = numberOfCols          #ilosc kolumn w planszy
        self._gameBoard = [[None for kolumny in range(self._numberOfCols)] for wiersze in range(self._numberOfRows)]    #utworzenie pola gry
        self._whosTurn = None
        self._winner = None                 #ustawiane gdy ktorys gracz wygra
        self._colorOfActivePlayer = None        #kolor aktywnego gracza
        self._numberOfConnectedToWin = None         #wymagana ilosc polaczonych monet do wygrania gry
        self._nextTurnNumberGen = self.GenerateTurnNumber()     #generator do zwracania aktualnego numery tury
        self._nrOfTurn = None


    def WhoStarts(self):
        '''
        Losowanie zaczynajacego gracza
        :return: 1 lub 2
        '''
        return random.randint(1,2)

    def WhoWins(self):
        '''
        funkcja wirtualna do sprawdzenia czy jest juz zwyciezca
        :return:
        '''
        raise NotImplementedError('nie zaimplementowana funkcja WhoWins')

    @property
    def NumberOfCols(self):
        '''
        funkcja wirtualna do zwrocenia ilosci kolumn w grze
        :return:
        '''
        raise NotImplementedError('nie zaimplementowana funkcja numberOfCols')

    @property
    def NumberOfRows(self):
        '''
        funkcja wirtualna do zwrocenia ilosci wierszy w grze
        :return:
        '''
        raise NotImplementedError('nie zaimplementowana funkcja numberOfRows')

    @property
    def ColorOfActivePlayer(self):
        '''
        funkcja wirtualna do zwrocenia koloru aktywnego gracza
        :return:
        '''
        raise NotImplementedError('nie zaimplementowana funkcja colorOfActivePlayer')

    @property
    def Board(self):
        '''
        funkcja wirtualna do zwrocenia stanu planszy
        :return:
        '''
        raise NotImplementedError('nie zaimplementowana funkcja Board')

    @property
    def ActivePlayer(self):
        '''
        funkcja wirtualna do zwrocenia aktualnego gracza
        :return:
        '''
        raise NotImplementedError('nie zaimplementowana funkcja ActivePlayer')


    def DropCoin(self,column):
        '''
        obsluga monety spadajacej do wybranej kolumny
        :param column: kolumna do ktorej gracz probuje spuscic monete
        :return:
        '''
        if self._gameBoard[self._numberOfRows-1][column-1] is None:
            for rows in self._gameBoard:
                if rows[column-1] is None:
                    rows[column-1] = self._whosTurn
                    self._nrOfTurn =  next(self._nextTurnNumberGen)
                    if self._IsTie():
                        raise FullGameBoardException("Limit ruchow wyczerpany")
                    break
                else:
                    continue
        else:
            raise FullColumnException("Ta kolumna jest pełna")

    def ChangeActivePlayer(self):
        '''
        Zmiana aktywnego gracza na drugiego
        :return:
        '''
        if self._whosTurn == 1:
            self._whosTurn = 2
            self._colorOfActivePlayer = "yellow"
        else:
            self._whosTurn = 1
            self._colorOfActivePlayer = "red"

    def _IsTie(self) -> int:
        '''
        Sprawdzenie czy wyczerpano wszystkie ruchy w grze
        :return:
        '''
        return self._nrOfTurn == self._numberOfRows * self._numberOfCols

    def GenerateTurnNumber(self):
        '''
        Generator numeru kolejnej tury
        :return:
        '''
        for turnNr in range(1,(self._numberOfRows*self._numberOfCols)+1):
            yield turnNr


    def _CheckWinHorizontally(self,board):
        '''
        Sprawdzenie czy podana plansza posiada wygrywajaca konfiguracje horyzontalnie
        :param board: plansza do sprawdzenia
        :return:
        '''
        maxConnectedByFirstPlayer = 0
        maxConnectedBySecondPlayer = 0
        for oneRow in board:
            for oneElem in oneRow:
                if oneElem == 1:
                    maxConnectedByFirstPlayer +=1
                    maxConnectedBySecondPlayer = 0
                    if maxConnectedByFirstPlayer >= self._numberOfConnectedToWin:
                        self._winner = 1
                if oneElem == 2:
                    maxConnectedByFirstPlayer = 0
                    maxConnectedBySecondPlayer += 1
                    if maxConnectedBySecondPlayer >= self._numberOfConnectedToWin:
                        self._winner = 2
                if oneElem is None:
                    maxConnectedByFirstPlayer = 0
                    maxConnectedBySecondPlayer = 0
            maxConnectedByFirstPlayer = 0
            maxConnectedBySecondPlayer = 0



    def _CheckWinVertially(self):
        '''
        Transpozycja planszy i sprawdzenie jej horyzontalnie
        :return:
        '''
        flippedGameBoard = [[x[y] for x in self._gameBoard] for y in range(0,self._numberOfCols)]
        self._CheckWinHorizontally(flippedGameBoard)

    def _CheckWinDiagonally(self):
        '''
        Wyciagniecie diagonali z planszy jako linie i sprawdzenie ich jako horyzontalne
        :return:
        '''
        fdiag = [[] for forwardDiag in range(self.NumberOfRows + self._numberOfCols - 1)]
        bdiag = [[] for backDiag in range(len(fdiag))]
        min_bdiag = self._numberOfRows + 1

        for x in range(self._numberOfCols):
            for y in range(self._numberOfRows):
                fdiag[x + y].append(self._gameBoard[y][x])
                bdiag[x - y - min_bdiag].append(self._gameBoard[y][x])

        self._CheckWinHorizontally(fdiag)
        self._CheckWinHorizontally(bdiag)


    def CheckWin(self):
        '''
        Sprawdzenie planszy czy wystapila wygrywajaca konfiguracja
        :return:
        '''
        self._CheckWinHorizontally(self._gameBoard)
        self._CheckWinVertially()
        self._CheckWinDiagonally()

class StandardRules(MainLogic):
    '''
    Klasa odpowiedzialna za podstawowa wersje gry, Connect 4, dwoch graczy
    '''
    def __init__(self):
        super().__init__(7,6) #plansza 7 wierszy, 6 kolumn
        self._whosTurn = self.WhoStarts();
        self.ChangeActivePlayer()
        self._numberOfMovesInGame = 0
        self._numberOfConnectedToWin = 4

    @property
    def NumberOfCols(self) -> int:
        '''
        getter liczby kolumn planszy
        :return: liczba kolumn planszy
        '''
        return self._numberOfCols

    @property
    def NumberOfRows(self) -> int:
        '''
        getter liczby wierszy planszy
        :return: liczba wierszy planszy
        '''
        return self._numberOfRows

    @property
    def ColorOfActivePlayer(self) -> str:
        '''
        getter koloru aktywnego gracza
        :return: kolor aktywnego gracza
        '''
        return self._colorOfActivePlayer

    @property
    def Board(self) -> list:
        '''
        getter stanu planszy
        :return: lista list ze stanem pol, 1-monety gracza pierwszego, 2 - monety gracza drugiego, None - wolne pole
        '''
        return self._gameBoard

    @property
    def ActivePlayer(self) -> int:
        '''
        getter aktywnego gracza
        :return: numer aktywnego gracza
        '''
        return self._whosTurn

    def WhoWins(self) -> int:
        '''
        getter numeru zwycieskiego gracza
        :return: numer zwycieskiego gracza, 0 jesli nie ma jeszcze zwyciezcy
        '''
        if self._winner is not None:
            return self._winner
        else:
            return 0




class FiveInARow(MainLogic):
    '''
    Klasa odpowiedzialna za wersje gry z wieksza plansza 9x6
    '''
    def __init__(self):
        super().__init__(9,6)           #utworzenie planszy 9 kolumn na 6 wierszy
        self._numberOfMovesInGame = 0
        self._whosTurn = self.WhoStarts();
        for i in range(0,self._numberOfRows):   #zapelnienie pierwszej kolumny monetami
            self.DropCoin(1)
            self.ChangeActivePlayer()
            self._numberOfMovesInGame += 1
        for i in range(0,self._numberOfRows):   #zapelnienie ostatniej kolumny moentami
            self.DropCoin(9)
            self.ChangeActivePlayer()
            self._numberOfMovesInGame += 1
        self.ChangeActivePlayer()
        self._numberOfConnectedToWin = 5

    @property
    def NumberOfCols(self) -> int:
        '''
        getter liczby kolumn planszy
        :return: liczba kolumn planszy
        '''
        return self._numberOfCols

    @property
    def NumberOfRows(self) -> int:
        '''
        getter liczby wierszy planszy
        :return: liczba wierszy planszy
        '''
        return self._numberOfRows

    @property
    def ColorOfActivePlayer(self) -> str:
        '''
        getter koloru aktywnego gracza
        :return: kolor aktywnego gracza
        '''
        return self._colorOfActivePlayer

    @property
    def Board(self) -> list:
        '''
        getter stanu planszy
        :return: lista list ze stanem pol, 1-monety gracza pierwszego, 2 - monety gracza drugiego, None - wolne pole
        '''
        return self._gameBoard

    @property
    def ActivePlayer(self) -> int:
        '''
        getter aktywnego gracza
        :return: numer aktywnego gracza
        '''
        return self._whosTurn

    def WhoWins(self) -> int:
        '''
        getter numeru zwycieskiego gracza
        :return: numer zwycieskiego gracza, 0 jesli nie ma jeszcze zwyciezcy
        '''
        if self._winner is not None:
            return self._winner
        else:
            return 0


class PlayWithAI(MainLogic):
    '''
    Klasa odpowiedzialna za werjse gry z graczem komputerowym
    '''
    def __init__(self):
        super().__init__(7, 6)  #utowrzenie planszy 7 kolumn na 6 wierszy
        self._whosTurn = self.WhoStarts();
        self._ai = AI.AI(self._whosTurn)    #utworzenie obiektu gracza komputerowego i przypisanie mu nr gracza

        self.ChangeActivePlayer()
        self._numberOfMovesInGame = 0
        self._numberOfConnectedToWin = 4

    def AiMove(self):
        '''
        Wywolanie algorytmu gracza komputerowego do wykonania przez niego ruchu
        :return: kolumna do ktorej gracz komputerowy wrzuci monete, 1 - pierwsza kolumna
        '''
        return self._ai.PickbestMove(self._gameBoard)


    @property
    def NumberOfCols(self) -> int:
        '''
        getter liczby kolumn planszy
        :return: liczba kolumn planszy
        '''
        return self._numberOfCols

    @property
    def NumberOfRows(self) -> int:
        '''
        getter liczby wierszy planszy
        :return: liczba wierszy planszy
        '''
        return self._numberOfRows

    @property
    def ColorOfActivePlayer(self) -> str:
        '''
        getter koloru aktywnego gracza
        :return: kolor aktywnego gracza
        '''
        return self._colorOfActivePlayer

    @property
    def Board(self) -> list:
        '''
        getter stanu planszy
        :return: lista list ze stanem pol, 1-monety gracza pierwszego, 2 - monety gracza drugiego, None - wolne pole
        '''
        return self._gameBoard

    @property
    def ActivePlayer(self) -> int:
        '''
        getter aktywnego gracza
        :return: numer aktywnego gracza
        '''
        return self._whosTurn

    def WhoWins(self) -> int:
        '''
        getter numeru zwycieskiego gracza
        :return: numer zwycieskiego gracza, 0 jesli nie ma jeszcze zwyciezcy
        '''
        if self._winner is not None:
            return self._winner
        else:
            return 0





