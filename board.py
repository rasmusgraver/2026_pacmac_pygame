import pygame as pg
from constants import *

class Board:

    boardStr = [
        "###########",
        "#.........#",
        "#.##.##.#.#",
        "#.........#",
        "###########",
    ]

    boardStrLarge = [
        "#################",
        "#...##.....##...#",
        "#.#.###.###.#.#.#",
        "#.#...........#.#",
        "#.#.###.#.###.#.#",
        "#.....#...#.....#",
        "###.#.#####.#.###",
        "#...............#",
        "###.#.#####.#.###",
        "#.....#...#.....#",
        "#.#.###.#.###.#.#",
        "#.#...........#.#",
        "#.#.###.###.#.#.#",
        "#...##.....##...#",
        "#################",
    ]
    
    def __init__(self):
        # Lag en liste av lister:
        self.grid = [list(row) for row in self.boardStr]

        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.won = False # Sjekker om all maten er spist

    def window_size(self):
        # Legger på litt plass under brettet, til liv og poeng etc
        return self.cols*TILE_SIZE, self.rows*TILE_SIZE + 40

    def draw(self, surface):
        """Tegn brettet på den gitte pygame-flaten."""
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                rect = pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if tile == '#':
                    pg.draw.rect(surface, DARK_BLUE, rect, border_radius=5)
                elif tile == '.':
                    center = (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2)
                    pg.draw.circle(surface, YELLOW, center, radius=3)


    def is_wall(self, col: int, row: int) -> bool:
        """Returnerer True hvis posisjonen er fri for vegg."""
        if col < 0 or col >= self.cols or row < 0 or row >= self.rows:
            return False
        return self.grid[row][col] == '#'

    def visit(self, col: int, row: int) -> bool:
        """ Pacman besøker en celle - spiser maten, og returnerer true false om spist """
        if col < 0 or col >= self.cols or row < 0 or row >= self.rows:
            return False
        if self.grid[row][col] == '.':
            # Spis, og return True, så det teller som poeng
            self.grid[row][col] = ' '
            self.won = self.food_empty()
            return True
        return False

    def food_empty(self):
        # Sjekk om all maten på brettet er spist:
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                if tile == ".":
                    return False
        return True
