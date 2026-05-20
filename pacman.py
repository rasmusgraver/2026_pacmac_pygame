from pathlib import Path
import pygame as pg
from constants import *
from board import Board

class PacMan:
    IMAGE_FILE = Path(__file__).parent / "sprites" / "pacman2.png"
    PIXELS_PER_MOVE = 2
    FRAMES_PER_MOVE = TILE_SIZE // PIXELS_PER_MOVE

    def getImageSpriteList(self, col:int, row:int, num_frames:int) -> list[pg.Surface]:
        full_image = pg.image.load(self.IMAGE_FILE)
        frame_width = 16
        x_start = col*frame_width
        y_start = row*frame_width
        
        # Dele opp bildet i frames, som lagres i en liste:
        frames = []
        for i in range(num_frames):
            # Bildene er kvadratiske - bruker frame widht både som høye og bredde:
            frame = full_image.subsurface(pg.Rect(x_start + i * frame_width, y_start, frame_width, frame_width))
            frames.append(frame)
        return frames
    

    def __init__(self, col:int, row:int, board:Board):
        self.row = row
        self.col = col
        self.board = board
        self.direction = (1,0)
        self.next_direction = (0,0)
        self.offset = (0,0)
        # Holder styr på hvor langt vi "offsetter" i ruta når vi tegner oss selv

        self.points = 0 # starter med 0 poeng

        self.frames_right = self.getImageSpriteList(0, 0, 2)
        self.frames_down = self.getImageSpriteList(0, 3, 2)
        # Bildet vi skal vise til å starte med:
        self.frames = self.frames_right
        # Om vi vil ha animasjon som går gjennom frames:
        self.current_frame = 0
        self.framecounter = 0

        # Om vi vil speile bildet:
        self.venstre = False
        self.up = False


    def update(self):
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
                    print("Yes! Poeng", self.points)

            # Og sprite animasjon:
            if self.framecounter > 0 and self.framecounter % (self.FRAMES_PER_MOVE // 2) == 0:
                self.current_frame += 1
                self.current_frame %= len(self.frames) # Passer på holder oss innafor antall bilder tilgjengelig



    def draw(self, surface):

        # Få bildet fra en liste av bilder (om du vil bruke animasjon/sprites):
        current_frame_image = self.frames[self.current_frame]
        
        # Speiler bildet hvis det trengs:
        if self.venstre:
            current_frame_image = pg.transform.flip(current_frame_image, True, False)
        if self.up:
            current_frame_image = pg.transform.flip(current_frame_image, False, True)

        # Sørg for at vi tegner midt i "Tile":
        mid = TILE_SIZE // 2
        ox, oy = self.offset
        rect = current_frame_image.get_rect()
        rect.center = (self.col * TILE_SIZE + mid + ox*self.PIXELS_PER_MOVE , self.row * TILE_SIZE + mid + oy*self.PIXELS_PER_MOVE)

        # Blit images på skjermen (der self.rect befinner seg):
        surface.blit(current_frame_image, rect)

