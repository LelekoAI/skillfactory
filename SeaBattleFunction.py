from random import randint
import enum
import time


size: int = 6
ship_size: list[int] = [3, 2, 2, 1, 1, 1, 1]

ship_symbol = '■'
ship_hit_symbol = 'x'
empty_symbol = ' '
miss_symbol = '.'


class ShotType(enum.Enum):
    miss: int = 1
    hit: int = 2
    kill: int = 3


# возвращает точки корабля, если он на поле иначе пустой массив
def generate_ship_points(length: int) -> list[list[int]]:
    ship_dot: list[list[int]] = []
    orient: int = randint(0, 1)
    bow: list[int] = [randint(0, 6), randint(0, 6)]
    ship_dot.append(bow)
    for index in range(length - 1):
        if orient == 0:
            ship_dot.append([ship_dot[index][0] + 1, ship_dot[index][1]])
        else:
            ship_dot.append([ship_dot[index][0], ship_dot[index][1] + 1])
    if ship_dot[len(ship_dot) - 1][0] >= size or ship_dot[len(ship_dot) - 1][1] >= size:
        return []
    return ship_dot


# получаем список занятых точек вокруг точки корабля
def counter(x: int, y: int) -> list[list[int]]:
    counter_dots: list[list[int]] = [[-1, -1], [0, -1], [1, -1],
                    [-1, 0], [0, 0], [1, 0],
                    [-1, 1], [0, 1], [1, 1]]
    busy: list[list[int]] = []
    for index in range(len(counter_dots)):
        delta_dot: list[int] = counter_dots[index]
        busy_x: int = x + delta_dot[0]
        busy_y: int = y + delta_dot[1]
        if busy_x < 0 or busy_x >= size:
            continue
        if busy_y < 0 or busy_y >= size:
            continue
        busy.append([busy_x, busy_y])
    return busy


# получение всех занятых точек вокруг корабля
def counter_ship(ship_dots: list[list[int]]) -> list[list[int]]:
    ship_counter: list[list[int]] = []
    for ship_dot in ship_dots:
        for dot in counter(ship_dot[0], ship_dot[1]):
            ship_counter.append(dot)
    return distinct(ship_counter)


# получение всех занятых точек нескольких кораблей
def counter_ships(ships_dots: list[list[list[int]]]) -> list[list[int]]:
    ships_counter: list[list[int]] = []
    for ship_dots in ships_dots:
        for dot in counter_ship(ship_dots):
            ships_counter.append(dot)
    return distinct(ships_counter)


# возвращает свободные точки на поле
def free_space_to_ship(ships_dots: list[list[list[int]]]) -> list[list[int]]:
    # получить контура кораблей
    # сгенерировать одну точку поля
    # проверить что точка не в контурах кораблей
    # добавить точку в список свободных
    busy_points: list[list[int]] = counter_ships(ships_dots)
    free_ship_dots: list[list[int]] = []
    for column in range(size):
        for row in range(size):
            bow: list[int] = [column, row]
            if bow in busy_points:
                continue
            free_ship_dots.append(bow)
    return free_ship_dots


# удаляет повторяющиеся значения
def distinct(values: list[list[int]]) -> list[list[int]]:
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


# генерирует список кораблей на поле
def ship_generator(ships_size: list[int]) -> list[list[list[int]]]:
    # создаём пустую переменную для точек кораблей
    # заходим в бесконечный цикл в котором выставляем корабль если он в свободном пространстве
    # если корабль в свободном пространстве добавляем его в переменную для точек кораблей
    while True:
        ships_dots: list[list[list[int]]] = []
        can_generate: bool = True
        for ship_size in ships_size:
            free_space: list[list[int]] = free_space_to_ship(ships_dots)
            count_generate: int = 0
            while True:
                count_generate += 1
                if count_generate > 1000:
                    can_generate = False
                    break
                ship_points: list[list[int]] = generate_ship_points(ship_size)
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


# отрисовка списка точек кораблей
def draw_ships_str(ships_dots: list[list[list[int]]], shoot_dots: list[list[int]], show_ship: bool = True) -> list[str]:
    # проходим по каждой коллоне и строчке размера поля
    # проверяем есть ли корабль с такой точкой
    # oтрисовываем корабль или пустое место
    str_list: list[str] = []
    str_list.append('-' * 26)
    str_list.append(' | 1 | 2 | 3 | 4 | 5 | 6 |')
    str_list.append('-' * 26)
    dots: list[list[int]] = []
    for ship_dots in ships_dots:
        for dot in ship_dots:
            dots.append(dot)
    for column in range(size):
        str_row: str = ''
        str_row += f'{column + 1}'
        for row in range(size):
            str_row += '| '
            field_dot: list[int] = [column, row]
            if field_dot in dots:
                if field_dot in shoot_dots:
                    str_row += f'{ship_hit_symbol} '
                else:
                    if show_ship:
                        str_row += f'{ship_symbol} '
                    else:
                        str_row += f'{empty_symbol} '
            else:
                if field_dot in shoot_dots:
                    str_row += f'{miss_symbol} '
                else:
                    str_row += f'{empty_symbol} '
        str_row += '|'
        str_list.append(str_row)
    return str_list


