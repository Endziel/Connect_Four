import math
import random

import Connect4Logic
import copy


class AI:
    '''
    Klasa odpowiedzialna za ruch gracza komputerowego
    '''
    def __init__(self,playerNr):
        self._iAmPlayerNr = playerNr        #przypisanie graczowi komputerowemu numeru gracza
        self._otherPlayerNr = self.OtherPlayerNr()  #numer drugiego gracza
        self._numberOfConnectedToWin = 4
        self._numberOfCols = 7
        self._numberOfRows = 6
        self._recursionValue = 7            #liczba ruchow do przodu jaka bedzie przewidywal komputer

    def OtherPlayerNr(self) -> int:
        '''
        przypisanie graczowi ludzkiemu nr gracza
        :return: numer gracza niekomputerowego
        '''
        if self._iAmPlayerNr == 1:
            return 2
        else:
            return 1


    def _CheckWinHorizontally(self, board) -> int:
        '''
        Sprawdzenie podanej planszy czy w rzedach jest wygrywajaca konfiguracja
        :param board: plansza gry do sprawdzenia wierszy
        :return: nr gracza ktory wygral, 0- brak wygranego
        '''
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

    def _CheckWinVertially(self,board) -> int:
        '''
        Transpozycja podanej planszy i wywolanie sprawdzenia wygrywajacej kombinacji horyzontalnie
        :param board: plansza gry do sprawdzenia kolumn
        :return: nr gracza ktory wygral, 0- brak wygranego
        '''
        flippedGameBoard = [[x[y] for x in board] for y in range(0, self._numberOfCols)]
        return self._CheckWinHorizontally(flippedGameBoard)

    def _CheckWinDiagonally(self,board) -> tuple :
        '''
        Zapisanie diagonali planszy do list i i wywolanie sprawdzenia wygrywajacej kombinacji horyzontalnie
        :param board: plansza gry do sprawdzenia diagonali
        :return: nr gracza ktory wygral dla dwoch skosow diagonali, 0 - brak wygranego
        '''
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

    def CheckWin(self,board) -> int:
        '''
        Sprawdzenie czy podana plansza posiada wygrywajaca kombinacje
        :param board: plansza gry do sprawdzenia
        :return: numer zwycieskiego gracza, 0 - brak zwyciezcy
        '''
        winH= self._CheckWinHorizontally(board)
        winV = self._CheckWinVertially(board)
        winFd,winBd = self._CheckWinDiagonally(board)
        for isWinner in [winH,winV,winFd,winBd]:
            if isWinner != 0:
                return isWinner
        else:
            return 0

    def PointsGrantedByGoodPlay(self,connected,holes,actualRecursion) -> int:
        '''
        Punktacja planszy za dobra gre , premiowane sa wieksze polaaczenia i gdy sa one dostepne dla mniejszej liczby ruchow
        :param connected: ilosc polaczonych monet
        :param holes: ilosc wolnych pol przy polaczonych monetach
        :param actualRecursion: aktualna wartosc rekurencji, ile tur do przodu jest aktualna plansza
        :return: punkty przyznane za polaczenia na planszy
        '''
        if connected >= 4:
            return 100 *(self._recursionValue - actualRecursion +1)
        elif connected == 3 and holes >= 1:
            return  5 *(self._recursionValue - actualRecursion +1)
        elif connected == 2 and holes >= 2:
            return 2 *(self._recursionValue - actualRecursion +1)
        else:
            return 0

    def PointsGrantedByBadPlay(self,connected,holes,actualRecursion) -> int:
        '''
        Punktacja planszy za zla gre, liczone sa polaczenia utworzone przez przeciwnika
        :param connected: ilosc polaczonych monet przez przeciwnika
        :param holes:  ilosc wolnych pol obok polaczonych moent
        :param actualRecursion: aktualna wartosc rekurencji, ile tur do przodu jest aktualna plansza
        :return: punkty odjete za polaczenia na planszy przeciwnika
        '''
        if connected >= 4:
            return -100 *(self._recursionValue - actualRecursion +1)
        elif connected == 3 and holes >= 1:
            return  -4 *(self._recursionValue - actualRecursion +1)
        else:
            return 0

    def EvaluateLine(self,list,actualRecursion) -> int:
        '''
        Sprawdzenie jednego wiersza/linii o mozliwych monetach obok siebie i wolnych polach obok tych monet
        :param list: jeden wiersz/linia do sprawdzenia
        :param actualRecursion: aktualna wartosc rekurencji, ile tur do przodu jest aktualna plansza
        :return: punkty przyznane za dana linie
        '''
        maxConnectedByAi = 0    #maksymalna ilosc polaczonych monet w linii
        tempMaxConnect = 0      #ciag aktualnie sprawdzanych monet
        maxConnectedbyOpponent = 0
        holes = 0   #wolne pola obok monet
        score = 0   #wynik do zwrocenia
        for elem in list:   #liczenie dodatich punktow za gre komputera
            if elem == self._iAmPlayerNr: #ciag polaczonych monet
                tempMaxConnect += 1

            elif elem == self._otherPlayerNr: #przerwany ciag polaczonych monet, moneta przeciwnego gracza
                tempMaxConnect = 0
                score += self.PointsGrantedByGoodPlay(maxConnectedByAi,holes,actualRecursion)
                holes = 0

            elif elem == None:  #wolne pole w ktore mozna ustawic monete w przyszlosci
                holes += 1
                if tempMaxConnect > maxConnectedByAi:
                    maxConnectedByAi = tempMaxConnect
                tempMaxConnect = 0
        else:
            score += self.PointsGrantedByGoodPlay(maxConnectedByAi, holes,actualRecursion)

        tempMaxConnect = 0
        holes = 0
        for elem in list:   #liczenie ujemnych punktow za gre przeciwnika
            if elem == self._otherPlayerNr:     #ciag polaczonych monet przez przeciwnika
                tempMaxConnect += 1

            elif elem == self._iAmPlayerNr:     #przerwany ciag poloczonych monet przez przeciwnka
                tempMaxConnect = 0
                score += self.PointsGrantedByBadPlay(maxConnectedbyOpponent, holes,actualRecursion)
                holes = 0

            elif elem == None:  #wolne pole w ktore mozna ustawic monete w przyszlosci
                holes += 1
                if tempMaxConnect > maxConnectedbyOpponent:
                    maxConnectedbyOpponent = tempMaxConnect
                tempMaxConnect = 0
        else:
            score += self.PointsGrantedByBadPlay(maxConnectedbyOpponent, holes,actualRecursion)

        return score



    def EvaluateBoard(self,board,actualRecursion) -> int:
        '''
        Sprawdzenie podanej planszy gry w celu jej oceny punktowej
        :param board: badana plansza
        :param actualRecursion: aktualna wartosc rekurencji, ile tur do przodu jest aktualna plansza
        :return: punkty przyznane za dana plansze
        '''
        score = 0
        for row in board:
            score += self.EvaluateLine(row,actualRecursion)
        flippedGameBoard = [[x[y] for x in board] for y in range(0, self._numberOfCols)]

        for newRow in flippedGameBoard:
            score += self.EvaluateLine(newRow,actualRecursion)

        fdiag = [[] for forwardDiag in range(self._numberOfRows + self._numberOfCols - 1)]
        bdiag = [[] for backDiag in range(len(fdiag))]
        min_bdiag = self._numberOfRows + 1

        for x in range(self._numberOfCols):
            for y in range(self._numberOfRows):
                fdiag[x + y].append(board[y][x])
                bdiag[x - y - min_bdiag].append(board[y][x])

        for forwardD in fdiag:
            score += self.EvaluateLine(forwardD,actualRecursion)
        for backD in bdiag:
            score += self.EvaluateLine(backD,actualRecursion)
        return score



    def CheckFirstFreeSlotToDropCoin(self,actualColumn,board,actualRow) -> tuple:
        '''
        Szukanie w kolumnie pierwszego miejsca w ktorym mozna dodac monete, wywolanie rekurencyjnie dla kolejnych wierszy
        :param actualColumn: numer kolumny do zbadania
        :param board: badana plansza
        :param actualRow: aktualnie rekurencyjnie badany wiersz
        :return: wspolrzedne wiersz,kolumna w ktorym mozna umiescic moenete w kolejnym ruchu
        '''
        if board[actualRow][actualColumn] is None:
            return (actualRow,actualColumn)
        elif actualRow >= 5:
            return
        else:
            return self.CheckFirstFreeSlotToDropCoin(actualColumn,board,actualRow+1)



    def PossibleMoves(self,board) -> list:
        '''
        Zbadanie listy mozliwych ruchow dla podanej planszy
        :param board: badana plansza
        :return: lista krotek(wiersz,kolumna) mozliwych ruchow do wykonania
        '''
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



    def MaxAlphaBeta(self,board,recursiveDepth,alpha,beta) ->tuple:
        '''
        Czesc algorytmu MinMax alpha-beta pruning do badania najlepszego nastepnego ruchu, czesc max
        :param board: badana plansza
        :param recursiveDepth: aktualna wartosc rekurencji, ile tur do przodu jest aktualna plansza
        :param alpha: najwieksza znaleziona wartosc punktacji dla badanych dzieci
        :param beta: najmniejsza znaleziona wartosc punktacji(gracz przeciwny) dla badanych dzieci
        :return: nr kolumny do wrzucenia monety i jej wartosc punktowa na plus dla komputera
        '''
        result = self.CheckWin(board)
        if result == self._iAmPlayerNr: #aktualna plansza jest wygrana
            return (None, 100000)
        elif result == self._otherPlayerNr: #aktualna plasza jest przegrana
            return (None, -100000)
        elif recursiveDepth == 0:   #aktualna plansza nie ma jednonacznego wyniku i trzeba ja spuntkowac
            return (None, self.EvaluateBoard(board,self._recursionValue - recursiveDepth))

        value = -math.inf   #ustalana jest najmniejsza mozliwa liczba puntkow dla alpha
        possibleMoves = self.PossibleMoves(board)   #sprawdzenie mozliwych ruchow dla danej planszy
        if len(possibleMoves) > 0:
            maxColumn = random.choice(possibleMoves)
        for move in possibleMoves:
            rowCoord,colCoord = move
            updatedBoard = copy.deepcopy(board)     #utworzenie kopii pola gry by dodac mozliwa zmiane w nastepnym ruchu
            updatedBoard[rowCoord][colCoord] = self._iAmPlayerNr
            newScore = self.MinAlphaBeta(updatedBoard,recursiveDepth-1,alpha,beta)[1] #wywolanie funkcji min dla przeciwnego gracza i wyciciagniecie z niego punktow
            if newScore > value:
                value = newScore
                maxColumn = colCoord
            alpha = max(alpha,value)
            if alpha >= beta:
                break
        return maxColumn,value




    def MinAlphaBeta(self,board,recursiveDepth,alpha,beta) -> tuple:
        '''
        Czesc algorytmu MinMax alpha-beta pruning do badania najlepszego nastepnego ruchu, czesc min
        :param board: badana plansza
        :param recursiveDepth: aktualna wartosc rekurencji, ile tur do przodu jest aktualna plansza
        :param alpha: najwieksza znaleziona wartosc punktacji dla badanych dzieci
        :param beta: najmniejsza znaleziona wartosc punktacji(gracz przeciwny) dla badanych dzieci
        :return: nr kolumny do wrzucenia monety i jej wartosc punktowa na plus dla gracza przeciwnego, 0 - pierwsza kolumna
        '''
        result = self.CheckWin(board)
        if result == self._iAmPlayerNr:
            return (None, 100000)
        elif result == self._otherPlayerNr:
            return (None, -100000)
        elif recursiveDepth == 0:
            return (None, self.EvaluateBoard(board,self._recursionValue - recursiveDepth))

        value = math.inf
        possibleMoves = self.PossibleMoves(board)

        if len(possibleMoves) > 0:
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

    def PickbestMove(self,board) -> int:
        '''
        Wybranie najlepszego ruchu dla podanej planszy
        :param board: badana plansza
        :return: nr kolumny do ktorej najlepiej wrzucic monete, 1 - pierwsza kolumna
        '''
        possibleMoves = self.PossibleMoves(board)
        for move in possibleMoves:      #sprawdzenie czy nie ma wygranej w najblizszym ruchu
            rowCoord,colCoord = move
            updatedBoard = copy.deepcopy(board)
            updatedBoard[rowCoord][colCoord] = self._iAmPlayerNr
            if self.CheckWin(updatedBoard) == self._iAmPlayerNr:
                return colCoord+1
        for move in possibleMoves:  #sprawdzenie czy nie ma przegranej w najblizszym ruchu
            rowCoord,colCoord = move
            updatedBoard = copy.deepcopy(board)
            updatedBoard[rowCoord][colCoord] = self._otherPlayerNr
            if self.CheckWin(updatedBoard) == self._otherPlayerNr:
                return colCoord+1


        bestMove = self.MaxAlphaBeta(board,self._recursionValue,-math.inf,math.inf) #sprawdzenie najlepszego ruchu algorytmem
        return bestMove[0]+1



