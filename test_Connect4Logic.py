import unittest
import Connect4Logic
import Errors

class TestLogicForStandardConnect4(unittest.TestCase):
    '''
    Testy dla podstawowego trybu Connect4
    '''
    def setUp(self):
        self.game = Connect4Logic.StandardRules()
        self.whoStartedShouldWin = self.game.ActivePlayer
        self.game.ChangeActivePlayer()
        self.otherPlayerNr = self.game.ActivePlayer
        self.game.ChangeActivePlayer()



    def test_Stack4Coins(self):
        columnToDropCoin = 1
        for i in range(0,4):
            self.game.DropCoin(columnToDropCoin)
            self.game.ChangeActivePlayer()
        self.assertEqual(self.game.Board[3][columnToDropCoin-1],self.otherPlayerNr )

    def test_WinHorizontal(self):
        columnToDropCoin = 1
        for oneFullTurn in range(0,3):
            for onePlayer in range(0,2):
                self.game.DropCoin(columnToDropCoin)
                self.game.ChangeActivePlayer()
            columnToDropCoin += 1
        self.game.DropCoin(columnToDropCoin)
        self.game.CheckWin()
        self.assertEqual(self.game.WhoWins(), self.whoStartedShouldWin)

    def test_WinVertical(self):
        columnToDropCoinForFirstPlayer = 1
        columnToDropCoinForSecondPlayer = 2
        for oneFullTurn in range(0,3):
            self.game.DropCoin(columnToDropCoinForFirstPlayer)
            self.game.ChangeActivePlayer()
            self.game.DropCoin(columnToDropCoinForSecondPlayer)
            self.game.ChangeActivePlayer()
        self.game.DropCoin(columnToDropCoinForFirstPlayer)
        self.game.CheckWin()
        self.assertEqual(self.game.WhoWins(), self.whoStartedShouldWin)

    def test_WinDiagonally(self):
        columnToDropCoin = 1
        self.game.DropCoin(columnToDropCoin)
        self.game.ChangeActivePlayer()

        for oneColumn in range(0,3):
            columnToDropCoin += 1
            for oneTurn in range(0,3):
                self.game.DropCoin(columnToDropCoin)
                self.game.ChangeActivePlayer()
        self.game.DropCoin(columnToDropCoin)
        self.game.CheckWin()
        self.assertEqual(self.game.WhoWins(), self.whoStartedShouldWin)

    def test_WinWhenConnectSeven(self):
        columnToDropCoin = 1
        for oneFullTurn in range(0,3): #kazdy gracz wrzuca po jednej monecie do kolumn od 1-3
            for onePlayer in range(0,2):
                self.game.DropCoin(columnToDropCoin)
                self.game.ChangeActivePlayer()
            columnToDropCoin += 1

        columnToDropCoin = 5
        for oneFullTurn in range(0,3):  #kazdy gracz wrzuca po jednej monecie do kolumn od 5-7
            for onePlayer in range(0,2):
                self.game.DropCoin(columnToDropCoin)
                self.game.ChangeActivePlayer()
            columnToDropCoin += 1

        self.game.DropCoin(4)

        self.game.CheckWin()
        self.assertEqual(self.game.WhoWins(), self.whoStartedShouldWin)

    def test_Tie(self):
        for columnToDropCoin in range(1,4): #zapelnienie pierwszych trzech kolumn naprzemian
            for oneFullTurn in range(0,6):
                self.game.DropCoin(columnToDropCoin)
                self.game.ChangeActivePlayer()

        for columnToDropCoin in range(5,7): #zapelnienie 5 i 6 kolumny naprzemian
            for oneFullTurn in range(0,6):
                self.game.DropCoin(columnToDropCoin)
                self.game.ChangeActivePlayer()

        self.game.DropCoin(7) #jedna moneta do 7 kolumny by zmienic kolory

        for oneFullTurn in range(0, 6): #zapelnienie 4 kolumny
            self.game.DropCoin(4)
            self.game.ChangeActivePlayer()

        for oneFullTurn in range(0,4): #dokladanie monet do 7 kolumny, zostaje jedno wolne miejsce
            self.game.DropCoin(7)
            self.game.ChangeActivePlayer()

        self.assertRaises(Errors.FullGameBoardException,self.game.DropCoin,7)

    def test_ExceptionWhenDropCoinToFullColumn(self):
        for dropCoinInFirstColumn in range(0,6):
            self.game.DropCoin(1)
            self.game.ChangeActivePlayer()
        self.assertRaises(Errors.FullColumnException,self.game.DropCoin,1)




