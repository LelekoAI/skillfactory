from random import randint
import enum
import time


class Dot:  # Класс точек на поле
    def __init__(self, x, y):
        self.x: int = x
        self.y: int = y

    def __eq__(self, other: any):  # Метод для проверки принадлежности точки
        # типизируем other(Ограничили)
        if type(self) != type(other):
            return False
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class ShotType(enum.Enum):
    miss: int = 1
    hit: int = 2
    kill: int = 3


class Tools:
# удаляет повторяющиеся точки
    @staticmethod
    def distinct(values: list[Dot]) -> list[Dot]:
        element1: int = 0
        while element1 <= len(values) - 1:
            element2: int = element1 + 1
            while element2 <= (len(values) - 1):
                if values[element1] == values[element2]:
                    del values[element2]
                    continue
                element2 += 1
            element1 += 1
        return values


class Board:
    def __init__(self, size: int, ships_size: list[int]):
        self.size: int = size
        self.ships_size: list[int] = ships_size
        self.ship_symbol = '■'
        self.ship_hit_symbol = 'x'
        self.empty_symbol = ' '
        self.miss_symbol = '.'

# метод возвращающий точки корабля, если он на поле иначе пустой массив
    def generate_ship_points(self, length: int) -> list[Dot]:
        ship_dot: list[Dot] = []
        orient: int = randint(0, 1)
        bow: Dot = Dot(randint(0, 6), randint(0, 6))
        ship_dot.append(bow)
        for index in range(length - 1):
            if orient == 0:
                ship_dot.append(Dot(ship_dot[index].x + 1, ship_dot[index].y))
            else:
                ship_dot.append(Dot(ship_dot[index].x, ship_dot[index].y + 1))
        if ship_dot[len(ship_dot) - 1].x >= self.size or ship_dot[len(ship_dot) - 1].y >= self.size:
            return []
        return ship_dot

# получаем список занятых точек вокруг точки корабля
    def counter(self, point: Dot) -> list[Dot]:
        counter_dots: list[list[int]] = [[-1, -1], [0, -1], [1, -1],
                                         [-1, 0], [0, 0], [1, 0],
                                         [-1, 1], [0, 1], [1, 1]]
        busy: list[Dot] = []
        for index in range(len(counter_dots)):
            delta_dot: Dot = Dot(counter_dots[index][0], counter_dots[index][1])
            busy_x: int = point.x + delta_dot.x
            busy_y: int = point.y + delta_dot.y
            if busy_x < 0 or busy_y >= self.size:
                continue
            elif busy_y < 0 or busy_y >= self.size:
                continue
            busy.append(Dot(busy_x, busy_y))
        return busy

# олучаем список всех занятых точек вокруг корабля
    def counter_ship(self, ship_dots: list[Dot]) -> list[Dot]:
        ship_counter: list[Dot] = []
        for ship_dot in ship_dots:
            for point in Board(self.size, self.ships_size).counter(ship_dot):
                ship_counter.append(point)
        return Tools.distinct(ship_counter)

# получаем список всех занятых точек всех кораблей
    def counter_ships(self, ships_dots: list[list[Dot]]) -> list[Dot]:
        ships_counter: list[Dot] = []
        for ship_dots in ships_dots:
            for point in Board(self.size, self.ships_size).counter_ship(ship_dots):
                ships_counter.append(point)
        return Tools.distinct(ships_counter)

# возвращает свободные точки на поле
    def free_space_to_ship(self, ships_dots: list[list[Dot]]) -> list[Dot]:
        busy_points: list[Dot] = Board(self.size, self.ships_size).counter_ships(ships_dots)
        free_ship_dots: list[Dot] = []
        for column in range(self.size):
            for row in range(self.size):
                point: Dot = Dot(column, row)
                if point in busy_points:
                    continue
                free_ship_dots.append(point)
        return free_ship_dots

