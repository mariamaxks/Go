import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from progect_go import Go
# импортируем класс и тд


class Play(QMainWindow):
    # задаем переменные; создаем игровую доску вызовом класса
    def __init__(self):
        self.board_ui = []
        self.board = Go(5, 0)
        super().__init__()
        uic.loadUi('design_go_ui.ui', self)
        # используем готовый дизайн
        self.board_matrix = [[self.pb11, self.pb21, self.pb31, self.pb41, self.pb51],
                             [self.pb12, self.pb22, self.pb32, self.pb42, self.pb52],
                             [self.pb13, self.pb23, self.pb33, self.pb43, self.pb53],
                             [self.pb14, self.pb24, self.pb34, self.pb44, self.pb54],
                             [self.pb15, self.pb25, self.pb35, self.pb45, self.pb55]]
        for x in self.board_matrix:
            for y in x:
                y.clicked.connect(self.run)
        self.b_alarm.clicked.connect(self.passed)
        # подключаем активные в игре кнопки
        self.show()

    def run(self):
        run_button: str = str(self.sender().objectName())
        # выясняем название нажатой на ходу кнопки
        run_b = run_button[2::]
        x, y = int(run_b[0]), int(run_b[1])
        # получаем из названия кнопки координаты камешка в self.board класса Go
        result = self.board.move(y - 1, x - 1)
        # делаем ход, преобразуя х и у в координаты на self.board
        self.board_ui = result[0]
        # вычленяем из вывода хода модифицированную доску
        for x in range(len(self.board_matrix)):
            for y in range(len(self.board_matrix[x])):
                # итерируем по доске и изменяем текст на игровом поле соответственно ->
                if self.board_ui[x][y] == 0:
                    self.board_matrix[x][y].setText("-")
                elif self.board_ui[x][y] == 1:
                    self.board_matrix[x][y].setText("●")
                elif self.board_ui[x][y] == -1:
                    self.board_matrix[x][y].setText("⭕")
        self.count_black.setText(str(result[1]))
        # обновляем счет черных
        self.count_white.setText(str(result[2]))
        # обновляем счет белых
        if result[3] == 1:
            # (ПЕРЕДАЧА ХОДА)- обновляем значение цвета текущего хода ->
            self.color_play.setText("ЧЕРНЫЕ")
        else:
            self.color_play.setText("БЕЛЫЕ")

    def passed(self):
        # (ПЕРЕДАЧА ХОДА)- обновляем значение цвета текущего хода ->
        result = self.board.move(-1, -1)
        if result[3] == 1:
            self.color_play.setText("ЧЕРНЫЕ")
        else:
            self.color_play.setText("БЕЛЫЕ")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Play()
    sys.exit(app.exec_())
else:
    print(__name__)