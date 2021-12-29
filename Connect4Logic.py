import random


from Errors import *


class MainLogic:
    def __init__(self,numberOfCols,numberOfRows):
        self._numberOfRows = numberOfRows
        self._numberOfCols = numberOfCols
        self._gameBoard = [[None for kolumny in range(self._numberOfCols)] for wiersze in range(self._numberOfRows)]
        self._whosTurn = None
        self._whoWins = None





    def WhoStarts(self):
        return random.randint(1,2)

    def WhoWins(self,playerNumber):
        pass



class StandardRules(MainLogic):
    def __init__(self,numberOfCols,numberOfRows):
        super().__init__(numberOfCols,numberOfRows)
        self._whosTurn = self.WhoStarts();
        self._numberOfMovesInGame = 0
        self._numberOfConnectedToWin = 4

    def ChangeActivePlayer(self):
        if self._whosTurn == 1:
            self._whosTurn = 2
        else:
            self._whosTurn = 1

    def DropCoin(self,column):
        if self._gameBoard[self._numberOfRows-1][column-1] is None:
            for rows in self._gameBoard:
                if rows[column-1] is None:
                    rows[column-1] = self._whosTurn
                    self._numberOfMovesInGame += 1
                    break
                else:
                    continue
        else:
            raise FullColumnException("Ta kolumna jest pełna")

    def IsTie(self):
        return self._numberOfMovesInGame == self._numberOfRows * self._numberOfCols

    def WhoWins(self, playerNumber):
        self._whoWins = playerNumber

    def CheckWinHorizontally(self):
        maxConnectedByFirstPlayer = 0
        maxConnectedBySecondPlayer = 0
        for oneRow in self._gameBoard:
            for oneElem in oneRow:
                if oneElem == 1:
                    maxConnectedByFirstPlayer +=1
                    maxConnectedBySecondPlayer = 0
                    if maxConnectedByFirstPlayer >= 4:
                        WhoWins(1)
                if oneElem == 2:
                    maxConnectedByFirstPlayer = 0
                    maxConnectedBySecondPlayer += 1
                    if maxConnectedByFirstPlayer >= 4:
                        WhoWins(2)
                if oneElem is None:
                    maxConnectedByFirstPlayer = 0
                    maxConnectedBySecondPlayer = 0


















test = StandardRules(7,6)
#print('\n'.join([str(lst) for lst in test._gameBoard]))
test.DropCoin(1)
test.DropCoin(2)
test.DropCoin(3)
test.DropCoin(4)
test.DropCoin(1)

for elem in test._gameBoard[::-1]:
    print(elem)
print(test._whoWins)
#print(test.IsTie())




