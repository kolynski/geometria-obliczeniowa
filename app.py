from flask import Flask, request, render_template_string
from geometry import Point, Segment, intersect_segments

app = Flask(__name__)

FIELDS = ('x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4')

EXAMPLES = {
    'point': {
        'label': 'Punkt',
        'values': {'x1': '0', 'y1': '0', 'x2': '2', 'y2': '2', 'x3': '0', 'y3': '2', 'x4': '2', 'y4': '0'},
    },
    'segment': {
        'label': 'Odcinek',
        'values': {'x1': '0', 'y1': '0', 'x2': '4', 'y2': '0', 'x3': '2', 'y3': '0', 'x4': '6', 'y4': '0'},
    },
    'none': {
        'label': 'Brak',
        'values': {'x1': '0', 'y1': '0', 'x2': '1', 'y2': '0', 'x3': '2', 'y3': '0', 'x4': '3', 'y4': '0'},
    },
    'touch': {
        'label': 'Styk',
        'values': {'x1': '0', 'y1': '0', 'x2': '1', 'y2': '0', 'x3': '1', 'y3': '0', 'x4': '2', 'y4': '0'},
    },
}

EMPTY_VALUES = {field: '' for field in FIELDS}

INDEX_HTML = """
<!doctype html>
<html lang="pl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>PrzeciÄ™cie odcinkĂłw</title>
  <style>
    :root {
      --bg: #f5f7fb;
      --panel: #ffffff;
      --text: #172033;
      --muted: #667085;
      --line: #d9e2ef;
      --line-strong: #b9c7da;
      --blue: #2563eb;
      --green: #059669;
      --red: #dc2626;
      --ink: #111827;
      --shadow: 0 16px 40px rgba(23, 32, 51, 0.10);
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      background: var(--bg);
      color: var(--text);
      font-family: Arial, Helvetica, sans-serif;
      font-size: 16px;
      line-height: 1.5;
    }

    .page {
      width: min(1120px, calc(100% - 32px));
      margin: 0 auto;
      padding: 32px 0 42px;
    }

    .topbar {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 18px;
      margin-bottom: 20px;
    }

    h1,
    h2,
    p {
      margin: 0;
    }

    h1 {
      font-size: 32px;
      line-height: 1.15;
      font-weight: 800;
    }

    .subtitle {
      margin-top: 6px;
      color: var(--muted);
    }

    .badge {
      flex: 0 0 auto;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: #ffffff;
      color: #344054;
      padding: 8px 12px;
      font-size: 13px;
      font-weight: 700;
    }

    .layout {
      display: grid;
      grid-template-columns: minmax(320px, 420px) minmax(0, 1fr);
      gap: 20px;
      align-items: start;
    }

    .panel {
      overflow: hidden;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      box-shadow: var(--shadow);
    }

    .panel-header,
    .result-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      border-bottom: 1px solid var(--line);
      padding: 16px 18px;
    }

    .panel-header h2,
    .result-header h2 {
      font-size: 18px;
      line-height: 1.2;
    }

    .small-note {
      color: var(--muted);
      font-size: 13px;
      font-weight: 700;
    }

    .form {
      padding: 18px;
    }

    .segment-fieldset {
      margin: 0 0 14px;
      padding: 14px;
      border: 1px solid var(--line);
      border-left-width: 5px;
      border-radius: 8px;
    }

    .segment-fieldset.blue {
      border-left-color: var(--blue);
    }

    .segment-fieldset.green {
      border-left-color: var(--green);
    }

    .segment-fieldset legend {
      padding: 0 8px;
      font-weight: 800;
      color: #243047;
    }

    .point-row {
      display: grid;
      grid-template-columns: 34px minmax(0, 1fr) minmax(0, 1fr);
      gap: 10px;
      align-items: end;
      margin-top: 12px;
    }

    .point-name {
      display: grid;
      place-items: center;
      width: 30px;
      height: 30px;
      align-self: center;
      border-radius: 999px;
      background: #eef2f7;
      color: #243047;
      font-weight: 800;
    }

    .field label {
      display: block;
      margin-bottom: 5px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
    }

    .field input {
      width: 100%;
      min-height: 42px;
      border: 1px solid var(--line-strong);
      border-radius: 6px;
      padding: 9px 10px;
      color: var(--text);
      font: inherit;
      background: #ffffff;
    }

    .field input:focus {
      border-color: #475467;
      outline: 3px solid rgba(37, 99, 235, 0.16);
    }

    .actions,
    .example-list {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }

    .actions {
      margin-top: 18px;
    }

    button,
    .button-link,
    .example-link {
      min-height: 42px;
      border: 1px solid var(--line-strong);
      border-radius: 6px;
      padding: 9px 14px;
      font: inherit;
      font-weight: 800;
      text-decoration: none;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
    }

    .primary {
      border-color: var(--ink);
      background: var(--ink);
      color: #ffffff;
    }

    .button-link,
    .example-link {
      background: #ffffff;
      color: var(--text);
    }

    .example-link.active,
    .example-link:hover,
    .button-link:hover {
      border-color: #98a2b3;
      background: #f8fafc;
    }

    .examples {
      border-top: 1px solid var(--line);
      padding: 16px 18px 18px;
    }

    .examples-title {
      margin-bottom: 10px;
      color: #344054;
      font-size: 13px;
      font-weight: 800;
      text-transform: uppercase;
    }

    .result-pill {
      flex: 0 0 auto;
      border-radius: 999px;
      padding: 6px 10px;
      font-size: 13px;
      font-weight: 800;
    }

    .result-pill.yes {
      background: #ecfdf3;
      color: #047857;
    }

    .result-pill.no {
      background: #fff7ed;
      color: #c2410c;
    }

    .result-pill.error {
      background: #fef2f2;
      color: #b91c1c;
    }

    .result-text {
      color: #243047;
      font-weight: 800;
    }

    .canvas {
      padding: 18px;
    }

    .plot-wrap,
    .empty-state {
      width: 100%;
      min-height: 420px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fbfdff;
    }

    .plot-wrap {
      overflow: hidden;
      aspect-ratio: 1 / 1;
    }

    .plot-wrap svg {
      display: block;
      width: 100%;
      height: 100%;
    }

    .empty-state {
      display: grid;
      place-items: center;
      padding: 24px;
      color: var(--muted);
      text-align: center;
      font-weight: 700;
    }

    .legend {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 12px;
      color: var(--muted);
      font-size: 13px;
      font-weight: 700;
    }

    .legend-item {
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }

    .legend-color {
      width: 12px;
      height: 12px;
      border-radius: 999px;
      display: inline-block;
    }

    @media (max-width: 840px) {
      .page {
        width: min(100% - 20px, 640px);
        padding-top: 18px;
      }

      .topbar,
      .layout {
        display: block;
      }

      .badge {
        display: inline-flex;
        margin-top: 12px;
      }

      .panel + .panel {
        margin-top: 16px;
      }

      h1 {
        font-size: 26px;
      }
    }
  </style>
</head>
<body>
  <main class="page">
    <header class="topbar">
      <div>
        <h1>PrzeciÄ™cie odcinkĂłw</h1>
        <p class="subtitle">WprowadĹş punkty A, B, C i D, a program wyznaczy czÄ™Ĺ›Ä‡ wspĂłlnÄ… odcinkĂłw AB oraz CD.</p>
      </div>
      <div class="badge">Geometria obliczeniowa</div>
    </header>

    <div class="layout">
      <section class="panel">
        <div class="panel-header">
          <h2>Dane wejĹ›ciowe</h2>
          <span class="small-note">4 punkty</span>
        </div>

        <form class="form" method="post" action="/intersect">
          <fieldset class="segment-fieldset blue">
            <legend>Odcinek AB</legend>
            <div class="point-row">
              <div class="point-name">A</div>
              <div class="field">
                <label for="x1">x</label>
                <input id="x1" name="x1" type="text" inputmode="decimal" value="{{ values.x1 }}" required>
              </div>
              <div class="field">
                <label for="y1">y</label>
                <input id="y1" name="y1" type="text" inputmode="decimal" value="{{ values.y1 }}" required>
              </div>
            </div>
            <div class="point-row">
              <div class="point-name">B</div>
              <div class="field">
                <label for="x2">x</label>
                <input id="x2" name="x2" type="text" inputmode="decimal" value="{{ values.x2 }}" required>
              </div>
              <div class="field">
                <label for="y2">y</label>
                <input id="y2" name="y2" type="text" inputmode="decimal" value="{{ values.y2 }}" required>
              </div>
            </div>
          </fieldset>

          <fieldset class="segment-fieldset green">
            <legend>Odcinek CD</legend>
            <div class="point-row">
              <div class="point-name">C</div>
              <div class="field">
                <label for="x3">x</label>
                <input id="x3" name="x3" type="text" inputmode="decimal" value="{{ values.x3 }}" required>
              </div>
              <div class="field">
                <label for="y3">y</label>
                <input id="y3" name="y3" type="text" inputmode="decimal" value="{{ values.y3 }}" required>
              </div>
            </div>
            <div class="point-row">
              <div class="point-name">D</div>
              <div class="field">
                <label for="x4">x</label>
                <input id="x4" name="x4" type="text" inputmode="decimal" value="{{ values.x4 }}" required>
              </div>
              <div class="field">
                <label for="y4">y</label>
                <input id="y4" name="y4" type="text" inputmode="decimal" value="{{ values.y4 }}" required>
              </div>
            </div>
          </fieldset>

          <div class="actions">
            <button class="primary" type="submit">Oblicz</button>
            <a class="button-link" href="/?case=point">Reset</a>
          </div>
        </form>

        <div class="examples">
          <div class="examples-title">Szybkie przykĹ‚ady</div>
          <div class="example-list">
            {% for key, example in examples.items() %}
              <a class="example-link {% if active_case == key %}active{% endif %}" href="/?case={{ key }}">{{ example.label }}</a>
            {% endfor %}
          </div>
        </div>
      </section>

      <section class="panel">
        <div class="result-header">
          <div>
            <h2>Wynik</h2>
            <p class="result-text">{{ result_text or 'Gotowe do obliczenia' }}</p>
          </div>
          {% if result_type %}
            <span class="result-pill {{ result_type }}">{{ result_label }}</span>
          {% endif %}
        </div>

        <div class="canvas">
          {% if svg %}
            <div class="plot-wrap">
              {{ svg|safe }}
            </div>
            <div class="legend">
              <span class="legend-item"><span class="legend-color" style="background: var(--blue)"></span>AB</span>
              <span class="legend-item"><span class="legend-color" style="background: var(--green)"></span>CD</span>
              <span class="legend-item"><span class="legend-color" style="background: var(--red)"></span>PrzeciÄ™cie</span>
            </div>
          {% else %}
            <div class="empty-state">Wpisz wspĂłĹ‚rzÄ™dne punktĂłw i kliknij Oblicz.</div>
          {% endif %}
        </div>
      </section>
    </div>
  </main>
</body>
</html>
"""


