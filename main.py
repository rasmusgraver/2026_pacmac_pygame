import pygame as pg
from constants import *
from board import Board
from pacman import PacMan

pg.init()
board = Board()
vindu = pg.display.set_mode(board.window_size())
clock = pg.time.Clock()

pacman = PacMan(4, 3, board)

font = pg.font.SysFont("Arial", 24)      # opprett font

def draw_points(vindu):
    text_surface = font.render(f"Points: {pacman.points}", True, YELLOW)
    rect = (10, board.rows*TILE_SIZE + 5)
    vindu.blit(text_surface, rect)
    if board.won:
        text_surface = font.render("YOU WON!", True, YELLOW)
        rect = (100, board.rows*TILE_SIZE + 5)
        vindu.blit(text_surface, rect)


running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False

    # Tegn bakgrunn: (En slags "reset" av hele vinduet vårt)
    vindu.fill(BLACK)

    # Tegn brettet først, og pacman og andre ting "oppå":
    board.draw(vindu)
    draw_points(vindu)

    # Oppdater objektene våre:
    pacman.update()

    # Tegn objektene våre:
    pacman.draw(vindu)


    # Har alltid disse med til slutt:
    pg.display.flip()
    clock.tick(FPS)


# While running er slutt: Avslutt pygame på en "ryddig måte":
pg.quit()
