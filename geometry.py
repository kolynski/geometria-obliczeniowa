"""Funkcje geometryczne do przeciecia odcinkow.

Implementuje odporne numerycznie przeciecie odcinkow 2D i zwraca brak
przeciecia, pojedynczy punkt albo wspolny odcinek.
"""
from dataclasses import dataclass
from typing import Tuple, Optional, Dict

# Tolerancja uzywana w porownaniach zmiennoprzecinkowych.
EPS = 1e-9


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class Segment:
    a: Point
    b: Point


def _orient(a: Point, b: Point, c: Point) -> float:
    """Return orientation value (cross product) of (b-a) x (c-a)."""
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)


def _on_segment(a: Point, b: Point, p: Point) -> bool:
    """Check if point p lies on segment ab (inclusive)."""
    if abs(_orient(a, b, p)) > EPS:
        return False
    return (min(a.x, b.x) - EPS <= p.x <= max(a.x, b.x) + EPS and
            min(a.y, b.y) - EPS <= p.y <= max(a.y, b.y) + EPS)


def _approx_equal(a: float, b: float) -> bool:
    # Porownanie z tolerancja EPS dla skalarow i wspolrzednych.
    return abs(a - b) <= EPS


def _segment_overlap_1d(a1: float, a2: float, b1: float, b2: float) -> Optional[Tuple[float, float]]:
    """Return overlap interval in 1D or None."""
    lo = max(min(a1, a2), min(b1, b2))
    hi = min(max(a1, a2), max(b1, b2))
    if lo <= hi + EPS:
        return (lo, hi)
    return None


def _intersection_segment_or_point(p1: Point, p2: Point) -> Dict[str, object]:
    # Sprowadz do punktu, gdy dlugosc pokrycia wynosi zero.
    if _approx_equal(p1.x, p2.x) and _approx_equal(p1.y, p2.y):
        return {'intersect': True, 'type': 'point', 'point': (p1.x, p1.y)}
    return {'intersect': True, 'type': 'segment', 'segment': ((p1.x, p1.y), (p2.x, p2.y))}


def _intersection_point(s1: Segment, s2: Segment) -> Optional[Point]:
    """Compute intersection point of lines (not segments). Returns Point or None if parallel."""
    x1, y1 = s1.a.x, s1.a.y
    x2, y2 = s1.b.x, s1.b.y
    x3, y3 = s2.a.x, s2.a.y
    x4, y4 = s2.b.x, s2.b.y
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < EPS:
        return None
    px = ((x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / denom
    py = ((x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)) / denom
    return Point(px, py)


def intersect_segments(s1: Segment, s2: Segment) -> Dict[str, object]:
    """Determine intersection between two segments.

    Returns a dictionary with keys:
      - 'intersect': bool
      - 'type': 'point'|'segment'|'none'
      - 'point': (x,y) if type == 'point'
      - 'segment': ((x1,y1),(x2,y2)) if type == 'segment'
    """
    a, b = s1.a, s1.b
    c, d = s2.a, s2.b
    o1 = _orient(a, b, c)
    o2 = _orient(a, b, d)
    o3 = _orient(c, d, a)
    o4 = _orient(c, d, b)

    # Przypadek ogolny: poprawne przeciecie (odcinki sie przecinaja).
    if o1 * o2 < -EPS and o3 * o4 < -EPS:
        p = _intersection_point(s1, s2)
        if p is None:
            return {'intersect': True, 'type': 'point', 'point': (float('nan'), float('nan'))}
        return {'intersect': True, 'type': 'point', 'point': (p.x, p.y)}

    # Przypadek wspoliniowy: wszystkie orientacje ~0.
    if abs(o1) <= EPS and abs(o2) <= EPS and abs(o3) <= EPS and abs(o4) <= EPS:
        # Rzut do 1D, aby znalezc wspolny przedzial na osi X lub Y.
        if not _approx_equal(a.x, b.x):
            interval = _segment_overlap_1d(a.x, b.x, c.x, d.x)
            if interval is None:
                return {'intersect': False, 'type': 'none'}
            xlo, xhi = interval
            def y_at(s: Segment, x):
                # Interpolacja liniowa na odcinku dla y(x).
                if abs(s.a.x - s.b.x) < EPS:
                    return min(s.a.y, s.b.y)
                t = (x - s.a.x) / (s.b.x - s.a.x)
                return s.a.y + t * (s.b.y - s.a.y)
            p1 = Point(xlo, y_at(s1, xlo))
            p2 = Point(xhi, y_at(s1, xhi))
            return _intersection_segment_or_point(p1, p2)
        else:
            interval = _segment_overlap_1d(a.y, b.y, c.y, d.y)
            if interval is None:
                return {'intersect': False, 'type': 'none'}
            ylo, yhi = interval
            p1 = Point(a.x, ylo)
            p2 = Point(a.x, yhi)
            return _intersection_segment_or_point(p1, p2)

    # Przypadki szczegolne: dotkniecie koncami poza wspoliniowoscia.
    if _on_segment(a, b, c):
        return {'intersect': True, 'type': 'point', 'point': (c.x, c.y)}
    if _on_segment(a, b, d):
        return {'intersect': True, 'type': 'point', 'point': (d.x, d.y)}
    if _on_segment(c, d, a):
        return {'intersect': True, 'type': 'point', 'point': (a.x, a.y)}
    if _on_segment(c, d, b):
        return {'intersect': True, 'type': 'point', 'point': (b.x, b.y)}

    return {'intersect': False, 'type': 'none'}


if __name__ == '__main__':
    # quick manual test
    s1 = Segment(Point(0, 0), Point(2, 2))
    s2 = Segment(Point(0, 2), Point(2, 0))
    print(intersect_segments(s1, s2))