class TestLogicForFiveInARow(unittest.TestCase):
    '''
    Testy dla trybu z wieksza plansza 9x6
    '''
    def setUp(self):
        self.game = Connect4Logic.FiveInARow()
        self.whoStartedShouldWin = self.game.ActivePlayer
        self.game.ChangeActivePlayer()
        self.otherPlayerNr = self.game.ActivePlayer
        self.game.ChangeActivePlayer()



    def test_Stack4Coins(self):
        columnToDropCoin = 2
        for i in range(0,4):
            self.game.DropCoin(columnToDropCoin)
            self.game.ChangeActivePlayer()
        self.assertEqual(self.game.Board[3][columnToDropCoin-1],self.otherPlayerNr )

    def test_WinHorizontal(self):
        columnToDropCoin = 2
        for oneFullTurn in range(0,4):
            for onePlayer in range(0,2):
                self.game.DropCoin(columnToDropCoin)
                self.game.ChangeActivePlayer()
            columnToDropCoin += 1
        self.game.DropCoin(columnToDropCoin)
        self.game.CheckWin()
        self.assertEqual(self.game.WhoWins(), self.whoStartedShouldWin)



    def test_WinVertical(self):
        columnToDropCoinForFirstPlayer = 2
        columnToDropCoinForSecondPlayer = 3
        for oneFullTurn in range(0,4):
            self.game.DropCoin(columnToDropCoinForFirstPlayer)
            self.game.ChangeActivePlayer()
            self.game.DropCoin(columnToDropCoinForSecondPlayer)
            self.game.ChangeActivePlayer()
        self.game.DropCoin(columnToDropCoinForFirstPlayer)
        self.game.CheckWin()
        self.assertEqual(self.game.WhoWins(), self.whoStartedShouldWin)

    def test_WinDiagonally(self):
        columnToDropCoin = 2
        self.game.DropCoin(columnToDropCoin)
        self.game.ChangeActivePlayer()

        for oneColumn in range(0,2):
            columnToDropCoin += 1
            for oneTurn in range(0,3):
                self.game.DropCoin(columnToDropCoin)
                self.game.ChangeActivePlayer()

        for oneColumn in range(0,2):
            columnToDropCoin += 1
            for oneTurn in range(0,5):
                self.game.DropCoin(columnToDropCoin)
                self.game.ChangeActivePlayer()

        self.game.DropCoin(columnToDropCoin)
        self.game.CheckWin()
        self.assertEqual(self.game.WhoWins(), self.whoStartedShouldWin)

    def test_WinWhenConnectSeven(self):
        columnToDropCoin = 2
        for oneFullTurn in range(0,4): #kazdy gracz wrzuca po jednej monecie do kolumn od 2-5
            for onePlayer in range(0,2):
                self.game.DropCoin(columnToDropCoin)
                self.game.ChangeActivePlayer()
            columnToDropCoin += 1

        columnToDropCoin = 7
        for oneFullTurn in range(0,2):  #kazdy gracz wrzuca po jednej monecie do kolumn od 7-8
            for onePlayer in range(0,2):
                self.game.DropCoin(columnToDropCoin)
                self.game.ChangeActivePlayer()
            columnToDropCoin += 1

        self.game.DropCoin(6)

        self.game.CheckWin()
        self.assertEqual(self.game.WhoWins(), self.whoStartedShouldWin)

    def test_Tie(self):
        for columnToDropCoin in range(2,6): #zapelnienie kolumn 2-5 naprzemian
            for oneFullTurn in range(0,6):
                self.game.DropCoin(columnToDropCoin)
                self.game.ChangeActivePlayer()

        for columnToDropCoin in range(7,8): #zapelnienie 7 kolumny naprzemian
            for oneFullTurn in range(0,6):
                self.game.DropCoin(columnToDropCoin)
                self.game.ChangeActivePlayer()

        self.game.DropCoin(8) #jedna moneta do 8 kolumny by zmienic kolory

        for oneFullTurn in range(0, 6): #zapelnienie 6 kolumny
            self.game.DropCoin(6)
            self.game.ChangeActivePlayer()

        for oneFullTurn in range(0,4): #dokladanie monet do 8 kolumny, zostaje jedno wolne miejsce
            self.game.DropCoin(8)
            self.game.ChangeActivePlayer()

        self.assertRaises(Errors.FullGameBoardException,self.game.DropCoin,8)

    def test_ExceptionWhenDropCoinToFullColumn(self):
        for dropCoinInFirstColumn in range(0,6):
            self.game.DropCoin(2)
            self.game.ChangeActivePlayer()
        self.assertRaises(Errors.FullColumnException,self.game.DropCoin,2)



if __name__ == '__main__':
    unittest.main()