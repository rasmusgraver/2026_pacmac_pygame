from pathlib import Path
import pygame as pg
from constants import *
from board import Board

class PacMan:
    IMAGE_FILE = Path(__file__).parent / "sprites" / "pacman2.png"
    FRAMES_PER_MOVE = TILE_SIZE

    def getImageSpriteList(self, x_start, y_start, num_frames) -> list[pg.Surface]:
        full_image = pg.image.load(self.IMAGE_FILE)
        frame_width = 16
        
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

        self.frames_idle = self.getImageSpriteList(0, 0, 4)
        # Bildet vi skal vise til å starte med er idle:
        self.frames = self.frames_idle
        # Om vi vil ha animasjon som går gjennom frames:
        self.current_frame = 0
        self.framecounter = 0

        # Om vi vil speile bildet:
        self.venstre = False


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


        # Endrer offset ut i fra direction:
        dx, dy = self.direction
        self.offset = (self.offset[0] + dx, self.offset[1] + dy)
        self.framecounter += 1

        # Sjekk om vi krasjer i en vegg:
        if self.board.is_wall(self.col + dx, self.row + dy):
            self.offset = (0, 0)
            self.framecounter = 0

        if self.framecounter > self.FRAMES_PER_MOVE:
            self.offset = (0, 0)
            self.framecounter = 0
            self.col += dx
            self.row += dy


    def draw(self, surface):

        # Få bildet fra en liste av bilder (om du vil bruke animasjon/sprites):
        current_frame_image = self.frames[self.current_frame]
        
        # Speiler bildet hvis det trengs:
        if self.venstre:
            current_frame_image = pg.transform.flip(current_frame_image, True, False)

        # Sørg for at vi tegner midt i "Tile":
        mid = TILE_SIZE // 2
        ox, oy = self.offset
        rect = current_frame_image.get_rect()
        rect.center = (self.col * TILE_SIZE + mid + ox , self.row * TILE_SIZE + mid + oy)

        # Blit images på skjermen (der self.rect befinner seg):
        surface.blit(current_frame_image, rect)

