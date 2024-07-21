

import numpy as np
import pygame
import random

def initialize_grid(rows, cols):
    return np.zeros((rows, cols), dtype=int)

def get_next_state(grid):
    rows, cols = grid.shape
    new_grid = grid.copy()
    for row in range(rows):
        for col in range(cols):
            neighbors = grid[max(0, row-1):min(row+2, rows), max(0, col-1):min(col+2, cols)]
            num_living_neighbors = np.sum(neighbors) - grid[row, col]
            if grid[row, col] == 1:
                if num_living_neighbors < 2 or num_living_neighbors > 3:
                    new_grid[row, col] = 0
            else:
                if num_living_neighbors == 3:
                    new_grid[row, col] = 1
    return new_grid

def randomize_grid(grid):
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            grid[row, col] = random.choice([0, 1])
    return grid

def clear_grid(grid):
    return np.zeros_like(grid)

def draw_grid(screen, grid):
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            color = (255, 255, 0) if grid[row, col] == 1 else (128, 128, 128)
            pygame.draw.rect(screen, color, (MARGIN + col*CELL_SIZE, MARGIN + row*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, (192, 192, 192), (MARGIN + col*CELL_SIZE, MARGIN + row*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_buttons(screen, start_x, button_y, button_width, button_height, button_padding):
    button_color = (0, 122, 204)
    button_hover_color = (0, 153, 255)
    button_text_color = (255, 255, 255)
    button_font = pygame.font.SysFont(None, 24)
    
    buttons = {
        "Start/Stop": (start_x, button_y, button_width, button_height),
        "Randomize": (start_x + button_width + button_padding, button_y, button_width, button_height),
        "Clear": (start_x + 2 * (button_width + button_padding), button_y, button_width, button_height)
    }
    
    for text, (x, y, w, h) in buttons.items():
        mouse_pos = pygame.mouse.get_pos()
        color = button_hover_color if x < mouse_pos[0] < x + w and y < mouse_pos[1] < y + h else button_color
        pygame.draw.rect(screen, color, (x, y, w, h))
        button_text = button_font.render(text, True, button_text_color)
        screen.blit(button_text, (x + (w - button_text.get_width()) // 2, y + (h - button_text.get_height()) // 2))

pygame.init()

# Constants
GRID_SIZE = 30
CELL_SIZE = 20
MARGIN = 20
WIDTH = GRID_SIZE * CELL_SIZE + 2 * MARGIN
HEIGHT = GRID_SIZE * CELL_SIZE + 2 * MARGIN
BUTTON_PANEL_HEIGHT = 60
BOTTOM_MARGIN = 20  # Additional margin below buttons

screen = pygame.display.set_mode((WIDTH, HEIGHT + BUTTON_PANEL_HEIGHT + BOTTOM_MARGIN))
pygame.display.set_caption("Conway's Game of Life")

grid = initialize_grid(GRID_SIZE, GRID_SIZE)
paused = True

button_width, button_height = 100, 30
button_padding = 20
total_button_width = 3 * button_width + 2 * button_padding
start_x = (WIDTH - total_button_width) // 2
button_y = HEIGHT + MARGIN + 10

running = True
while running:
    screen.fill((128, 128, 128))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_r:
                grid = randomize_grid(grid)
            elif event.key == pygame.K_c:
                grid = clear_grid(grid)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if start_x <= x <= start_x + button_width and button_y <= y <= button_y + button_height:
                paused = not paused
            elif start_x + button_width + button_padding <= x <= start_x + 2 * button_width + button_padding and button_y <= y <= button_y + button_height:
                grid = randomize_grid(grid)
            elif start_x + 2 * (button_width + button_padding) <= x <= start_x + 3 * button_width + 2 * button_padding and button_y <= y <= button_y + button_height:
                grid = clear_grid(grid)
            else:
                col = (x - MARGIN) // CELL_SIZE
                row = (y - MARGIN) // CELL_SIZE
                if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE:
                    grid[row, col] = 1 - grid[row, col]
    
    if not paused:
        grid = get_next_state(grid)
    
    draw_grid(screen, grid)
    draw_buttons(screen, start_x, button_y, button_width, button_height, button_padding)
    
    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