def _values_for_case(case_name: str) -> dict:
    example = EXAMPLES.get(case_name, EXAMPLES['point'])
    return dict(example['values'])


def _read_number(raw_value: str, field_name: str) -> float:
    value = raw_value.strip().replace(',', '.')
    if not value:
        raise ValueError(f'Pole {field_name} jest puste')
    return float(value)


def _parse_form(form) -> tuple:
    raw_values = {field: form.get(field, '').strip() for field in FIELDS}

    if not any(raw_values.values()) and form.get('vals'):
        parts = form.get('vals', '').split()
        if len(parts) != 8:
            raise ValueError('Oczekiwane 8 liczb')
        raw_values = dict(zip(FIELDS, parts))

    numbers = [_read_number(raw_values[field], field) for field in FIELDS]
    return raw_values, numbers


def _format_result(res) -> tuple:
    if not res['intersect']:
        return 'NIE', 'no', 'Brak'
    if res['type'] == 'point':
        x, y = res['point']
        return f'TAK - punkt: ({x:.6f}, {y:.6f})', 'yes', 'Punkt'
    if res['type'] == 'segment':
        (x1, y1), (x2, y2) = res['segment']
        return f'TAK - odcinek: ({x1:.6f}, {y1:.6f}) - ({x2:.6f}, {y2:.6f})', 'yes', 'Odcinek'
    return 'NIE', 'no', 'Brak'


