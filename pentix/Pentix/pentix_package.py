#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import random
import time
import sys


class Gui():

    """
        класс отвечает за Графический интерфейс
    """

    def __init__(self, width, height, bgColor):
        """
            Инициализация графического интерфейса
            width - ширина окна px
            height - высота окна px
            bgColor - цвет фона (R,G,B)
        """
        pygame.init()
        pygame.font.init()
        self.bgColor = bgColor
        self.window_width = width
        self.window_height = height
        self.screen = pygame.display.set_mode((self.window_width,
                                               self.window_height), 0, 32)
        self.screen.fill(self.bgColor)

    def set_title(self, title):
        """
            Установка названия окна
            title - название
        """
        pygame.display.set_caption(title)

    def update(self):
        """
            Обновление графического интерфейса

        """
        pygame.display.update()

    def clear(self):
        """
            Очистка экрана
        """
        self.screen.fill(self.bgColor)

    def drawText(self, text, font, size, color, pos_x, pos_y):
        """
            Метод пишет текст на экран
            text - текст
            size - размер текста
            color - цвет текста (R,G,B)
            pos_x - позиция на экране по горизонтали
            pos_y - позиция на экране по вертикали
        """
        my_font = pygame.font.Font(font, size)
        text_render = my_font.render(text, 0, color)
        self.screen.blit(text_render, (pos_x, pos_y))

    def keydown(self, key, event):
        """
            Проверка на нажатие клавиши
            key - название кнопки в формате pyGame
            event - событие
        """
        if event.type == KEYDOWN:
            if event.key == key:
                return True

    def keyup(self, key, event):
        """
            Проверка на спуск клавиши
            key - название кнопки в формате pyGame
            event - событие
        """
        if event.type == KEYUP:
            if event.key == key:
                return True

    def pressHandling(self):
        """
            Метод определяет какая клавиша была нажата и
            возвращает символьный эквивалент в формате str
        """
        for event in pygame.event.get([QUIT]):
            self.shutdown()
        for event in pygame.event.get():
            if self.keydown(K_ESCAPE, event):
                self.shutdown()
            if self.keydown(K_LEFT, event):
                return 'left'
            elif self.keydown(K_RETURN, event):
                return 'enter'
            elif self.keydown(K_RIGHT, event):
                return 'right'
            elif self.keydown(K_DOWN, event):
                return 'down'
            elif self.keydown(K_SPACE, event):
                return 'space'
            elif self.keydown(K_UP, event):
                return 'up'
            elif self.keydown(K_p, event):
                return 'p'
            elif self.keydown(K_r, event):
                return 'r'
            elif self.keydown(K_s, event):
                return 's'
            elif self.keydown(K_y, event):
                return 'y'
            elif self.keydown(K_n, event):
                return 'n'
            elif self.keydown(K_l, event):
                return 'l'

            elif self.keyup(K_DOWN, event):
                return 'down_release'

            elif self.keyup(K_LEFT, event):
                return 'left_release'

            elif self.keyup(K_RIGHT, event):
                return 'right_release'

    def shutdown(self):
        """
            Завершает работу графического интерфейса
            и самой программы
        """
        pygame.quit()
        sys.exit()


