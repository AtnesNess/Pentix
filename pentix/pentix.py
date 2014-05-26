
#!/usr/bin/python3
import random
import time
import inputbox
import pygame
import sys
import os
from pygame.locals import *
from Pentix.pentix_package import *

helloText = "PENTIX"
sub_text = "Powered by AtnesNess"
end_text = "GAME OVER"
restart_text = "Press R to restart"
start_text = "Press Any Button to Start"
moveside_freq = 0.1
movedown_freq = 0.05
field_width = 10
field_height = 20


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


def main():
    load = waiting_for_start()
    gui.clear()
    start(load)


def start(load):
    score = Score(gui, orange, font, 20, 300, 20)
    board = Board(gui, score, box_size, blank,
                  lightblue, orange,
                  figures, figure_width, figure_height,
                  field_width, field_height,
                  colors, lightcolors)
    board.get_empty()
    if load is True:
        board.load()
    next_piece = Piece(gui, board, figures, figure_colors,
                       figure_width, figure_height)
    next_piece.y += 2
    piece = None
    mainloop = True
    last_fall = time.time()
    last_move = time.time()
    falldown = False
    move_right = False
    move_left = False
    pause = False

    while mainloop:
        score.freq_level()
        score.draw()
        event = gui.pressHandling()

        if event == 'r':
            record_list()

        if event == 'p':
            if pause:
                pause = False
            else:
                pause = True

        if pause:
            last_fall = time.time()
            last_move = time.time()

        if piece is None:

            piece = next_piece
            if piece.isTruePos(ady=1) is False:
                mainloop = False
            next_piece = Piece(gui, board, figures,
                               figure_colors, figure_width, figure_height)
            next_piece.toHighest()

           # if not piece.isTruePos(ady=1):
               # mainloop = False
        if event == 'left':
            move_left = True
        elif event == 'right':
            move_right = True
        elif event == 'down':
            falldown = True
        elif event == 'space':
            while piece.isTruePos(ady=1):
                piece.y += 1
        elif event == 'up':
            piece.rotation = (piece.rotation + 1) % len(
                figures[piece.shape])
            if not piece.isTruePos():
                piece.rotation = (piece.rotation - 1) % \
                    len(figures[piece.shape])
        elif event == 's':
            board.save()

        elif event == 'down_release':
            falldown = False

        elif event == 'left_release':
            move_left = False

        elif event == 'right_release':
            move_right = False

        if falldown is True and time.time() - last_fall > movedown_freq:
            if piece.isTruePos(ady=1):
                piece.y += 1
                last_fall = time.time()
        if move_right is True and time.time() - last_move > moveside_freq:
            if piece.isTruePos(adx=1):
                piece.x += 1
                last_move = time.time()

        if move_left is True and time.time() - last_move > moveside_freq:
            if piece.isTruePos(adx=-1):
                piece.x -= 1
                last_move = time.time()
        if time.time() - last_fall > score.freq:
            if not piece.isTruePos(ady=1):
                piece.addToBoard()
                score.addScore(board.deleteFullLines())
                score.freq_level()
                piece = None
            else:
                piece.y += 1
                last_fall = time.time()
     #render
        gui.clear()
        score.draw()
        gui.drawText('Record: {}'.format(topRecord().split(' ')[1][:-1]),
                     font, 20, white, 0, 0)
        board.drawBoard()
        if piece is not None:
            board.drawNextPiece(next_piece, orange, font, 40, shiftx=-150)
            board.drawPiece(piece)
        if pause:
            gui.drawText('PAUSE', font, 70, orange, 70, 100)
            gui.drawText('press p to continue', font, 20, orange, 100, 180)
            gui.drawText('press s to save', font, 20, red, 100, 200)
            gui.drawText('press r to see records', font, 20, white, 100, 220)
        gui.update()
    #Restart

    next_piece = Piece(gui, board,
                       figures, figure_colors,
                       figure_width, figure_height)
    next_piece.y += 2
    piece = None

    if score.isNewRecord():
        answer = inputbox.ask(gui.screen, "Your name")
        while answer == '':
            answer = inputbox.ask(gui.screen, "Your name")
        score.writeRecord(answer)
        gui.clear()
        board.drawBoard()
        gui.drawText('THE END', font, 70, red, 70, 100)
        gui.drawText('Your score is: {}'.format(score.score),
                     font, 20, white, 120, 0)
        gui.update()
    while mainloop is False:
        gui.clear()
        board.drawBoard()
        gui.drawText('THE END', font, 70, red, 70, 100)
        gui.drawText('Press enter to restart', font, 20, white, 100, 30)
        gui.drawText('Your score is: {}'.format(score.score),
                     font, 20, white, 120, 0)
        gui.drawText('press r to see records', font, 20, white, 100, 200)
        event = gui.pressHandling()
        if event == 'enter':
            load = False
            mainloop = True
        if event == 'r':
            record_list()
        gui.update()
    start(load)


def waiting_for_start():
    load = False
    topRecord()

    go = False
    while go is False:
        gui.drawText('Pentix', font, 70, orange, 70, 100)
        gui.drawText('Powered by AtNes Ness', font, 30, orange, 20, 180)
        gui.drawText('press enter to start', font, 20, orange, 100, 220)
        gui.drawText('press l to load', font, 20, green, 100, 240)
        gui.drawText('press r to see records', font, 20, blue, 70, 260)
        gui.drawText('The record is {} pts made by {}'.format(
            topRecord().split(' ')[1][:-1],
            topRecord().split(' ')[0]), font, 20, red, 0, 300)
        gui.update()
        event = gui.pressHandling()
        if event == 'r':
            record_list()
        if event == 'enter':
            go = True
        if event == 'l':
            load = True
            go = True

    return load


def record_list():
    gui.clear()
    rec = True
    while rec:
        pos = 0
        for i in show_records().split(';'):
            gui.drawText(i[:-1], font, 20, green, 100, 30+pos)
            pos += 30
        event = gui.pressHandling()
        gui.drawText('press enter to return', font, 20, red, 100, 20+pos)
        if event == 'enter':
            gui.clear()
            rec = False

        gui.update()

if __name__ == '__main__':
    main()
