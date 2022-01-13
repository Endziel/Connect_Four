import math
import random

import Connect4Logic
import copy


class AI:
    def __init__(self,playerNr):
        self._iAmPlayerNr = playerNr
        self._otherPlayerNr = self.OtherPlayerNr()
        self._numberOfConnectedToWin = 4
        self._numberOfCols = 7
        self._numberOfRows = 6
        self._recursionValue = 6

    def OtherPlayerNr(self):
        if self._iAmPlayerNr == 1:
            return 2
        else:
            return 1


    def _CheckWinHorizontally(self, board):
        maxConnectedByFirstPlayer = 0
        maxConnectedBySecondPlayer = 0
        for oneRow in board:
            for oneElem in oneRow:
                if oneElem == 1:
                    maxConnectedByFirstPlayer += 1
                    maxConnectedBySecondPlayer = 0
                    if maxConnectedByFirstPlayer >= self._numberOfConnectedToWin:
                        return 1
                if oneElem == 2:
                    maxConnectedByFirstPlayer = 0
                    maxConnectedBySecondPlayer += 1
                    if maxConnectedBySecondPlayer >= self._numberOfConnectedToWin:
                        return  2
                if oneElem is None:
                    maxConnectedByFirstPlayer = 0
                    maxConnectedBySecondPlayer = 0
            maxConnectedByFirstPlayer = 0
            maxConnectedBySecondPlayer = 0
        else:
            return 0

    def _CheckWinVertially(self,board):
        flippedGameBoard = [[x[y] for x in board] for y in range(0, self._numberOfCols)]
        return self._CheckWinHorizontally(flippedGameBoard)

    def _CheckWinDiagonally(self,board):
        fdiag = [[] for forwardDiag in range(self._numberOfRows + self._numberOfCols - 1)]
        bdiag = [[] for backDiag in range(len(fdiag))]
        min_bdiag = self._numberOfRows + 1

        for x in range(self._numberOfCols):
            for y in range(self._numberOfRows):
                fdiag[x + y].append(board[y][x])
                bdiag[x - y - min_bdiag].append(board[y][x])

        fowardDiag = self._CheckWinHorizontally(fdiag)
        backDiag =  self._CheckWinHorizontally(bdiag)
        return(fowardDiag,backDiag)

    def CheckWin(self,board):
        winH= self._CheckWinHorizontally(board)
        winV = self._CheckWinVertially(board)
        winFd,winBd = self._CheckWinDiagonally(board)
        for isWinner in [winH,winV,winFd,winBd]:
            if isWinner != 0:
                return isWinner
        else:
            return 0

    def PointsGrantedByGoodPlay(self,connected,holes):
        if connected >= 4:
            return 100
        elif connected == 3 and holes >= 1:
            return  5
        elif connected == 2 and holes >= 2:
            return 2
        else:
            return 0

    def PointsGrantedByBadPlay(self,connected,holes):
        if connected >= 4:
            return -100
        elif connected == 3 and holes >= 1:
            return  -4
        else:
            return 0

    def EvaluateLine(self,list):
        maxConnectedByAi = 0
        tempMaxConnect = 0
        maxConnectedbyOpponent = 0
        holes = 0
        score = 0
        for elem in list:
            if elem == self._iAmPlayerNr:
                tempMaxConnect += 1

            elif elem == self._otherPlayerNr:
                tempMaxConnect = 0
                score += self.PointsGrantedByGoodPlay(maxConnectedByAi,holes)
                holes = 0

            elif elem == None:
                holes += 1
                if tempMaxConnect > maxConnectedByAi:
                    maxConnectedByAi = tempMaxConnect
                tempMaxConnect = 0
        else:
            score += self.PointsGrantedByGoodPlay(maxConnectedByAi, holes)

        tempMaxConnect = 0
        holes = 0
        for elem in list:
            if elem == self._otherPlayerNr:
                tempMaxConnect += 1

            elif elem == self._iAmPlayerNr:
                tempMaxConnect = 0
                score += self.PointsGrantedByBadPlay(maxConnectedbyOpponent, holes)
                holes = 0

            elif elem == None:
                holes += 1
                if tempMaxConnect > maxConnectedbyOpponent:
                    maxConnectedbyOpponent = tempMaxConnect
                tempMaxConnect = 0
        else:
            score += self.PointsGrantedByBadPlay(maxConnectedbyOpponent, holes)

        return score



    def EvaluateBoard(self,board):
        score = 0
        for row in board:
            score += self.EvaluateLine(row)
        flippedGameBoard = [[x[y] for x in board] for y in range(0, self._numberOfCols)]

        for newRow in flippedGameBoard:
            score += self.EvaluateLine(newRow)

        fdiag = [[] for forwardDiag in range(self._numberOfRows + self._numberOfCols - 1)]
        bdiag = [[] for backDiag in range(len(fdiag))]
        min_bdiag = self._numberOfRows + 1

        for x in range(self._numberOfCols):
            for y in range(self._numberOfRows):
                fdiag[x + y].append(board[y][x])
                bdiag[x - y - min_bdiag].append(board[y][x])

        for forwardD in fdiag:
            score += self.EvaluateLine(forwardD)
        for backD in bdiag:
            score += self.EvaluateLine(backD)
        return score



    def CheckFirstFreeSlotToDropCoin(self,actualColumn,board,actualRow):
        if board[actualRow][actualColumn] is None:
            return (actualRow,actualColumn)
        elif actualRow >= 5:
            return
        else:
            return self.CheckFirstFreeSlotToDropCoin(actualColumn,board,actualRow+1)



    def PossibleMoves(self,board):
        listOfPossibleMoves = []
        for bottomRowIter in range(0,self._numberOfCols):
            if board[0][bottomRowIter] is None:
                listOfPossibleMoves.append((0,bottomRowIter))
            else:
                possibleMove = self.CheckFirstFreeSlotToDropCoin(bottomRowIter,board,1)
                if possibleMove is not None:
                    row,column = possibleMove
                    listOfPossibleMoves.append((row,column))
        return listOfPossibleMoves



    def MaxAlphaBeta(self,board,recursiveDepth,alpha,beta):
        result = self.CheckWin(board)
        if result == self._iAmPlayerNr:
            return (None, 100000)
        elif result == self._otherPlayerNr:
            return (None, -100000)
        elif recursiveDepth == 0:
            return (None, self.EvaluateBoard(board))

        value = -math.inf
        possibleMoves = self.PossibleMoves(board)
        maxColumn = random.choice(possibleMoves)
        for move in possibleMoves:
            rowCoord,colCoord = move
            updatedBoard = copy.deepcopy(board)
            updatedBoard[rowCoord][colCoord] = self._iAmPlayerNr
            newScore = self.MinAlphaBeta(updatedBoard,recursiveDepth-1,alpha,beta)[1]
            if newScore > value:
                value = newScore
                maxColumn = colCoord
            alpha = max(alpha,value)
            if alpha >= beta:
                break
        return maxColumn,value




    def MinAlphaBeta(self,board,recursiveDepth,alpha,beta):
        result = self.CheckWin(board)
        if result == self._iAmPlayerNr:
            return (None, 100000)
        elif result == self._otherPlayerNr:
            return (None, -100000)
        elif recursiveDepth == 0:
            return (None, self.EvaluateBoard(board))

        value = math.inf
        possibleMoves = self.PossibleMoves(board)
        minColumn = random.choice(possibleMoves)
        for move in possibleMoves:
            rowCoord, colCoord = move
            updatedBoard = copy.deepcopy(board)
            updatedBoard[rowCoord][colCoord] = self._otherPlayerNr
            newScore = self.MaxAlphaBeta(updatedBoard, recursiveDepth - 1, alpha, beta)[1]
            if newScore < value:
                value = newScore
                minColumn = colCoord
            beta = min(beta, value)
            if alpha >= beta:
                break
        return minColumn, value

    def PickbestMove(self,board):
        bestMove = self.MaxAlphaBeta(board,7,-math.inf,math.inf)
        print(bestMove)
        return bestMove[0]+1

        # if bestMove[1] > 0:
        #     return bestMove[0]+1
        # else:
        #     return random.choice(self.PossibleMoves(board))[0]+1

        # possibleMoves = self.PossibleMoves(board)
        # for move in possibleMoves:
        #     row,col = move
        #     updatedBoard = copy.deepcopy(board)
        #     updatedBoard[row][col] = self._iAmPlayerNr
        #     print(self.MaxAlphaBeta(updatedBoard,6,-math.inf,math.inf))



