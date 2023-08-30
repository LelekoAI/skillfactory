from random import choice


def printer(battle, ground):
    print(' ' + '-' * 13)
    for i in battle:
        n = ' | ' + str(i) + ''
        if len(ground.keys()) >= 0:
            if i in ground.keys():
                n = ' | ' + str(ground[i]) + ''
        if i % 3 != 0:
            print(n, end='')
        else:
            print(n, '|')
    print(' ' + '-' * 13)


def winner(ground):
    win_comb = [[1, 2, 3], [4, 5, 6], [7, 8, 9],
                [1, 4, 7], [2, 5, 8], [3, 6, 9],
                [1, 5, 9], [3, 5, 7]]
    x_list = [k for k in ground if ground[k] == "x"]
    o_list = [k for k in ground if ground[k] == "o"]
    for comb in win_comb:
        if comb[0] in x_list and comb[1] in x_list and comb[2] in x_list:
            return "x winner", x_list
        elif comb[0] in o_list and comb[1] in o_list and comb[2] in o_list:
            return "o winner", o_list
        elif len(ground.keys()) == 9:
            return 'победила дружба'


def next_stage():
    battle = [i for i in range(1, 10)]
    ground = {}
    player = input('выберите x или o - ')
    if player not in ['x','o']:
        player = input('неверный выбор выберите x или o - ')
    count = 0
    printer(battle, ground)
    while len(ground) < 9:
        if player == 'x' and count % 2 == 0:
            b = int(input(f'ходит игрок {player} - '))
            if b not in battle and b in ground.keys():
                b = int(input(f'неверный ход, повторите игрок {player} - '))
            ground[b] = player
            printer(battle, ground)
            count += 1
            print('ходит искусственный интелект')
            shot = [elem for elem in battle if elem not in ground.keys()]
            b = choice(shot)
            ground[b] = 'o'
            printer(battle, ground)
            count += 1
        else:
            print('ходит искусственный интелект')
            shot = [elem for elem in battle if elem not in ground.keys()]
            b = choice(shot)
            ground[b] = 'x'
            printer(battle, ground)
            count += 1
            b = int(input(f'ходит игрок {player} - '))
            if b not in battle and b in ground.keys():
                b = int(input(f'неверный ход, повторите игрок {player} - '))
            ground[b] = player
            printer(battle, ground)
            count += 1
        if winner(ground) is not None:
            print(winner(ground))
            break


next_stage()
