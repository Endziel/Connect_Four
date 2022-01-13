import random
from Errors import *
import AI


class MainLogic:
    def __init__(self,numberOfCols,numberOfRows):
        self._numberOfRows = numberOfRows
        self._numberOfCols = numberOfCols
        self._gameBoard = [[None for kolumny in range(self._numberOfCols)] for wiersze in range(self._numberOfRows)]
        self._whosTurn = None
        self._winner = None
        self._colorOfActivePlayer = None
        self._numberOfConnectedToWin = None
        self._nextTurnNumberGen = self.GenerateTurnNumber()
        self._nrOfTurn = None


    def WhoStarts(self):
        return random.randint(1,2)

    def WhoWins(self):
        pass

    def DropCoin(self,column):
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
        if self._whosTurn == 1:
            self._whosTurn = 2
            self._colorOfActivePlayer = "yellow"
        else:
            self._whosTurn = 1
            self._colorOfActivePlayer = "red"

    def _IsTie(self):
        return self._nrOfTurn == self._numberOfRows * self._numberOfCols

    def GenerateTurnNumber(self):
        for turnNr in range(1,(self._numberOfRows*self._numberOfCols)+1):
            yield turnNr


    def _CheckWinHorizontally(self,board):
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
        flippedGameBoard = [[x[y] for x in self._gameBoard] for y in range(0,self._numberOfCols)]
        self._CheckWinHorizontally(flippedGameBoard)

    def _CheckWinDiagonally(self):
        fdiag = [[] for forwardDiag in range(self.numberOfRows + self._numberOfCols - 1)]
        bdiag = [[] for backDiag in range(len(fdiag))]
        min_bdiag = self._numberOfRows + 1

        for x in range(self._numberOfCols):
            for y in range(self._numberOfRows):
                fdiag[x + y].append(self._gameBoard[y][x])
                bdiag[x - y - min_bdiag].append(self._gameBoard[y][x])

        self._CheckWinHorizontally(fdiag)
        self._CheckWinHorizontally(bdiag)


    def CheckWin(self):
        self._CheckWinHorizontally(self._gameBoard)
        self._CheckWinVertially()
        self._CheckWinDiagonally()

class StandardRules(MainLogic):
    def __init__(self):
        super().__init__(7,6)
        self._whosTurn = self.WhoStarts();
        self.ChangeActivePlayer()
        self._numberOfMovesInGame = 0
        self._numberOfConnectedToWin = 4

    @property
    def numberOfCols(self):
        return self._numberOfCols

    @property
    def numberOfRows(self):
        return self._numberOfRows

    @property
    def WhoW(self):
        return self._whoWins
    @property
    def colorOfActivePlayer(self):
        return self._colorOfActivePlayer
    @property
    def Board(self):
        return self._gameBoard

    @property
    def ActivePlayer(self):
        return self._whosTurn

    def WhoWins(self):
        if self._winner is not None:
            return self._winner
        else:
            return 0




class FiveInARow(MainLogic):
    def __init__(self):
        super().__init__(9,6)
        self._numberOfMovesInGame = 0
        self._whosTurn = self.WhoStarts();
        for i in range(0,self._numberOfRows):
            self.DropCoin(1)
            self.ChangeActivePlayer()
            self._numberOfMovesInGame += 1
        for i in range(0,self._numberOfRows):
            self.DropCoin(9)
            self.ChangeActivePlayer()
            self._numberOfMovesInGame += 1
        self.ChangeActivePlayer()
        self._numberOfConnectedToWin = 5

    @property
    def numberOfCols(self):
        return self._numberOfCols

    @property
    def numberOfRows(self):
        return self._numberOfRows

    @property
    def WhoW(self):
        return self._whoWins

    @property
    def colorOfActivePlayer(self):
        return self._colorOfActivePlayer
    @property
    def Board(self):
        return self._gameBoard

    @property
    def ActivePlayer(self):
        return self._whosTurn

    def WhoWins(self):
        if self._winner is not None:
            return self._winner
        else:
            return 0

class PlayWithAI(MainLogic):
    def __init__(self):
        super().__init__(7, 6)
        self._whosTurn = self.WhoStarts();
        self.ChangeActivePlayer()
        self._numberOfMovesInGame = 0
        self._numberOfConnectedToWin = 4
        self._ai = AI.AI(random.choice([1,2]))


    @property
    def numberOfCols(self):
        return self._numberOfCols

    @property
    def numberOfRows(self):
        return self._numberOfRows

    @property
    def WhoW(self):
        return self._whoWins

    @property
    def colorOfActivePlayer(self):
        return self._colorOfActivePlayer

    @property
    def Board(self):
        return self._gameBoard

    @property
    def ActivePlayer(self):
        return self._whosTurn

    def AiMove(self):
        return self._ai.PickbestMove(self._gameBoard)

    def WhoWins(self):
        if self._winner is not None:
            return self._winner
        else:
            return 0