class Board():
    """
        Класс отвечает за обработку игрового поля
    """
    def __init__(self, gui, score, box_size, blank, grid_color,
                 border_color,  figures, width, height,
                 field_width, field_height, colors, lightcolors):
        """
         Инициализация игрового поля
         gui - графический интерфейс (класс)
         score - счет (класс)
         box_size - размер наименьшей части фигуры
         blank - символ пустого элемента на поле (блока)
         grid_color - цвет сетки на поле (R, G, B)
         border_color - цвет границы поля (R, G, B)
         figures - словарь фигур
         width - максимальная ширина фигуры
         height - максимальная длина фигруы
         field_width - ширина игрового поля
         field_height - высота игрового поля
         colors - цвета для тени блоков (кортеж)
         lightcolors - основные цвета блоков (кортеж)
        """
        self.score = score
        self.figures = figures
        self.figure_width = width
        self.figure_height = height
        self.colors = colors
        self.lightcolors = lightcolors
        self.grid_color = grid_color
        self.border_color = border_color
        self.gui = gui
        self.blank = blank
        self.box_size = box_size
        self.board = []
        self.width = box_size * field_width
        self.height = box_size * field_height
        self.xmargin = gui.window_width-self.width - 100
        self.ymargin = gui.window_height-self.height

    def save(self):
        """
            сохранение текущего состояния игры
        """
        self.gui.clear()
        self.gui.drawText('Do you want to save the game?',
                          'freesansbold.ttf', 20, (255, 0, 0), 50, 100)
        self.gui.drawText("press 'y'(yes) or 'n'(no)",
                          'freesansbold.ttf', 20, (255, 0, 0), 100, 130)
        self.gui.update()
        wait = True
        while wait:
            event = self.gui.pressHandling()
            if event == 'y':
                save_file = open('saves.sv', 'w')
                save_file.write(str(self.score.score))
                for i in range(int(self.height/self.box_size)):
                    save_file.write('\n')
                    for j in range(int(self.width/self.box_size)):
                        save_file.write(str(self.board[j][i]))
                self.gui.shutdown()
            elif event == 'n':
                wait = False

    def load(self):
        """
            загрузка состояния игры из файла
        """
        save_file = open('saves.sv', 'r')
        score = save_file.next()
        self.score.addScore(int(score))
        self.score.freq_level()
        for i in range(int(self.height/self.box_size)):
            nex = save_file.next()
            for j in range(int(self.width/self.box_size)):
                try:
                    self.board[j][i] = int(nex[j])
                except ValueError:
                    self.board[j][i] = nex[j]

    def convertToPix(self, x, y, xmargin, ymargin):
        """
            конвертация координат на поле в пиксели
            x - координата x на игровом поле
            y - координата y на игровом поле
            xmargin - отступ по x
            ymargin - отступ по y
            возвращает кортеж из двух
            конвертированных координат x,y
        """
        return (xmargin + (x * self.box_size)), (ymargin + (y * self.box_size))

    def get_empty(self):
        """
            задание матрицы игрового поля и его обнуление
            возвращает матрицу игрового поля
        """
        self.board = []
        for i in range(int(self.width/self.box_size)):
            self.board.append([self.blank] * int(self.height / self.box_size))
        return self.board

    def deleteFullLines(self):
        """
            стираем все заполненные линии
            возвращает количество удаленных линий
        """
        number_of_lines = 0
        y = int(self.height / self.box_size - 1)
        while y > 0:
            if self.isCompleteLine(y):
                number_of_lines += 1
                self.shiftDown(y)
                self.drawBoard()
            else:
                y -= 1

        return number_of_lines

    def isCompleteLine(self, y):
        """
            проверяет является ли строка на позиции y
            заполненной
            возвращает True или False
        """
        for x in range(int(self.width/self.box_size)):
            if self.board[x][y] == self.blank:
                return False
        return True

    def shiftDown(self, y):
        """
            стирает строку y и свдигает все поле на
            1 клетку вниз
            y - координата строки
        """
        for shift in range(y, 0, -1):
            for x in range(int(self.width/self.box_size)):
                self.board[x][shift] = self.board[x][shift-1]
        for x in range(int(self.width/self.box_size)):
            self.board[x][0] = self.blank

    def drawBox(self, x, y, color=None, shiftx=0):
        """
            прорисовывает блок на определенном месте
            x - координата по горзонтали
            y - координата по вертикали
            color - цвет блока
            shiftx - сдвиг по x
        """
        if self.board[x][y] == self.blank and color is None:
            return
        if color is None:
            place = self.board[x][y]
        else:
            place = color
        x, y = self.convertToPix(x, y, self.xmargin, self.ymargin)

        pygame.draw.rect(self.gui.screen, self.colors[place],
                         (x + 1 + shiftx, y + 1, self.box_size - 1,
                          self.box_size - 1))
        pygame.draw.rect(self.gui.screen, self.lightcolors[place],
                         (x + 3 + shiftx, y + 3, self.box_size - 4,
                          self.box_size - 4))

    def drawBoard(self):
        """
            прописовка самого игрового поля
        """
        for x in range(int(self.width/self.box_size)):
            for y in range(int(self.height/self.box_size)):
                self.drawBox(x, y)
                pygame.draw.rect(self.gui.screen, self.grid_color,
                                 (self.xmargin + x*self.box_size,
                                  self.ymargin +
                                  y * self.box_size,
                                  self.box_size, self.box_size), 1)
        pygame.draw.rect(self.gui.screen,
                         self.border_color,
                         (self.xmargin, self.ymargin, self.width,
                          self.height), 2)

    def drawPiece(self, piece, shiftx=0):
        """
            Прорисовка фигуры на игровом поле
            piece - фигура
            shiftx - сдвиг по x
        """
        shapeToDraw = self.figures[piece.shape][piece.rotation]
        for x in range(self.figure_width):
            for y in range(self.figure_height):
                if shapeToDraw[y][x] != self.blank:
                    self.drawBox(piece.x + x, piece.y + y,
                                 color=piece.color, shiftx=shiftx)

    def drawNextPiece(self, next_piece, color, font, size, shiftx=0):
        """
            прорисовка ожидаемой фигуры
            next_piece - следующая фигура
            color - цвет текста Next
            size - размер текста
            shiftx - сдвиг по x
        """
        myFont = pygame.font.Font(font, size)
        nextPrint = myFont.render('Next:', True, color)
        nextRect = nextPrint.get_rect()
        nextRect.topleft = (next_piece.x * self.box_size
                            + self.xmargin + shiftx, self.ymargin - size*2)
        self.gui.screen.blit(nextPrint, nextRect)
        self.drawPiece(next_piece, shiftx)


