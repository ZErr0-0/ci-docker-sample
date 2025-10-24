import os
import sys

def dop_cell(cell):
    if len(cell) != 2:
        return False
    if not ('A' <= cell[0] <= 'H' or 'a' <= cell[0] <= 'h'):
        return False
    if not ('1' <= cell[1] <= '8'):
        return False
    return True

def _figure_(figure):
    valid_figures = ["ферзь", "ладья", "слон", "конь"]
    return figure.lower() in valid_figures

def coords(cell):
    letter_to_num = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
    x = letter_to_num[cell[0].upper()]
    y = int(cell[1]) - 1
    return x, y

def coords2(x, y):
    num_to_letter = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}
    return num_to_letter[x] + str(y + 1)

def same_color(cell1, cell2):
    x1, y1 = coords(cell1)
    x2, y2 = coords(cell2)
    return (x1 + y1) % 2 == (x2 + y2) % 2

def risk(figure, cell1, cell2):
    x1, y1 = coords(cell1)
    x2, y2 = coords(cell2)

    if figure.lower() == "ферзь":
        return x1 == x2 or y1 == y2 or abs(x1 - x2) == abs(y1 - y2)
    elif figure.lower() == "ладья":
        return x1 == x2 or y1 == y2
    elif figure.lower() == "слон":
        return abs(x1 - x2) == abs(y1 - y2)
    elif figure.lower() == "конь":
        return (abs(x1 - x2), abs(y1 - y2)) in [(2, 1), (1, 2)]
    else:
        return False

def possible_moves(figure, cell):
    x, y = coords(cell)
    moves = []

    if figure.lower() == "ферзь":
        for i in range(8):
            if i != y:
                moves.append(coords2(x, i))
            if i != x:
                moves.append(coords2(i, y))
        for i in range(1, 8):
            if 0 <= x + i < 8 and 0 <= y + i < 8:
                moves.append(coords2(x + i, y + i))
            if 0 <= x - i < 8 and 0 <= y - i < 8:
                moves.append(coords2(x - i, y - i))
            if 0 <= x + i < 8 and 0 <= y - i < 8:
                moves.append(coords2(x + i, y - i))
            if 0 <= x - i < 8 and 0 <= y + i < 8:
                moves.append(coords2(x - i, y + i))

    elif figure.lower() == "ладья":
        for i in range(8):
            if i != y:
                moves.append(coords2(x, i))
            if i != x:
                moves.append(coords2(i, y))

    elif figure.lower() == "слон":
        for i in range(1, 8):
            if 0 <= x + i < 8 and 0 <= y + i < 8:
                moves.append(coords2(x + i, y + i))
            if 0 <= x - i < 8 and 0 <= y - i < 8:
                moves.append(coords2(x - i, y - i))
            if 0 <= x + i < 8 and 0 <= y - i < 8:
                moves.append(coords2(x + i, y - i))
            if 0 <= x - i < 8 and 0 <= y + i < 8:
                moves.append(coords2(x - i, y + i))

    elif figure.lower() == "конь":
        knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                        (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for dx, dy in knight_moves:
            if 0 <= x + dx < 8 and 0 <= y + dy < 8:
                moves.append(coords2(x + dx, y + dy))

    return moves


# --- основной блок ---
def main():
    # читаем переменные окружения
    kv1 = os.getenv("CELL_1")
    kv2 = os.getenv("CELL_2")
    figure = os.getenv("FIGURE")

    # если нет — спрашиваем вручную
    if not kv1:
        kv1 = input('введите первую клетку (например, A1): ')
    if not dop_cell(kv1):
        print("ошибка: Некорректная клетка.")
        sys.exit(1)

    if not kv2:
        kv2 = input('введите вторую клетку (например, A1): ')
    if not dop_cell(kv2):
        print("ошибка: Некорректная клетка.")
        sys.exit(1)

    if not figure:
        figure = input("введите название фигуры (ферзь, ладья, слон, конь): ")
    if not _figure_(figure):
        print("ошибка: некорректное название фигуры.")
        sys.exit(1)

    print(f"клетки {kv1} и {kv2} одного цвета:", same_color(kv1, kv2))
    print(f"фигура {figure} угрожает клетке {kv2}:", risk(figure, kv1, kv2))
    print(f"возможные ходы для фигуры {figure} из клетки {kv1}:", possible_moves(figure, kv1))


if __name__ == "__main__":
    main()
