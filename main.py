"""CLI for segment intersection project.

Usage examples:
  python main.py x1 y1 x2 y2 x3 y3 x4 y4
If no args provided, prompts the user for eight numbers.
"""
import sys
from geometry import Point, Segment, intersect_segments


def parse_floats(args):
    try:
        vals = [float(x) for x in args]
        if len(vals) != 8:
            raise ValueError('Expected 8 numeric values')
        return vals
    except ValueError as e:
        raise


def format_result(res):
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
    if not argv:
        s = input('Podaj 8 liczb (x1 y1 x2 y2 x3 y3 x4 y4):\n')
        argv = s.strip().split()
    try:
        vals = parse_floats(argv)
    except Exception as e:
        print('Błąd: nieprawidłowe dane wejściowe:', e)
        return 1
    x1, y1, x2, y2, x3, y3, x4, y4 = vals
    s1 = Segment(Point(x1, y1), Point(x2, y2))
    s2 = Segment(Point(x3, y3), Point(x4, y4))
    res = intersect_segments(s1, s2)
    print(format_result(res))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
