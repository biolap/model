import numpy as np
import pygame

# Размер игрового поля
grid_size = 20
cell_size = 50

# Игрок
player_position = np.array([grid_size // 2, grid_size // 2])
player_speed = 5

def perlin_noise(x, y, seed=0):
    np.random.seed(seed)
    gradients = np.random.randn(grid_size, grid_size, 2)
    gradients_norm = np.sqrt(np.sum(gradients ** 2, axis=2))
    gradients /= np.expand_dims(gradients_norm, axis=2)
    x0 = np.floor(x * (grid_size - 1)).astype(int)
    y0 = np.floor(y * (grid_size - 1)).astype(int)
    
    # Убедимся, что x1 и y1 не выходят за границы
    x1 = np.minimum(x0 + 1, grid_size - 1)
    y1 = np.minimum(y0 + 1, grid_size - 1)

    # Используем массивы sx и sy
    sx = np.expand_dims(x * (grid_size - 1) - x0, axis=-1)
    sy = np.expand_dims(y * (grid_size - 1) - y0, axis=-1)

    n0 = np.sum(gradients[x0, y0] * np.dstack([sx, sy]), axis=2)
    n1 = np.sum(gradients[x1, y0] * np.dstack([1 - sx, sy]), axis=2)
    n2 = np.sum(gradients[x0, y1] * np.dstack([sx, 1 - sy]), axis=2)
    n3 = np.sum(gradients[x1, y1] * np.dstack([1 - sx, 1 - sy]), axis=2)
    return np.sum(np.stack([n0, n1, n2, n3], axis=0) * np.stack([1 - sx, sx, 1 - sy, sy], axis=0), axis=0)

# Инициализация игрового поля шумом Перлина
x = np.linspace(0, 1, grid_size)
y = np.linspace(0, 1, grid_size)
emotional_grid = perlin_noise(x, y)

# Функция для применения гомотопии между эмоциями
def emotional_homotopy(t, emotion1, emotion2):
    return (1 - t) * emotion1 + t * emotion2  # добавлены знаки умножения

# Функция для шага игры
def game_step(emotional_grid, player_position):
    new_emotional_grid = emotional_grid.copy()

    # Применение гомотопии к соседним клеткам
    for x in range(max(0, player_position[0] - 1), min(grid_size, player_position[0] + 2)):
        for y in range(max(0, player_position[1] - 1), min(grid_size, player_position[1] + 2)):
            if x != player_position[0] or y != player_position[1]:
                t = np.random.rand()  # случайный параметр гомотопии
                new_emotional_grid[player_position[0], player_position[1]] = emotional_homotopy(t, emotional_grid[player_position[0], player_position[1]], emotional_grid[x, y])

    return new_emotional_grid

# Инициализация pygame
pygame.init()
screen = pygame.display.set_mode((grid_size * cell_size, grid_size * cell_size))  # исправлено умножение
clock = pygame.time.Clock()

# Игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_position = player_position + np.array([0, -player_speed])  # использование np.array
            elif event.key == pygame.K_DOWN:
                player_position = player_position + np.array([0, player_speed])
            elif event.key == pygame.K_LEFT:
                player_position = player_position + np.array([-player_speed, 0])
            elif event.key == pygame.K_RIGHT:
                player_position = player_position + np.array([player_speed, 0])

    # Отображение текущего состояния игрового поля
    print(f"Форма emotional_grid: {emotional_grid.shape}")

    for i in range(grid_size):
        for j in range(grid_size):
            # Ограничиваем значение emotional_grid[i, j] диапазоном от 0 до 1
            print("i:", i, "j:", j)
            value = np.clip(emotional_grid[i, j], 0, 1)
            color = (int(value * 255), 0, 0)
            pygame.draw.rect(screen, color, (i * cell_size, j * cell_size, cell_size, cell_size))


    # Отображение игрока
    pygame.draw.rect(screen, (0, 255, 0), (player_position[0] * cell_size, player_position[1] * cell_size, cell_size, cell_size))  # исправлено умножение

    pygame.display.flip()
    emotional_grid = game_step(emotional_grid, player_position)
    clock.tick(2)  # Частота обновления поля (2 раза в секунду)

# Завершение pygame
pygame.quit()