# генерируем список кораблей на поле
    def ship_generetor(self) -> list[list[Dot]]:
        while True:
            ships_dots: list[list[Dot]] = []
            can_generate: bool = True
            for ship_size in self.ships_size:
                free_space: list[Dot] = Board(self.size, self.ships_size).free_space_to_ship(ships_dots)
                count_generate: int = 0
                while True:
                    count_generate += 1
                    if count_generate > 1000:
                        can_generate = False
                        break
                    ship_points: list[Dot] = Board(self.size, self.ships_size).generate_ship_points(ship_size)
                    if len(ship_points) == 0:
                        continue

                    ship_in_free_space: bool = True
                    for element in ship_points:
                        ship_in_free_space = element in free_space
                        if not ship_in_free_space:
                            break
                    if not ship_in_free_space:
                        continue

                    ships_dots.append(ship_points)
                    break
                if not can_generate:
                    break
            if can_generate:
                break
        return ships_dots

# определяет каким элементом будет отрисован каждый элемент массива доски
    def draw_ships_str(self, ships_dots: list[list[Dot]], shoot_dots: list[Dot], show_ship: bool = True) -> list[str]:
        str_list: list[str] = []
        str_list.append('-' * 26)
        str_list.append(' | 1 | 2 | 3 | 4 | 5 | 6 |')
        str_list.append('-' * 26)
        dots: list[Dot] = []
        for ship_dots in ships_dots:
            for dot in ship_dots:
                dots.append(dot)
        for column in range(self.size):
            str_row: str = ''
            str_row += f'{column + 1}'
            for row in range(self.size):
                str_row += '| '
                field_dot: Dot = Dot(column, row)
                if field_dot in dots:
                    if field_dot in shoot_dots:
                        str_row += f'{self.ship_hit_symbol} '
                    else:
                        if show_ship:
                            str_row += f'{self.ship_symbol} '
                        else:
                            str_row += f'{self.empty_symbol} '
                else:
                    if field_dot in shoot_dots:
                        str_row += f'{self.miss_symbol} '
                    else:
                        str_row += f'{self.empty_symbol} '
            str_row += '|'
            str_list.append(str_row)
        return str_list

# функция отрисовка доски
    def draw_board(self, player_ships: list[list[Dot]], player_shoots: list[Dot],
                   ai_ships: list[list[Dot]], ai_shoots: list[Dot]):
        player_board: list[str] = Board(self.size, self.ships_size).draw_ships_str(player_ships, ai_shoots, True)
        ai_board: list[str] = Board(self.size, self.ships_size).draw_ships_str(ai_ships, player_shoots, True)
        for index in range(len(player_board)):
            print(player_board[index], '     ', ai_board[index])

class Movement:
    def __init__(self, ships_dots: list[list[Dot]], shoot_dots: list[Dot], size: int):
        self.shoot_dots: list[Dot] = shoot_dots
        self.ships_dots: list[list[Dot]] = ships_dots
        self.size = size

# возвращаем тип выстрела
    def shoot(self):
        last_shoot: Dot = self.shoot_dots[len(self.shoot_dots) - 1]
        for ship in self.ships_dots:
            if last_shoot not in ship:
                continue
            count: int = 0
            for element in range(len(ship)):
                if ship[element] not in self.shoot_dots:
                    break
                count += 1
            if count == len(ship):
                return ShotType.kill
            return ShotType.hit
        return ShotType.miss

# возвращает точку хода
    def step(self) -> Dot:
        while True:
            str_number: str = input('Введите координату выстрела: ')
            str_number = str_number.strip()
            if len(str_number) != 2:
                print('Неверный формат воода координаты.')
                continue
            if not str_number.isdigit():
                print('Неверный формат воода координаты.')
                continue
            coord: int = int(str_number)
            column: int = coord // 10
            row: int = coord % 10
            if row < 1 or row > 6:
                print('Неверный формат воода координаты.')
                continue
            if column < 1 or column > 6:
                print('Неверный формат воода координаты.')
                continue
            point: Dot = Dot(column - 1, row - 1)
            if point in self.shoot_dots:
                print('Вы сюда уже стреляли.')
                continue
            return point

