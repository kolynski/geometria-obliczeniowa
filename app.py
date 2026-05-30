from flask import Flask, request, render_template_string, redirect, url_for
from geometry import Point, Segment, intersect_segments

app = Flask(__name__)

INDEX_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Przecięcie odcinków</title>
</head>
<body>
  <h1>Przecięcie odcinków</h1>
    <form method="post" action="/intersect">
        <p>Wprowadź współrzędne (x1 y1 x2 y2 x3 y3 x4 y4):</p>
        <input name="vals" size="80" value="{{ vals }}" />
        <button type="submit">Oblicz</button>
    </form>
    <form method="get" action="/" style="display:inline;margin-left:8px;">
        <button type="submit">Reset</button>
    </form>
  {% if result %}
    <h2>Wynik: {{ result_text }}</h2>
    <div>
      {{ svg|safe }}
    </div>
  {% endif %}
</body>
</html>
"""


def _make_svg(s1: Segment, s2: Segment, res) -> str:
    # bounding box
    xs = [s1.a.x, s1.b.x, s2.a.x, s2.b.x]
    ys = [s1.a.y, s1.b.y, s2.a.y, s2.b.y]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    # pad
    dx = maxx - minx or 1.0
    dy = maxy - miny or 1.0
    pad = 0.1 * max(dx, dy)
    minx -= pad; maxx += pad; miny -= pad; maxy += pad
    W = 500
    H = 500
    def tx(x):
        return (x - minx) / (maxx - minx) * W
    def ty(y):
        return H - (y - miny) / (maxy - miny) * H

    svg = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    # background
    svg.append(f'<rect width="100%" height="100%" fill="#f8f8f8" stroke="none"/>')

    # draw grid and axes with ticks
    import math
    def nice_step(span, target=10):
        raw = span / target if span > 0 else 1.0
        exp = math.floor(math.log10(raw))
        base = 10 ** exp
        for m in (1, 2, 5, 10):
            step = m * base
            if step >= raw:
                return step
        return 10 * base

    xstep = nice_step(maxx - minx)
    ystep = nice_step(maxy - miny)

    # vertical grid lines (x ticks)
    x_start = math.floor((minx) / xstep) * xstep
    x_end = math.ceil((maxx) / xstep) * xstep
    x = x_start
    while x <= x_end + 1e-12:
        sx = tx(x)
        svg.append(f'<line x1="{sx:.2f}" y1="0" x2="{sx:.2f}" y2="{H}" stroke="#e6e6e6" stroke-width="1" />')
        svg.append(f'<text x="{sx+3:.2f}" y="{H-4:.2f}" font-size="10" fill="#444">{x:.2f}</text>')
        x += xstep

    # horizontal grid lines (y ticks)
    y_start = math.floor((miny) / ystep) * ystep
    y_end = math.ceil((maxy) / ystep) * ystep
    y = y_start
    while y <= y_end + 1e-12:
        sy = ty(y)
        svg.append(f'<line x1="0" y1="{sy:.2f}" x2="{W}" y2="{sy:.2f}" stroke="#e6e6e6" stroke-width="1" />')
        svg.append(f'<text x="4" y="{sy-4:.2f}" font-size="10" fill="#444">{y:.2f}</text>')
        y += ystep

    # axes (x=0, y=0)
    if minx <= 0 <= maxx:
        svg.append(f'<line x1="{tx(0):.2f}" y1="0" x2="{tx(0):.2f}" y2="{H}" stroke="#888" stroke-width="2" />')
    if miny <= 0 <= maxy:
        svg.append(f'<line x1="0" y1="{ty(0):.2f}" x2="{W}" y2="{ty(0):.2f}" stroke="#888" stroke-width="2" />')

    # segments
    svg.append(f'<line x1="{tx(s1.a.x):.2f}" y1="{ty(s1.a.y):.2f}" x2="{tx(s1.b.x):.2f}" y2="{ty(s1.b.y):.2f}" stroke="blue" stroke-width="3" />')
    svg.append(f'<line x1="{tx(s2.a.x):.2f}" y1="{ty(s2.a.y):.2f}" x2="{tx(s2.b.x):.2f}" y2="{ty(s2.b.y):.2f}" stroke="green" stroke-width="3" />')
    # endpoints
    for p, color in [(s1.a, 'blue'), (s1.b, 'blue'), (s2.a, 'green'), (s2.b, 'green')]:
        svg.append(f'<circle cx="{tx(p.x):.2f}" cy="{ty(p.y):.2f}" r="4" fill="{color}" />')

    if res['intersect']:
        if res['type'] == 'point':
            x, y = res['point']
            svg.append(f'<circle cx="{tx(x):.2f}" cy="{ty(y):.2f}" r="6" fill="red" />')
        elif res['type'] == 'segment':
            (x1, y1), (x2, y2) = res['segment']
            svg.append(f'<line x1="{tx(x1):.2f}" y1="{ty(y1):.2f}" x2="{tx(x2):.2f}" y2="{ty(y2):.2f}" stroke="red" stroke-width="4" />')

    svg.append('</svg>')
    return '\n'.join(svg)


@app.route('/')
def index():
    # default eight zeros
    return render_template_string(INDEX_HTML, result=None, vals='0 0 0 0 0 0 0 0')


@app.route('/intersect', methods=['POST'])
def intersect():
    vals_raw = request.form.get('vals', '')
    parts = vals_raw.strip().split()
    try:
        nums = [float(x) for x in parts]
        if len(nums) != 8:
            raise ValueError('Oczekiwane 8 liczb')
    except Exception as e:
        return render_template_string(INDEX_HTML, result=True, result_text=f'Błąd: {e}', svg='', vals=vals_raw or '0 0 0 0 0 0 0 0')
    x1, y1, x2, y2, x3, y3, x4, y4 = nums
    s1 = Segment(Point(x1, y1), Point(x2, y2))
    s2 = Segment(Point(x3, y3), Point(x4, y4))
    res = intersect_segments(s1, s2)
    if not res['intersect']:
        result_text = 'NIE'
    elif res['type'] == 'point':
        x, y = res['point']
        result_text = f'TAK - punkt: ({x:.6f}, {y:.6f})'
    else:
        (xa, ya), (xb, yb) = res['segment']
        result_text = f'TAK - odcinek: ({xa:.6f}, {ya:.6f}) - ({xb:.6f}, {yb:.6f})'
    svg = _make_svg(s1, s2, res)
    return render_template_string(INDEX_HTML, result=True, result_text=result_text, svg=svg, vals=vals_raw)


if __name__ == '__main__':
    app.run(debug=True)