class Piece():
    """
        Класс отвечающий за обработку фигуры на игровом поле
    """
    def __init__(self, gui, board, figures, colors, f_width, f_height):
        """
            Инициализация фигуры
            gui - графический интерфейс ( Класс)
            board - игровое поле ( Класс)
            figures - словарь фигур
            colors - цвета
            f_width - максимальная ширина фигуры
            f_height - максимальная длина фигуры
        """
        self.gui = gui
        self.board = board
        self.f_width = f_width
        self.f_height = f_height
        self.figures = figures
        self.shape = random.choice(list(figures.keys()))
        self.color = colors[self.shape]
        self.rotation = random.randint(0, len(figures[self.shape]) - 1)
        self.x = int(self.board.width /
                     self.board.box_size / 2) - int(f_width / 2)
        self.y = -3

    def isOnBoard(self, x, y, adx=0, ady=0):
        """
            Проверяет лежит ли точка в игровом поле
            x - координата по горизонтали
            y - координата по вертикали
            adx - сдвиг по x
            ady - сдвиг по y
        """
        return 0 <= adx + self.x + x < \
            self.board.width / self.board.box_size and\
            0 <= y + self.y + ady < self.board.height/self.board.box_size

    def addToBoard(self):
        """
            Добавляет фигуру на игровое поле
        """
        for x in range(self.f_width):
            for y in range(self.f_height):
                if self.figures[self.shape][self.rotation][y][x]\
                        != self.board.blank:
                    self.board.board[x + self.x][y + self.y] = self.color

    def isTruePos(self, adx=0, ady=0):
        """
            Проверяет лежит ли фигура полностью в игровом поле
        """
        for x in range(self.f_width):
            for y in range(self.f_height):
                if self.figures[self.shape][self.rotation][y][x]\
                        != self.board.blank:
                    if not self.isOnBoard(x, y, adx, ady):
                        return False
                    if self.board.board[x + self.x + adx][y + self.y + ady]\
                            != self.board.blank:
                            return False
        return True

    def toHighest(self):
        """
            Перемещает фигуру в наивысшую возможную точку игрового поля
        """
        while not self.isTruePos(ady=1):
            self.y += 1
            if self.y > 4:
                break


