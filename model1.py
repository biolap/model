import numpy as np
import pyqtgraph as pg
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsPolygonItem


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

# Создание сферы
app = QApplication([])
win = QMainWindow()
view = pg.GraphicsLayoutWidget()
win.setCentralWidget(view)
win.show()

# Создание сцены
scene = view.addPlot()
scene.setAspectLocked(True)

# Создание многоугольников на сфере
polygons = []
for i in range(grid_size):
    for j in range(grid_size):
        x = i / grid_size
        y = j / grid_size
        z = emotional_grid[i, j]
        color = pg.intColor(z * 255)
        polygon = QGraphicsPolygonItem(
            QtGui.QPolygonF([
                QtCore.QPointF(x, y),
                QtCore.QPointF(x + 1 / grid_size, y),
                QtCore.QPointF(x + 1 / grid_size, y + 1 / grid_size),
                QtCore.QPointF(x, y + 1 / grid_size)
            ])
        )
        polygon.setBrush(pg.mkBrush(color))
        scene.addItem(polygon)
        polygons.append(polygon)

# Функция для обновления многоугольников
def update_polygons():
    global emotional_grid
    emotional_grid = game_step(emotional_grid)

    for i in range(grid_size):
        for j in range(grid_size):
            polygon = polygons[i * grid_size + j]
            z = emotional_grid[i, j]
            color = pg.intColor(z * 255)
            polygon.setBrush(pg.mkBrush(color))

# Игровой цикл
timer = pg.QtCore.QTimer()
timer.timeout.connect(update_polygons)
timer.start(1000)  # Частота обновления поля (1 раз в секунду)

# Запуск приложения
if __name__ == '__main__':
    app.exec_()
