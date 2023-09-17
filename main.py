# Example file showing a basic pygame "game loop"
import pygame
import argparse
from enum import Enum

# pygame setup
pygame.init()
screen = pygame.display.set_mode((700, 700))
clock = pygame.time.Clock()

class CellState(Enum):
    EMPTY = 0,
    ALIVE = 1

class Color(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

class CellTexture(Enum):
    EMPTY_TEXTURE = Color.BLACK,
    ALIVE_TEXTURE = Color.RED

class Cell():
    def __init__(self, position, state: CellState = CellState.EMPTY, texture = None):
        self.texture = texture
        self.state = state
        self.position = position

    def is_alive(self):
        return self.state == CellState.ALIVE
    
    def set_state(self, state: CellState):
        self.state = state

    def get_position(self):
        return self.position

class Grid():
    def __init__(self, rows: int, cols: int, cells: [Cell]):
        self.x = rows
        self.y = cols
        self.cells = cells
        self.cellsize_x = screen.get_height() / self.x
        self.cellsize_y = screen.get_width() / self.y

        self.print_positions()

    @staticmethod
    def from_file(filepath):
        with open(filepath, "r", encoding="utf-8-sig") as file:
            text = file.readlines()
            x, y = text[0].split(" ")
            x = x.strip()
            y = y.strip()
            print("%s %s", (x, y))
            
            print(text[1:])
            line_actual_length = len(text[1].split(" ")) + 2
            cells = []
            cells.append([Cell((-1, i - 1)) for i in range(line_actual_length)])
            for i, line in enumerate(text[1:]):
                cells.append([Cell((i, -1))] + [Cell((i, j)) if cell.strip() == "0" else Cell((i, j), CellState.ALIVE) for j, cell in enumerate(line.split(" "))] + [Cell((i, line_actual_length - 2))])
            cells.append([Cell((line_actual_length - 2, i - 1)) for i in range(line_actual_length)])

            return Grid(int(x), int(y), cells)

    def draw(self):
        # cells
        for j, line in enumerate(self.cells[1:-1]):
            for i, cell in enumerate(line[1:-1]):
                if cell.is_alive():
                    pygame.draw.rect(screen, Color.RED.value, [i * self.cellsize_x, j * self.cellsize_y, self.cellsize_x, self.cellsize_y])

        # lines
        for i in range(self.x - 1):
           y = (i + 1) * self.cellsize_x
           pygame.draw.line(screen, Color.BLACK.value, [0, y], [screen.get_width(), y])
        for i in range(self.y - 1):
           x = (i + 1) * self.cellsize_y
           pygame.draw.line(screen, Color.BLACK.value, [x, 0], [x, screen.get_height()])

    def update(self):
        def get_neighbours_count(i, j):
            for line in self.cells[j:j+3]:
                print([cell.get_position() for cell in line[i: i+3]])

            return sum(1 if cell.is_alive() else 0 for line in self.cells[j:j+3] for cell in line[i:i+3]) - (1 if self.cells[j+1][i+1].is_alive() else 0)
        
        temp_update = []

        for j, line in enumerate(self.cells[1:-1]):
            temp_update.append([])
            for i, cell in enumerate(line[1:-1]):
                count = get_neighbours_count(i, j)
                print(f'{cell.get_position()} : count: {count}')
                temp_update[j].append(count)

        for j, line in enumerate(temp_update):
            for i, count in enumerate(line):
                cell = self.cells[j+1][i+1]

                if (count == 3 and not cell.is_alive()) or (cell.is_alive() and (count in (2, 3))):
                    cell.set_state(CellState.ALIVE)
                else:
                    cell.set_state(CellState.EMPTY)

    # --------- DEBUG -----------
    def print_complete(self):
        print('---')
        for line in self.cells:
            print([1 if cell.is_alive() else 0 for cell in line])

    def print(self):
        print('---')
        for line in self.cells[1: -1]:
            print([1 if cell.is_alive() else 0 for cell in line[1: -1]])

    def print_positions(self):
        print('---debug positions---')
        for line in self.cells:
            print([cell.get_position() for cell in line])
                


def main():
    grid = Grid.from_file("patterns/plus.p")
    running = True

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYUP:
                grid.update()
                grid.print()

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(Color.WHITE.value)

        # RENDER YOUR GAME HERE
        grid.draw()

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Game of Life: Press a button to update a cycle")
    args = parser.parse_args()
    try:
        if args.help:
            print(args.help)
    except AttributeError:
        pass

    main()