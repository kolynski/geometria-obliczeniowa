from geometry import Point, Segment, intersect_segments


def test_crossing_point():
    s1 = Segment(Point(0, 0), Point(2, 2))
    s2 = Segment(Point(0, 2), Point(2, 0))
    r = intersect_segments(s1, s2)
    assert r['intersect'] and r['type'] == 'point'
    x, y = r['point']
    assert abs(x - 1) < 1e-6 and abs(y - 1) < 1e-6


def test_no_intersection_parallel():
    s1 = Segment(Point(0, 0), Point(1, 0))
    s2 = Segment(Point(0, 1), Point(1, 1))
    r = intersect_segments(s1, s2)
    assert not r['intersect']


def test_overlap_segment():
    s1 = Segment(Point(0, 0), Point(4, 0))
    s2 = Segment(Point(2, 0), Point(6, 0))
    r = intersect_segments(s1, s2)
    assert r['intersect'] and r['type'] == 'segment'
    (x1, y1), (x2, y2) = r['segment']
    assert abs(x1 - 2) < 1e-6 and abs(x2 - 4) < 1e-6


def test_touch_endpoint():
    s1 = Segment(Point(0, 0), Point(1, 1))
    s2 = Segment(Point(1, 1), Point(2, 3))
    r = intersect_segments(s1, s2)
    assert r['intersect'] and r['type'] == 'point'
    x, y = r['point']
    assert abs(x - 1) < 1e-6 and abs(y - 1) < 1e-6
