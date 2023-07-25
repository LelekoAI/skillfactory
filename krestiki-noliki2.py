# игровое поле
board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
board_size = 3


# выводим игровое поле
def genboard():
    print('-' * 13)
    for i in range(board_size):
        print('|', board[i * 3], '|', board[1 + i * 3], '|', board[2 + i * 3], '|')
        print('-' * 13)
    pass


# выполнение хода
def next_step(step_index, char):
    if step_index > 9 or step_index < 1 or board[step_index - 1] in ('x', 'o'):
        return False
    board[step_index-1] = char
    return True


# проверка комбинаций
def check_comb():
    # Проверяем все возможные комбинации победы
    win = '\0'
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Горизонтали
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Вертикали
        [0, 4, 8], [2, 4, 6]  # Диагонали
    ]
    for combination in win_combinations:
        if board[combination[0]] == board[combination[1]] == board[combination[2]]:
            win = board[combination[0]]

    return win


# игра
def play_game():
    # текущий игрок
    current_player = 'x'
    # номер шага
    step = 1
    genboard()
    while (step <= 9) and (check_comb() == '\0'):
        step_index = int(input('ходит игрок ' + current_player + '. Введите номер поля:'))
        if step_index == '0':
            break
        # если получилось походить
        if next_step(int(step_index), current_player):
            print('ход сделан')
            genboard()
            step += 1
            # подмена символа и игрока
            if current_player == 'x':
                current_player = 'o'
            else:
                current_player = 'x'
        else:
            print('неверный ход! повторите!')
        next_step(step_index, current_player)
    if step == 10:
        print('игра окончена. Ничья!')
    else:
        print('выиграл ' + check_comb())


print('Давай поиграем в крестики нолики')
play_game()