# мы берём последний элемент shoot dots
# сравниваемые с точками каждого корабля в списке кораблей
# если последний элемент shoot dots в есть в точках какого-либо корабля
# то проверяем остальные элемент shoot dots c точками корабля
# и далее исходя из совпадений возвращаем shottype
def shoot(ships_dots: list[list[list[int]]], shoot_dots: list[list[int]]) -> ShotType:
    last_shoot: list[int] = shoot_dots[len(shoot_dots) - 1]
    for ship in ships_dots:
        if last_shoot not in ship:
            continue
        count: int = 0
        for element in range(len(ship)):
            if ship[element] not in shoot_dots:
                break
            count += 1
        if count == len(ship):
            return ShotType.kill
        return ShotType.hit
    return ShotType.miss


# принимает списки кораблей и списки выстрелов и отрисовывает доски построчно в цикле
def draw_board(player_ships: list[list[list[int]]], player_shoots: list[list[int]],
               ai_ships: list[list[list[int]]], ai_shoots: list[list[int]]):
    player_board: list[str] = draw_ships_str(player_ships, ai_shoots, True)
    ai_board: list[str] = draw_ships_str(ai_ships, player_shoots, False)
    for index in range(len(player_board)):
        print(player_board[index], '     ', ai_board[index])


# осуществление хода
# в него передаём список выстрелов
# возвращает точку хода
def step(shoot_dots: list[list[int]]) -> list[int]:
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
        dota: list[int] = [column - 1, row - 1]
        if dota in shoot_dots:
            print('Вы сюда уже стреляли.')
            continue
        return dota


def step_ai(shoot_dots: list[list[int]]) -> list[int]:
    while True:
        step_dot: list[int] = [randint(0, size - 1), randint(0, size - 1)]
        if step_dot in shoot_dots:
            continue
        return step_dot


# возвращает список точек корабля который убит
# получает точку выстрела, список точек кораблей
def ship_dots_by_shot(shoot: list[int], ships_dots: list[list[list[int]]]) -> list[list[int]]:
    for ship in ships_dots:
        if shoot in ship:
            return ship
    return [[]]


# вызывает метод степ чтобы получить точку выстрела
# вызывает метод шут чтобы понять попал не попал и что делать
# если попал или убил пользователь ходит ещё раз
# если выстрелом корабль убит то вызвает ship_counter чтобы получить контур корабля
def player(ships_dots: list[list[list[int]]], shoot_dots: list[list[int]]) -> ShotType:
    steper: list[int] = step(shoot_dots)
    shoot_dots.append(steper)
    shoot_type: ShotType = shoot(ships_dots, shoot_dots)
    if shoot_type == ShotType.kill:
        for dot in counter_ship(ship_dots_by_shot(steper, ships_dots)):
            shoot_dots.append(dot)
    distinct(shoot_dots)
    return shoot_type


def ai_player(ships_dots: list[list[list[int]]], shoot_dots: list[list[int]]) -> ShotType:
    steper: list[int] = step_ai(shoot_dots)
    shoot_dots.append(steper)
    shoot_type: ShotType = shoot(ships_dots, shoot_dots)
    if shoot_type == ShotType.kill:
        for dot in counter_ship(ship_dots_by_shot(steper, ships_dots)):
            shoot_dots.append(dot)
    distinct(shoot_dots)
    return shoot_type


# возвращает True если все корабли подбиты, иначе False
# получает ships_dots и shoot_dots
def all_ship_kill(ships_dots: list[list[list[int]]], shoot_dots: list[list[int]]) -> bool:
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


# добавить условия выхода (победа поражение игрока)
# добавить повторные ходы
def logic():
    player_ships: list[list[list[int]]] = ship_generator(ship_size)
    ai_ships: list[list[list[int]]] = ship_generator(ship_size)
    player_shoots: list[list[int]] = []
    ai_shoots: list[list[int]] = []
    draw_board(player_ships, player_shoots, ai_ships, ai_shoots)
    while True:
        any_win = False
        while True:
            print('Игрок ходит.')
            shoot_type: ShotType = player(ai_ships, player_shoots)
            draw_board(player_ships, player_shoots, ai_ships, ai_shoots)
            any_win = all_ship_kill(ai_ships, player_shoots)
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
            shoot_type: ShotType = ai_player(player_ships, ai_shoots)
            draw_board(player_ships, player_shoots, ai_ships, ai_shoots)
            any_win = all_ship_kill(player_ships, ai_shoots)
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
    logic()