class Score():
    """
        Класс отвечающий за обработку счета, уровней и скорости падения фигуры
    """
    def __init__(self, gui, color, font, size, x_pos, y_pos):
        """
            gui - графический интерфейс (Класс)
            color - цвет текста Score и Level
            font - шрифт текста
            size - размер текста
            x_pos - позиция по горизонтали
            y_pos - позиция по вертикали
        """
        self.gui = gui
        self.color = color
        self.font = font
        self.size = size
        self.x_pos = x_pos
        self.y_pos = y_pos
        self._score = 0
        self._level = 1
        self._freq = 0

    def freq_level(self):
        """
            Расчитывает уровень и скорость падения фигуры по счету
        """
        self._level = self._score / 10
        self._freq = 0.4 - (self._level * 0.02)

    @property
    def level(self):
        """
            возвращает номер уровня
        """
        return self._level

    @property
    def freq(self):
        """
            возвращает скорость падения фигуры
        """
        return self._freq

    @property
    def score(self):
        """
            возвращает счет
        """
        return self._score

    def addScore(self, x):
        """
            Прибавляет число к счету
            x - число, прибавленное к счету
        """
        self._score += x
        self.freq_level()

    def draw(self):
        """
            Прорисовывает надписи Score и Level с
            соответствующими счетом и уровнем
        """
        self.gui.drawText('Score: {}'.format(self.score),
                          self.font, self.size,
                          self.color, self.x_pos, self.y_pos)

        self.gui.drawText('Level: {}'.format(self.level),
                          self.font, self.size,
                          self.color, self.x_pos, self.y_pos+2*self.size)

    def isNewRecord(self):
        """
            Проверяет входит ли ваш результат в таблицу рекордов
            (входит ли в 10Top)
        """
        records = open('records.rec', 'r')
        recs = 0
        first = ''
        for i in records:
            recs += 1
            if recs == 1:
                first = i
        if recs < 10:
            return True
        elif recs > 0:
            first = first.split(' ')
            if int(first[1]) < self.score:
                return True
        return False

    def writeRecord(self, inp):
        """
            Записывает рекорд в файлы с рекордами
            inp - строка введенная пользователем
        """
        records = open('records.rec', 'r')
        read = records.readlines()
        new_rec = open('records.rec', 'w')
        write = ''
        added = False
        if len(read) == 0:
            write += (str(inp + ' ' + str(self.score))+'\n')
        else:
            for i in read:
                try:
                    if self.score < int(i.split(' ')[1]) and not added:
                        added = True
                        write += (str(inp + ' ' + str(self.score))+'\n')
                    write += i
                except IndexError:
                    pass
            if not added:
                write += (str(inp + ' ' + str(self.score))+'\n')
            write = write.split('\n')
            while len(write) > 11:
                for k in range(len(write)-1):
                    write[k] = write[k+1]
                del write[len(write)-1]
            write = str('\n'.join(write))
        new_rec.write(write)


def topRecord():
    """
        возвращает топовый рекорд
    """
    records = open('records.rec', 'r').readlines()
    if len(records) == 0:
        return 'nobody 0.'
    return str(reversed(records).next())


def show_records():
    """
    возвращает все рекорды через ';'
    """
    out = ''
    records = open('records.rec', 'r').readlines()
    for i in reversed(records):
        out += i+';'
    return out


def make_figure(figure, dim):
    """
        Вращает данную матрицу несколько раз по 90 градусов
        figure - матрица для вращения
        dim - количество поворотов на 90 градусов
        возвращает двумерную матрицу с описанием всех вращений исходной матрицы
    """
    fig = [[]]
    fig[0] = figure
    for r in range(int(dim)-1):
        fig.append([''])
        for i in range(len(fig[0])):
            fig[r+1] = []
            for j in range(len(fig[0])):
                fig[r+1].append('')
                for k in range(len(fig[0])):
                    fig[r+1][j] += str(fig[r][len(fig[0])-1-k][j])

    return fig


def figure_describe_read(figure_height):
    """
        Считывает фигуру(матрица)
        figure_height - высота/ширина фигуры
        возвращает кортеж из фигур(матриц), цветов теней и основных цветов
    """
    fig_discribe = open('figure.discribe')
    colour = []
    colors = []
    lightcolors = []
    figure = []
    figures = {}
    num = 0
    for i in fig_discribe:

        if i == '--colors\n':
            colour = []
            digit = ''
            d = 0

            for j in fig_discribe.next():
                    d += 1
                    if d != 4:
                        digit += j
                    else:
                        d = 0
                        colour = list(colour)
                        colour.append(int(digit))
                        digit = ''

            colors.append(tuple(colour))
            colour = []
            d = 0
            for j in fig_discribe.next():
                    d += 1
                    if d != 4:
                        digit += j
                    else:
                        d = 0
                        colour.append(int(digit))
                        digit = ''
            lightcolors.append(tuple(colour))
        if i == '--figure\n':
            dim = fig_discribe.next()[:-1]
            for j in range(figure_height):
                figure.append(fig_discribe.next()[:-1])
            figures[num] = make_figure(figure, dim)
            num += 1
            figure = []
    return figures, tuple(colors), tuple(lightcolors)
