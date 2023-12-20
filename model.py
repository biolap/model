import numpy as np
import matplotlib.pyplot as plt
from IPython.display import clear_output
import time

# Размер игрового поля
grid_size = 10

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

# Функция для отображения игрового поля
def plot_emotional_grid(emotional_grid):
    plt.imshow(emotional_grid, cmap='coolwarm', interpolation='nearest', vmin=0.0, vmax=1.0)
    plt.colorbar()
    plt.show()

# Игровой цикл
for _ in range(10):  # 10 шагов игры
    # Очистка вывода и отображение текущего состояния игрового поля
    clear_output(wait=True)
    plot_emotional_grid(emotional_grid)
    time.sleep(0.5)  # задержка для создания эффекта анимации

    emotional_grid = game_step(emotional_grid)



