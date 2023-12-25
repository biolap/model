import numpy as np
import pygame

# Размер игрового поля
grid_size = 20
cell_size = 50

# Инициализация игрового поля случайными эмоциями
emotional_grid = np.random.uniform(low=0.0, high=1.0, size=(grid_size, grid_size))

# Функция для применения гомотопии между эмоциями
def emotional_homotopy(t, emotion1, emotion2):
    return (1 - t) * emotion1 + t * emotion2

# Функция для шага игры
def game_step(emotional_grid):
    new_emotional_grid = emotional_grid.copy()

    for i in range(grid_size):
        for j in range(grid_size):
            # Применение гомотопии к соседним клеткам
            for x in range(max(0, i - 1), min(grid_size, i + 2)):
                for y in range(max(0, j - 1), min(grid_size, j + 2)):
                    if x != i or y != j:
                        t = np.random.rand()  # случайный параметр гомотопии
                        new_emotional_grid[i, j] = emotional_homotopy(t, emotional_grid[i, j], emotional_grid[x, y])

    return new_emotional_grid

# Инициализация pygame
pygame.init()
screen = pygame.display.set_mode((grid_size * cell_size, grid_size * cell_size))
clock = pygame.time.Clock()

# Игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Отображение текущего состояния игрового поля
    for i in range(grid_size):
        for j in range(grid_size):
            color = (int(emotional_grid[i, j] * 255), 0, 0)
            pygame.draw.rect(screen, color, (i * cell_size, j * cell_size, cell_size, cell_size))

    pygame.display.flip()
    emotional_grid = game_step(emotional_grid)
    clock.tick(2)  # Частота обновления поля (2 раза в секунду)

# Завершение pygame
pygame.quit()



