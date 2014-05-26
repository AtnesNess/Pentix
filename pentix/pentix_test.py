#!/usr/bin/python3

import unittest
from Pentix.pentix_package import *
box_size = 20
blank = '.'
white = (255, 255, 255)
green = (0, 155,   0)
red = (255,   0,   0)
orange = (255, 140,   0)
blue = (0,   0, 155)
yellow = (155, 155,   0)
black = (0,   0,   0)
pink = (177,   0, 178)
sea = (51,  178, 169)
darkorange = (178,  88,   0)
lightred = (175,  20,  20)
lightgreen = (20, 175,  20)
lightblue = (20,  20, 175)
lightyellow = (175, 175,  20)
lightpink = (253,  76, 255)
darksea = (76, 255, 242)

figure_width = 5
figure_height = 5
figures, colors, lightcolors = figure_describe_read(figure_height)
figure_colors = {}
col = iter(range(len(colors)))
for figure in figures.keys():
    figure_colors[figure] = next(col)

gui = Gui(400, 500, black)
gui.set_title("Pentix by AtNesNess")
font = 'freesansbold.ttf'
field_width = 5
field_height = 10
score = Score(gui, orange, font, 20, 300, 20)
board = Board(gui, score, box_size, blank,
              lightblue, orange,
              figures, figure_width, figure_height,
              field_width, field_height,
              colors, lightcolors)
board.get_empty()


class Pentix_Board_test(unittest.TestCase):
    def setUp(self):
        self.board = Board(gui, score, box_size, blank,
                           lightblue, orange,
                           figures, figure_width, figure_height,
                           field_width, field_height,
                           colors, lightcolors)
        self.board.get_empty()
        self.board.board = [['.', '.', '.', '.', '.', 3, 0, 2, 1, 0],
                            ['.', '.', '.', '.', '.', 3, '.', 2, 1, 0],
                            ['.', '.', '.', '.', '.', 3, 0, 2, 1, 0],
                            ['.', '.', '.', '.', '.', 3, 0, 2, 1, '.'],
                            ['.', '.', '.', '.', '.', 3, 0, 2, 1, 0]]

    def test_complete_line(self):
        self.assertEqual(self.board.deleteFullLines(), 3)

    def test_shift_complete_line(self):
        new_board = self.board.board = [
            ['.', '.', '.', '.', '.', '.', '.', '.', 0, 0],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.', 0],
            ['.', '.', '.', '.', '.', '.', '.', '.', 0, 0],
            ['.', '.', '.', '.', '.', '.', '.', '.', 0, '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', 0, 0]]
        self.board.deleteFullLines()
        self.assertEqual(self.board.board, new_board)

    def test_empty(self):
        self.board.get_empty()
        empty = [['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.']]
        self.assertEqual(self.board.board, empty)


class Pentix_Piece_test(unittest.TestCase):
    def setUp(self):
        self.piece = Piece(gui, board,
                           figures, figure_colors,
                           figure_width, figure_height)

    def test_piece_on_false_pos(self):
        self.piece.toHighest()
        self.piece.y -= 5
        self.assertEqual(self.piece.isTruePos(), False)

    def test_piece_on_true_pos(self):
        self.piece.toHighest()
        self.piece.y += 2
        self.assertEqual(self.piece.isTruePos(), True)


class Pentix_Score_test(unittest.TestCase):
    def setUp(self):
        self.score = score

    def test_checkFreq(self):
        self.score.addScore(20)
        self.score.freq_level()
        self.assertEqual(round(self.score.freq, 2), 0.36)


if __name__ == '__main__':
    unittest.main()
