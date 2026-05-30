"""CLI dla projektu przeciecia odcinkow.

Obsluguje dwa tryby: argumenty (x1..y4) lub pytania o punkty A, B, C, D.
"""
import sys
from geometry import Point, Segment, intersect_segments

POINTS = (
    ('A', 'x1', 'y1'),
    ('B', 'x2', 'y2'),
    ('C', 'x3', 'y3'),
    ('D', 'x4', 'y4'),
)


def parse_float(value):
    # Akceptuj przecinek lub kropke jako separator dziesietny.
    return float(value.replace(',', '.'))


def parse_floats(args):
    # Wymagaj dokladnie osmiu wspolrzednych.
    if len(args) != 8:
        raise ValueError('oczekiwano 8 wartości liczbowych')
    return [parse_float(x) for x in args]


def read_points():
    # Czytanie punktow po kolei, wygodne na prezentacje.
    vals = []
    print('Podaj współrzędne punktów końcowych odcinków.')
    for point_name, x_name, y_name in POINTS:
        x = input(f'{point_name}.x ({x_name}): ').strip()
        y = input(f'{point_name}.y ({y_name}): ').strip()
        vals.extend([parse_float(x), parse_float(y)])
    return vals


def format_result(res):
    # Zamien wynik na przyjazny tekst.
    if not res['intersect']:
        return 'NIE'
    if res['type'] == 'point':
        x, y = res['point']
        return f'TAK - punkt: ({x:.6f}, {y:.6f})'
    if res['type'] == 'segment':
        (x1, y1), (x2, y2) = res['segment']
        return f'TAK - odcinek: ({x1:.6f}, {y1:.6f}) - ({x2:.6f}, {y2:.6f})'
    return 'NIE'


def main(argv=None):
    argv = argv or sys.argv[1:]
    try:
        vals = parse_floats(argv) if argv else read_points()
    except Exception as e:
        print('Błąd: nieprawidłowe dane wejściowe:', e)
        return 1

    x1, y1, x2, y2, x3, y3, x4, y4 = vals
    s1 = Segment(Point(x1, y1), Point(x2, y2))
    s2 = Segment(Point(x3, y3), Point(x4, y4))
    # Policz i wypisz przeciecie.
    res = intersect_segments(s1, s2)
    print(format_result(res))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
