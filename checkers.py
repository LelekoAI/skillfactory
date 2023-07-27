board = [i+1 for i in range(64)]


def divide_array():
    newBoard = []
    referencePoint = 0
    while referencePoint < 64:
        newBoard.append(board[referencePoint:referencePoint + 8])
        referencePoint += 8
    return newBoard


def draw_board():
    superBoard = divide_array()
    m = 0
    n = 0
    d = '██'
    c = '  '
    for m in range(len(superBoard)):
        for n in range(len(superBoard[m])):
            if (m % 2 == 0) and (n % 2 == 0):
                print(d, end='')
            elif (m % 2 == 0) and (n % 2 != 0):
                print(c, end='')
            elif (m % 2 != 0) and (n % 2 != 0):
                print(d, end='')
            else:
                print(c, end='')
        print()


draw_board()
