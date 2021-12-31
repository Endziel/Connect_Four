import random



from Errors import *


class MainLogic:
    def __init__(self,numberOfCols,numberOfRows):
        self._numberOfRows = numberOfRows
        self._numberOfCols = numberOfCols
        self._gameBoard = [[None for kolumny in range(self._numberOfCols)] for wiersze in range(self._numberOfRows)]
        self._whosTurn = None
        self._winner = None
        self._colorOfActivePlayer = None





    def WhoStarts(self):
        return random.randint(1,2)

    def WhoWins(self):
        pass



class StandardRules(MainLogic):
    def __init__(self,numberOfCols,numberOfRows):
        super().__init__(numberOfCols,numberOfRows)
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

    def colorOfActivePlayer(self):
        return self._colorOfActivePlayer

    def Board(self):
        return self._gameBoard


    def ActivePlayer(self):
        return self._whosTurn

    def ChangeActivePlayer(self):
        if self._whosTurn == 1:
            self._whosTurn = 2
            self._colorOfActivePlayer = "yellow"
        else:
            self._whosTurn = 1
            self._colorOfActivePlayer = "red"






    def DropCoin(self,column):
        if self._gameBoard[self._numberOfRows-1][column-1] is None:
            for rows in self._gameBoard:
                if rows[column-1] is None:
                    rows[column-1] = self._whosTurn
                    self._numberOfMovesInGame += 1
                    if self._IsTie():
                        raise FullGameBoardException("Limit ruchow wyczerpany")
                    break
                else:
                    continue
        else:
            raise FullColumnException("Ta kolumna jest pełna")

    def _IsTie(self):
        return self._numberOfMovesInGame == self._numberOfRows * self._numberOfCols

    def WhoWins(self):
        if self._winner is not None:
            return self._winner
        else:
            return 0


    def _CheckWinHorizontally(self,board):
        maxConnectedByFirstPlayer = 0
        maxConnectedBySecondPlayer = 0
        for oneRow in board:
            for oneElem in oneRow:
                if oneElem == 1:
                    maxConnectedByFirstPlayer +=1
                    maxConnectedBySecondPlayer = 0
                    if maxConnectedByFirstPlayer >= 4:
                        self._winner = 1
                if oneElem == 2:
                    maxConnectedByFirstPlayer = 0
                    maxConnectedBySecondPlayer += 1
                    if maxConnectedBySecondPlayer >= 4:
                        self._winner = 2
                if oneElem is None:
                    maxConnectedByFirstPlayer = 0
                    maxConnectedBySecondPlayer = 0
            maxConnectedByFirstPlayer = 0
            maxConnectedBySecondPlayer = 0

    def _CheckWinVertially(self):
        flippedGameBoard = [[x[y] for x in self._gameBoard] for y in range(len(self._gameBoard) +1)]
        # for elem in flippedGameBoard:
        #     print(elem)
        # print()
        self._CheckWinHorizontally(flippedGameBoard)




    def CheckWinDiagonally(self):
        fdiag = [[] for forwardDiag in range(self.numberOfRows + self.numberOfCols - 1)]
        bdiag = [[] for backDiag in range(len(fdiag))]
        min_bdiag = self.numberOfRows + 1

        for x in range(self.numberOfCols):
            for y in range(self.numberOfRows):
                fdiag[x + y].append(self._gameBoard[y][x])
                bdiag[x - y - min_bdiag].append(self._gameBoard[y][x])

        # print(fdiag)
        # print(bdiag)

        self._CheckWinHorizontally(fdiag)
        self._CheckWinHorizontally(bdiag)



    def CheckWin(self):
        self._CheckWinHorizontally(self._gameBoard)
        self._CheckWinVertially()
        self.CheckWinDiagonally()



















test = StandardRules(7,6)
#print('\n'.join([str(lst) for lst in test._gameBoard]))
test.DropCoin(1)
test.DropCoin(2)
test.DropCoin(3)
test.DropCoin(4)
test.DropCoin(1)
test.DropCoin(2)
test.DropCoin(2)


for elem in test._gameBoard[::-1]:
    print(elem)
#
#print(test.IsTie())




