import unittest
import Connect4Logic
import Errors

class TestLogicForStandardConnect4(unittest.TestCase):
    def setUp(self):
        self.game = Connect4Logic.StandardRules()
        self.game._whosTurn = 1

    def test_Stack4Coins(self):
        columnToDropCoin = 1
        for i in range(0,4):
            self.game.DropCoin(columnToDropCoin)
            self.game.ChangeActivePlayer()
        self.assertEqual(self.game.Board[3][columnToDropCoin-1],2 )

    def test_WinFirstPlayerHorizontal(self):
        columnToDropCoin = 1
        for oneFullTurn in range(0,3):
            for onePlayer in range(0,2):
                self.game.DropCoin(columnToDropCoin)
                self.game.ChangeActivePlayer()
            columnToDropCoin += 1
        self.game.DropCoin(columnToDropCoin)
        self.game.CheckWin()
        self.assertEqual(self.game._winner, 1)

    def test_WinFirstPlayerVertical(self):
        columnToDropCoinForFirstPlayer = 1
        columnToDropCoinForSecondPlayer = 2
        for oneFullTurn in range(0,3):
            self.game.DropCoin(columnToDropCoinForFirstPlayer)
            self.game.ChangeActivePlayer()
            self.game.DropCoin(columnToDropCoinForSecondPlayer)
            self.game.ChangeActivePlayer()
        self.game.DropCoin(columnToDropCoinForFirstPlayer)
        self.game.CheckWin()
        self.assertEqual(self.game._winner, 1)

    def test_WinFirstPlayerDiagonally(self):
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
        self.assertEqual(self.game._winner, 1)

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










if __name__ == '__main__':
    unittest.main()