def _render(values=None, result_text=None, result_type=None, result_label=None, svg=None, active_case=None):
    return render_template_string(
        INDEX_HTML,
        values=values or EMPTY_VALUES,
        result_text=result_text,
        result_type=result_type,
        result_label=result_label,
        svg=svg,
        examples=EXAMPLES,
        active_case=active_case,
    )


def _make_svg(s1: Segment, s2: Segment, res) -> str:
    xs = [s1.a.x, s1.b.x, s2.a.x, s2.b.x]
    ys = [s1.a.y, s1.b.y, s2.a.y, s2.b.y]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)

    dx = maxx - minx or 1.0
    dy = maxy - miny or 1.0
    pad = 0.14 * max(dx, dy)
    minx -= pad
    maxx += pad
    miny -= pad
    maxy += pad

    width = 520
    height = 520

    def tx(x):
        return (x - minx) / (maxx - minx) * width

    def ty(y):
        return height - (y - miny) / (maxy - miny) * height

    import math

    def nice_step(span, target=8):
        raw = span / target if span > 0 else 1.0
        exp = math.floor(math.log10(raw))
        base = 10 ** exp
        for multiplier in (1, 2, 5, 10):
            step = multiplier * base
            if step >= raw:
                return step
        return 10 * base

    xstep = nice_step(maxx - minx)
    ystep = nice_step(maxy - miny)

    svg = [
        f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Rysunek odcinkĂłw AB i CD">',
        '<rect width="100%" height="100%" fill="#fbfdff"/>',
    ]

    x = math.floor(minx / xstep) * xstep
    while x <= math.ceil(maxx / xstep) * xstep + 1e-12:
        sx = tx(x)
        svg.append(f'<line x1="{sx:.2f}" y1="0" x2="{sx:.2f}" y2="{height}" stroke="#e6edf5" stroke-width="1"/>')
        svg.append(f'<text x="{sx + 4:.2f}" y="{height - 8:.2f}" font-size="11" fill="#667085">{x:g}</text>')
        x += xstep

    y = math.floor(miny / ystep) * ystep
    while y <= math.ceil(maxy / ystep) * ystep + 1e-12:
        sy = ty(y)
        svg.append(f'<line x1="0" y1="{sy:.2f}" x2="{width}" y2="{sy:.2f}" stroke="#e6edf5" stroke-width="1"/>')
        svg.append(f'<text x="8" y="{sy - 5:.2f}" font-size="11" fill="#667085">{y:g}</text>')
        y += ystep

    if minx <= 0 <= maxx:
        svg.append(f'<line x1="{tx(0):.2f}" y1="0" x2="{tx(0):.2f}" y2="{height}" stroke="#98a2b3" stroke-width="2"/>')
    if miny <= 0 <= maxy:
        svg.append(f'<line x1="0" y1="{ty(0):.2f}" x2="{width}" y2="{ty(0):.2f}" stroke="#98a2b3" stroke-width="2"/>')

    svg.append(f'<line x1="{tx(s1.a.x):.2f}" y1="{ty(s1.a.y):.2f}" x2="{tx(s1.b.x):.2f}" y2="{ty(s1.b.y):.2f}" stroke="#2563eb" stroke-width="5" stroke-linecap="round"/>')
    svg.append(f'<line x1="{tx(s2.a.x):.2f}" y1="{ty(s2.a.y):.2f}" x2="{tx(s2.b.x):.2f}" y2="{ty(s2.b.y):.2f}" stroke="#059669" stroke-width="5" stroke-linecap="round"/>')

    if res['intersect']:
        if res['type'] == 'point':
            x, y = res['point']
            svg.append(f'<circle cx="{tx(x):.2f}" cy="{ty(y):.2f}" r="8" fill="#dc2626" stroke="#ffffff" stroke-width="3"/>')
        elif res['type'] == 'segment':
            (x1, y1), (x2, y2) = res['segment']
            svg.append(f'<line x1="{tx(x1):.2f}" y1="{ty(y1):.2f}" x2="{tx(x2):.2f}" y2="{ty(y2):.2f}" stroke="#dc2626" stroke-width="8" stroke-linecap="round"/>')

    points = [
        ('A', s1.a, '#2563eb'),
        ('B', s1.b, '#2563eb'),
        ('C', s2.a, '#059669'),
        ('D', s2.b, '#059669'),
    ]
    for label, point, color in points:
        px = tx(point.x)
        py = ty(point.y)
        svg.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="5" fill="{color}" stroke="#ffffff" stroke-width="2"/>')
        svg.append(f'<text x="{px + 10:.2f}" y="{py - 10:.2f}" font-size="15" font-weight="700" fill="#243047">{label}</text>')

    svg.append('</svg>')
    return '\n'.join(svg)


@app.route('/')
def index():
    case_name = request.args.get('case', 'point')
    return _render(values=_values_for_case(case_name), active_case=case_name)


@app.route('/intersect', methods=['POST'])
def intersect():
    try:
        values, nums = _parse_form(request.form)
        x1, y1, x2, y2, x3, y3, x4, y4 = nums
    except Exception as exc:
        values = {field: request.form.get(field, '').strip() for field in FIELDS}
        return _render(
            values=values,
            result_text=f'BĹ‚Ä…d: {exc}',
            result_type='error',
            result_label='BĹ‚Ä…d',
        )

    s1 = Segment(Point(x1, y1), Point(x2, y2))
    s2 = Segment(Point(x3, y3), Point(x4, y4))
    res = intersect_segments(s1, s2)
    result_text, result_type, result_label = _format_result(res)
    svg = _make_svg(s1, s2, res)
    return _render(values=values, result_text=result_text, result_type=result_type, result_label=result_label, svg=svg)


if __name__ == '__main__':
    app.run(debug=True)