if __name__ == '__main__':




    ai = AI(1)
    gameBoard = [[None for kolumny in range(7)] for wiersze in range(6)]
    # for elem in gameBoard:
    #     print(elem)
    #
    # print(ai.CheckWin(gameBoard))
    #
    gameBoard[0][0] = 1
    gameBoard[0][1] = 1
    gameBoard[0][3] = 1
    gameBoard[0][4] = 1
    gameBoard[0][5] = 1
    gameBoard[1][0] = 1
    gameBoard[1][1] = 1
    gameBoard[0][6] = 1



    gameBoard[2][0] = 1


    # #gameBoard[0][3] = 1
    # gameBoard[1][0] = 1
    # gameBoard[2][0] = 2
    # gameBoard[3][0] = 1
    # gameBoard[4][0] = 2
    # gameBoard[5][0] = 1

    diagonalGameBoard = [
        [2,1,None,None,None,1,1],
        [2,None,None,None,None,None,None],
        [2,None,None,None,None,None,None],
        [1,None,None,None,None,None,None],
        [None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None]
    ]
    for elem in gameBoard:
        print(elem)

    # # print(ai.CheckWin(gameBoard))
    # print(ai.PossibleMoves(gameBoard))
    # #print(ai.max(gameBoard))
    # print(ai.EvaluateBoard(diagonalGameBoard))
    # # line = [None,1,1,None,1,1,1]
    # # print(ai.EvaluateLine(line))
    #print(ai.MaxAlphaBeta(diagonalGameBoard,6,-math.inf,math.inf))
    print(ai.PickbestMove(diagonalGameBoard))