# возвращает точку хода для ИИ
    def step_ai(self):
        while True:
            step_dot: Dot = Dot(randint(0, self.size - 1), randint(0, self.size - 1))
            if step_dot in self.shoot_dots:
                continue
            return step_dot

# возвращает список точек корабля который убит
    def ship_dots_by_shot(self, point: Dot) ->list[Dot]:
        for ship in self.ships_dots:
            if point in ship:
                return ship
        return []


class Player:
    def __init__(self, ships_dots: list[list[Dot]], shoot_dots: list[Dot]):
        self.ships_dots: list[list[Dot]] = ships_dots
        self.shoot_dots: list[Dot] = shoot_dots
        self.size: int = 6
        self.ships_size = [3, 2, 2, 1, 1, 1, 1]

# Возвращает тип выстрела игрока
    def player(self):
        movement: Movement = Movement(self.ships_dots, self.shoot_dots, self.size)
        steper: Dot = movement.step()
        self.shoot_dots.append(steper)
        shoot_type: ShotType = movement.shoot()
        if shoot_type == ShotType.kill:
            players_object = Board(self.size, self.ships_size)
            for dot in players_object.counter_ship(movement.ship_dots_by_shot(steper)):
                self.shoot_dots.append(dot)
        Tools.distinct(self.shoot_dots)
        return shoot_type

# Возвращает тип выстрела игрока
    def ai_player(self):
        movement: Movement = Movement(self.ships_dots, self.shoot_dots, self.size)
        steper: Dot = movement.step_ai()
        self.shoot_dots.append(steper)
        shoot_type: ShotType = movement.shoot()
        if shoot_type == ShotType.kill:
            ai_object = Board(self.size, self.ships_size)
            for dot in ai_object.counter_ship(movement.ship_dots_by_shot(steper)):
                self.shoot_dots.append(dot)
        Tools.distinct(self.shoot_dots)
        return shoot_type


class Logic:
    def __init__(self):
        self.ships_size = [3, 2, 2, 1, 1, 1, 1]
        self.size = 6

# возвращает True если все корабли подбиты, иначе False
    @staticmethod
    def all_ship_kill(ships_dots: list[list[Dot]], shoot_dots: list[Dot]) -> bool:
        all_kill: bool = True
        for ship in ships_dots:
            for dot in ship:
                if dot not in shoot_dots:
                    all_kill = False
                    break
            if not all_kill:
                break
        if all_kill:
            return True
        return False

# метод игровой логики
    def game_logic(self):
        player = Board(self.size, self.ships_size)
        ai = Board(self.size, self.ships_size)
        player_ships: list[list[Dot]] = player.ship_generetor()
        ai_ships: list[list[Dot]] = ai.ship_generetor()
        player_shoots: list[Dot] = []
        ai_shoots: list[Dot] = []
        Board(self.size, self.ships_size).draw_board(player_ships, player_shoots, ai_ships, ai_shoots)
        while True:
            any_win = False
            while True:
                print('Игрок ходит')
                shoot_type: ShotType = Player(ai_ships, player_shoots).player()
                Board(self.size, self.ships_size).draw_board(player_ships, player_shoots, ai_ships, ai_shoots)
                any_win = Logic().all_ship_kill(ai_ships, player_shoots)
                if any_win:
                    print('Выявлен победитель: игрок.')
                    break
                if shoot_type == ShotType.kill or shoot_type == ShotType.hit:
                    print('Игрок делает дополнительный ход.')
                    continue
                break
            if any_win:
                break

            while True:
                print('ИИ ходит.')
                shoot_type: ShotType = Player(player_ships, ai_shoots).ai_player()
                Board(self.size, self.ships_size).draw_board(player_ships, player_shoots, ai_ships, ai_shoots)
                any_win = Logic().all_ship_kill(player_ships, ai_shoots)
                if any_win:
                    print('Выявлен победитель: ИИ.')
                    break
                if shoot_type == ShotType.kill or shoot_type == ShotType.hit:
                    print('ИИ делает дополнительный ход.')
                    time.sleep(2)
                    continue
                break
            if any_win:
                break


if __name__ == '__main__':
    Logic().game_logic()
