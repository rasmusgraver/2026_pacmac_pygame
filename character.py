from pathlib import Path
import pygame as pg
from constants import *
from board import Board

class Character:
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


        # Om vi vil ha animasjon som går gjennom frames:
        self.current_frame = 0
        self.framecounter = 0

        # Om vi vil speile bildet:
        self.venstre = False
        self.up = False

        # Må bare definere den her - subklassen må sette til noe fornuftig
        self.frames = []




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

