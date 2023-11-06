class Go:
    def __init__(self, size, fora):
        # добавить к счету более слабой позиции (фору)
        self.size = size
        cord = []
        for x in range(size):
            col = []
            for y in range(size):
                col.append(0)
            cord.append(col)
            # создание пустой матрицы с нулями - доска
        self.board = cord
        self.black = []
        self.white = []
        self.groups = [self.black, self.white]
        # группа групп координат камней одного цвета -> [[координаты черных], [координаты белых]]
        self.current_color = -1
        self.alarm = False
        self.count_b = 0
        # вводим переменную-счетчик очков черных
        self.count_w = 0 + fora
        # по правилу Коми прибавляем к слабой позиции фору (к задаваемому счету очков белых)

    def move(self, x, y):
        # функция Ход, 1 = черные, -1 = белые
        while ((x != -1) and (y == -1)) or ((x == -1) and (y != -1)):
            self.alarm = True
        if not ((x == -1) and (y == -1)):
            self.alarm = False
            if self.board[x][y] == 0:
                # если клетка пустая -
                self.board[x][y] = self.current_color
                # заполнаем ее цветом-камешком данного хода (фишкой данного цвета, обозначения цветов -> 1 и -1
        self.check_groups()
        # выполнаем проверку на соседей и повтор одного и того же хода
        self.check_freedom()
        # выполняем проверку на степени свободы и снимаем некоторые камни, если нужно (у них степень свободы == 0)
        self.current_color = self.current_color * (-1)
        return [self.board, self.count_b, self.count_w, self.current_color]

    def check_groups(self):
        # создаем массивы всех групп(островки- камни с соседями) камней
        self.groups[0].clear()
        # чистим для данного хода координаты соседей (и черных, и белых)
        self.groups[1].clear()
        for x in range(self.size):
            for y in range(self.size):
                # итерируем по всем клеткам (позициям доски)
                if self.board[x][y] != 0:
                    # если клетка не пустая
                    if self.board[x][y] == 1:
                        # если она черная
                        group_number = 0
                        colour = 1
                    else:
                        # если она белая
                        group_number = 1
                        colour = -1
                        # новая переменная, не color!
                    accounted = 0
                    # проверка, что клетка еще не учтена в массиве групп [ ([x,y],[x1,y1]), ([...],[...]) ]
                    for group in self.groups[group_number]:
                        # ищем текущую клетку по всем островам
                        print(group)
                        if [x, y] in group:
                            accounted = 1
                            # уже учли
                    if accounted == 0:
                        # клетка ещё не учтена ->
                        main_group = [[x, y]]
                        # создаем новую группу [ -> [[x,y],[x1,y1]] <- , [[...],[...]] ]
                        current_group = [[x, y]]
                        # клетки у которых надо проверить соседей на этом шаге
                        new_group = []
                        # тут будут клетки у которых будем проверять соседей на следующем шаге, "соседи прежних клетки(ок)"
                        while current_group:
                            # пока клетки в данной группе не иссякли
                            for cell in current_group:
                                # итерируем по клеткам(их координатам)
                                nearby_cells = self.get_neighbours(cell[0], cell[1])
                                # получаем список соседей
                                for near_cell in nearby_cells:
                                    # итерируем по соседям из списка соседей
                                    if (self.board[near_cell[0]][near_cell[1]] == colour) and (
                                            near_cell not in main_group):
                                        # если цвет соседа совпадает с цветом данной клетки
                                        # и если клетки-соседа еще нет в группе клеток-соседей ->
                                        new_group.append(near_cell)
                                        # добавляем клетку-соседа в группу клеток-соседей
                            for i in current_group:
                                if i not in main_group:
                                    main_group.append(i)
                                    # добавляем все элементы из current_group в main_group (которых там еще нет)
                            current_group = new_group
                            # переопределяем current_group, присваивая значения "последующих" соседей(да)
                            new_group = []
                            # очищаем, потом снова присвоим значения клеток, у которых будем проверять соседей на следующем шаге, "соседей прежних клетки(ок)"
                        self.groups[group_number].append(
                            main_group)
                        # в массив групп по цвету добавляем новую группу клеток-соседей

    def get_neighbours(self, x, y):
        # получаем координаты всех соседей, по вертикали и горизонтали (без диагоналей)
        neighbours = []
        if x != 0:
            neighbours.append([x - 1, y])
        if x != self.size - 1:
            neighbours.append([x + 1, y])
        if y != 0:
            neighbours.append([x, y - 1])
        if y != self.size - 1:
            neighbours.append([x, y + 1])
        return neighbours

    def check_freedom(self):
        # провека степени свободы; по цвету текущего хода (цвет данного камешка)
        if self.current_color == 1:
            opposite_color = 1
            # координата противоположного цвета в self.groups
        elif self.current_color == -1:
            opposite_color = 0
            # координата противоположного цвета в self.groups
        for group in self.groups[opposite_color]:
            # итерируем по группам групп камешков противоположного цвета
            freedom = 0
            # объявляем минимальную степень свободы
            for i_cord in group:
                # для каждого элемента-координат в данной группе ->
                neighbours = self.get_neighbours(i_cord[0], i_cord[1])
                # находим координаты-соседей данного элемента
                for neigh in neighbours:
                    # итерируем по координатам-соседям
                    if self.board[neigh[0]][neigh[1]] == 0:
                        # если клетка координаты пустая-
                        freedom += 1
                        # добавляем единицу степени свободы
            if freedom == 0:
                # если степень свободы == 0 ->
                for i_cord in group:
                    self.boar[i_cord[0]][i_cord[1]] = 0
                    # снимаем группу камней(ня) с доски
                    # и прибавляем количество к счету цвета данного хода
                    if self.current_color == 1:
                        self.count_b += 1
                    else:
                        self.count_w += 1

    def __str__(self):
        # после каждого хода модифицируем таблицу (не поле!) и вносим новые данные о камешках
        obj = ''
        for x in self.board:
            for y in x:
                if y == 0:
                    obj += ' 0'
                if y == 1:
                    obj += ' 1'
                if y == -1:
                    obj += '-1'
            obj += '\n'
        obj += 'black\n'
        for x in self.black:
            obj += str(x) + '\n'
        obj += 'white\n'
        for x in self.white:
            obj += str(x) + '\n'
        return obj