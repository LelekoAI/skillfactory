battle_ground = [i for i in range(1, 10)]
new_ground = {}
player = ''


def printer():
    print(' ' + '-' * 13)
    for i in battle_ground:
        n = ' | ' + str(i) + ''
        if len(new_ground.keys()) >= 0:
            if i in new_ground.keys():
                n = ' | ' + str(new_ground[i]) + ''
            else:
                pass
        else:
            pass
        if i % 3 != 0:
            print(n, end='')
        else:
            print(n, '|')
    print(' ' + '-' * 13)


def winner():
    win_comb = [[1, 2, 3], [4, 5, 6], [7, 8, 9],
                [1, 4, 7], [2, 5, 8], [3, 6, 9],
                [1, 5, 9], [3, 5, 7]]
    x_list = [k for k in new_ground if new_ground[k] == "x"]
    o_list = [k for k in new_ground if new_ground[k] == "o"]
    for comb in win_comb:
        if comb[0] in x_list and comb[1] in x_list and comb[2] in x_list:
            return "x winner", x_list
        elif comb[0] in o_list and comb[1] in o_list and comb[2] in o_list:
            return "o winner", o_list
        elif len(new_ground.keys()) == 9:
            return 'победила дружба'
        else:
            pass


def next_stage():
    a = 'x'
    printer()
    b = int(input(f'ходит игрок {a} - '))
    if b in battle_ground and b not in new_ground.keys():
        pass
    else:
        b = int(input(f'неверный ход, повторите игрок {a} - '))
    new_ground[b] = a
    printer()
    while len(new_ground) < 9:
        if a == 'x':
            a = '0'
        elif a == '0':
            a = 'x'
        b = int(input(f'ходит игрок {a} - '))
        if b in battle_ground and b not in new_ground.keys():
            pass
        else:
            b = int(input(f'неверный ход, повторите игрок {a} - '))
        new_ground[b] = a
        printer()
        if winner() is not None:
            print(winner())
            break


next_stage()
