import numpy as np
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
import pyqtgraph.opengl as gl

# Размер игрового поля
grid_size = 50

# Инициализация игрового поля случайными эмоциями
emotional_grid = np.random.uniform(low=0.0, high=1.0, size=(grid_size, grid_size))

# Создание приложения Qt
app = QApplication([])

# Создание трехмерного графика
view = gl.GLViewWidget()
view.show()
view.setWindowTitle('Emotional Sphere')

# Создание сетки для трехмерной сферы
theta = np.linspace(0, 2 * np.pi, grid_size + 1)
phi = np.linspace(0, np.pi, grid_size + 1)
theta, phi = np.meshgrid(theta, phi)

# Преобразование сферических координат в декартовы
x = np.sin(phi) * np.cos(theta)
y = np.sin(phi) * np.sin(theta)
z = np.cos(phi)

# Преобразование координат в одномерные массивы
x = x.flatten()
y = y.flatten()
z = z.flatten()

# Создание объекта для отображения многоугольников
mesh = gl.GLMeshItem(vertexes=np.vstack([x, y, z]).T, faces=np.arange(len(x)).reshape(grid_size+1, grid_size+1),
                     shader='shaded', smooth=True)

# Добавление объекта на сцену
view.addItem(mesh)

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

# Функция для обновления графика

def update():
    global emotional_grid
    emotional_grid = game_step(emotional_grid)

# Обновление цветов многоугольников
vertex_colors = np.zeros((grid_size+1, grid_size+1, 4))
vertex_colors[:-1, :-1, 0] = emotional_grid  # Красный канал
vertex_colors[:, :, 3] = 1.0  # Альфа-канал

# Добавим проверку на деление на ноль
norm = np.linalg.norm(np.vstack([x, y, z]), axis=0)
norm = norm / np.where(norm**2 != 0, (norm**2).sum()**0.5, 1)

mesh.setMeshData(vertexes=np.vstack([x, y, z]).T, faces=np.arange(len(x)).reshape(grid_size+1, grid_size+1),
                 shader='shaded', smooth=True, vertexColors=vertex_colors)





# Таймер для обновления
timer = QTimer()
timer.timeout.connect(update)
timer.start(1000)  # Частота обновления поля (1 раз в секунду)

# Запуск приложения
if __name__ == '__main__':
    QApplication.instance().exec_()


