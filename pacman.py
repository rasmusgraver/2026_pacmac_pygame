import pygame as pg
from constants import *
from board import Board
from character import Character

class PacMan(Character):
    PIXELS_PER_MOVE = 2
    FRAMES_PER_MOVE = TILE_SIZE // PIXELS_PER_MOVE

    def __init__(self, col:int, row:int, board:Board):
        super().__init__(col, row, board)

        self.points = 0 # starter med 0 poeng

        self.frames_right = self.getImageSpriteList(0, 0, 2)
        self.frames_down = self.getImageSpriteList(0, 3, 2)
        # Bildet vi skal vise til å starte med:
        self.frames = self.frames_right


    def update(self):

        if self.board.won:
            # Stopp bevegelse om all maten er spist
            return

        # Sjekk om brukeren trykker piltast og sett neste retning.
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.next_direction = (-1, 0)
        elif keys[pg.K_RIGHT]:
            self.next_direction = (1, 0)
        elif keys[pg.K_UP]:
            self.next_direction = (0, -1)
        elif keys[pg.K_DOWN]:
            self.next_direction = (0, 1)

        # Hvis vi står midt i ruta og neste retning er fri, bytt retning.
        # Skaper veldig hoppende bevegelse uten den offsett == 0,0 ! if self.next_direction != (0, 0):
        if self.offset == (0, 0) and self.next_direction != (0, 0):
            nx, ny = self.next_direction
            if not self.board.is_wall(self.col + nx, self.row + ny):
                self.direction = self.next_direction
                self.next_direction = (0, 0)
                self.venstre = self.direction[0] < 0
                self.up = self.direction[1] < 0
                if self.direction[0] != 0:
                    self.frames = self.frames_right
                else:
                    self.frames = self.frames_down


        if self.direction != (0,0):
            # Endrer offset ut i fra direction:
            dx, dy = self.direction
            self.offset = (self.offset[0] + dx, self.offset[1] + dy)
            self.framecounter += 1

            # Sjekk om vi krasjer i en vegg:
            if self.board.is_wall(self.col + dx, self.row + dy):
                self.offset = (0, 0)
                self.framecounter = 0
                self.current_frame = 0
                self.direction = (0,0)

            if self.framecounter > self.FRAMES_PER_MOVE:
                self.offset = (0, 0)
                self.framecounter = 0
                self.current_frame = 0
                self.col += dx
                self.row += dy
                if self.board.visit(self.col, self.row):
                    self.points += 10

            # Og sprite animasjon:
            if self.framecounter > 0 and self.framecounter % (self.FRAMES_PER_MOVE // 2) == 0:
                self.current_frame += 1
                self.current_frame %= len(self.frames) # Passer på holder oss innafor antall bilder tilgjengelig




