from flask import Flask, request, render_template_string
from geometry import Point, Segment, intersect_segments

app = Flask(__name__)

FIELDS = ('x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4')

EXAMPLES = {
    'point': {
        'label': 'Punkt',
        'detail': 'przecięcie w środku',
        'values': {'x1': '0', 'y1': '0', 'x2': '2', 'y2': '2', 'x3': '0', 'y3': '2', 'x4': '2', 'y4': '0'},
    },
    'segment': {
        'label': 'Wspólny odcinek',
        'detail': 'odcinki współliniowe',
        'values': {'x1': '0', 'y1': '0', 'x2': '4', 'y2': '0', 'x3': '2', 'y3': '0', 'x4': '6', 'y4': '0'},
    },
    'none': {
        'label': 'Brak przecięcia',
        'detail': 'rozłączne odcinki',
        'values': {'x1': '0', 'y1': '0', 'x2': '1', 'y2': '0', 'x3': '2', 'y3': '0', 'x4': '3', 'y4': '0'},
    },
    'touch': {
        'label': 'Styk końcami',
        'detail': 'jeden punkt wspólny',
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
  <title>Przecięcie odcinków</title>
  <style>
    :root {
      --page: #eef3f8;
      --surface: #ffffff;
      --surface-soft: #f7fafc;
      --text: #142033;
      --muted: #65758b;
      --border: #d7e0ea;
      --border-strong: #aebdcb;
      --blue: #2f6fed;
      --blue-soft: #e9f0ff;
      --green: #159a74;
      --green-soft: #e7f7f1;
      --red: #d92d20;
      --red-soft: #fff0ed;
      --amber-soft: #fff7e6;
      --amber: #b45309;
      --ink: #172033;
      --shadow: 0 18px 45px rgba(20, 32, 51, 0.12);
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      background: var(--page);
      color: var(--text);
      font-family: Inter, "Segoe UI", Arial, sans-serif;
      font-size: 15px;
      line-height: 1.45;
      overflow-x: hidden;
    }

    button,
    input {
      font: inherit;
    }

    a {
      color: inherit;
    }

    .app {
      width: min(1180px, calc(100% - 28px));
      max-width: 100vw;
      margin: 0 auto;
      padding: 22px 0 32px;
    }

    .app-header {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 16px;
      align-items: center;
      margin-bottom: 16px;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      min-width: 0;
    }

    .brand-mark {
      position: relative;
      width: 42px;
      height: 42px;
      flex: 0 0 auto;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--surface);
      box-shadow: 0 10px 22px rgba(20, 32, 51, 0.08);
    }

    .brand-mark::before,
    .brand-mark::after {
      position: absolute;
      left: 8px;
      right: 8px;
      top: 20px;
      content: "";
      height: 3px;
      border-radius: 99px;
      transform-origin: center;
    }

    .brand-mark::before {
      background: var(--blue);
      transform: rotate(34deg);
    }

    .brand-mark::after {
      background: var(--green);
      transform: rotate(-34deg);
    }

    h1,
    h2,
    h3,
    p {
      margin: 0;
    }

    h1 {
      font-size: 28px;
      line-height: 1.1;
      letter-spacing: 0;
    }

    .header-subtitle {
      margin-top: 4px;
      color: var(--muted);
      font-size: 14px;
      font-weight: 600;
    }

    .header-actions {
      display: flex;
      gap: 8px;
      align-items: center;
    }

    .chip {
      min-height: 34px;
      display: inline-flex;
      align-items: center;
      gap: 7px;
      border: 1px solid var(--border);
      border-radius: 999px;
      background: var(--surface);
      padding: 7px 11px;
      color: #314158;
      font-size: 13px;
      font-weight: 800;
      white-space: nowrap;
    }

    .chip-dot {
      width: 8px;
      height: 8px;
      border-radius: 999px;
      background: var(--green);
    }

    .workspace {
      display: grid;
      grid-template-columns: 390px minmax(0, 1fr);
      gap: 16px;
      align-items: stretch;
      min-width: 0;
    }

    .panel {
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--surface);
      box-shadow: var(--shadow);
      overflow: hidden;
      min-width: 0;
    }

    .input-panel {
      align-self: start;
      min-width: 0;
    }

    .panel-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
      padding: 16px 18px;
      border-bottom: 1px solid var(--border);
      background: #fbfdff;
    }

    .panel-title {
      font-size: 16px;
      line-height: 1.2;
      font-weight: 900;
    }

    .panel-note {
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
    }

    .form {
      padding: 16px;
      min-width: 0;
    }

    .segment {
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow: hidden;
      min-width: 0;
    }

    .segment + .segment {
      margin-top: 12px;
    }

    .segment-title {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      padding: 12px 13px;
      border-bottom: 1px solid var(--border);
      background: var(--surface-soft);
      font-weight: 900;
    }

    .segment-title.blue {
      color: #1e4fc2;
    }

    .segment-title.green {
      color: #087354;
    }

    .segment-line {
      display: inline-flex;
      align-items: center;
      gap: 7px;
    }

    .line-sample {
      width: 28px;
      height: 4px;
      border-radius: 999px;
      display: inline-block;
    }

    .line-sample.blue {
      background: var(--blue);
    }

    .line-sample.green {
      background: var(--green);
    }

    .point-grid {
      padding: 12px;
      display: grid;
      gap: 10px;
      min-width: 0;
    }

    .point-row {
      display: grid;
      grid-template-columns: 42px minmax(0, 1fr) minmax(0, 1fr);
      gap: 9px;
      align-items: center;
      min-width: 0;
    }

    .point-badge {
      width: 36px;
      height: 36px;
      display: grid;
      place-items: center;
      border-radius: 999px;
      color: #ffffff;
      font-weight: 900;
      box-shadow: 0 8px 18px rgba(20, 32, 51, 0.14);
    }

    .point-badge.blue {
      background: var(--blue);
    }

    .point-badge.green {
      background: var(--green);
    }

    .coord {
      position: relative;
      min-width: 0;
    }

    .coord span {
      position: absolute;
      top: 50%;
      left: 10px;
      transform: translateY(-50%);
      color: var(--muted);
      font-size: 12px;
      font-weight: 900;
      pointer-events: none;
    }

    .coord input {
      width: 100%;
      min-width: 0;
      height: 40px;
      border: 1px solid var(--border-strong);
      border-radius: 7px;
      background: #ffffff;
      color: var(--text);
      padding: 8px 10px 8px 31px;
      font-weight: 800;
      outline: none;
    }

    .coord input:focus {
      border-color: var(--blue);
      box-shadow: 0 0 0 3px rgba(47, 111, 237, 0.16);
    }

    .actions {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 10px;
      margin-top: 14px;
    }

    .btn {
      min-height: 44px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      border: 1px solid var(--border-strong);
      border-radius: 7px;
      padding: 10px 14px;
      background: #ffffff;
      color: var(--text);
      font-weight: 900;
      text-decoration: none;
      cursor: pointer;
    }

    .btn-primary {
      border-color: var(--ink);
      background: var(--ink);
      color: #ffffff;
    }

    .btn:hover,
    .scenario:hover {
      transform: translateY(-1px);
    }

    .scenarios {
      padding: 0 16px 16px;
    }

    .scenario-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }

    .scenario {
      min-height: 64px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: #ffffff;
      padding: 10px 11px;
      text-decoration: none;
      transition: transform 0.15s ease, border-color 0.15s ease, background 0.15s ease;
    }

    .scenario.active {
      border-color: #8aa9ec;
      background: var(--blue-soft);
    }

    .scenario strong {
      display: block;
      color: var(--text);
      font-size: 13px;
      line-height: 1.2;
    }

    .scenario span {
      display: block;
      margin-top: 4px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
    }

    .result-panel {
      display: grid;
      grid-template-rows: auto minmax(0, 1fr);
      min-height: 650px;
      min-width: 0;
    }

    .result-head {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 14px;
      align-items: center;
      padding: 16px 18px;
      border-bottom: 1px solid var(--border);
      background: #fbfdff;
      min-width: 0;
    }

    .result-title {
      display: flex;
      align-items: center;
      gap: 10px;
      min-width: 0;
    }

    .status-dot {
      width: 13px;
      height: 13px;
      border-radius: 999px;
      flex: 0 0 auto;
      background: var(--border-strong);
    }

    .status-dot.yes {
      background: var(--green);
    }

    .status-dot.no {
      background: var(--amber);
    }

    .status-dot.error {
      background: var(--red);
    }

    .result-value {
      color: var(--text);
      font-size: 17px;
      font-weight: 900;
      overflow-wrap: anywhere;
    }

    .result-label {
      border-radius: 999px;
      padding: 8px 11px;
      font-size: 13px;
      font-weight: 900;
      white-space: nowrap;
    }

    .result-label.yes {
      background: var(--green-soft);
      color: #087354;
    }

    .result-label.no {
      background: var(--amber-soft);
      color: var(--amber);
    }

    .result-label.error {
      background: var(--red-soft);
      color: var(--red);
    }

    .plot-area {
      padding: 16px;
      min-height: 0;
      display: grid;
      grid-template-rows: minmax(0, 1fr) auto;
      gap: 12px;
    }

    .plot {
      min-height: 480px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: #fbfdff;
      overflow: hidden;
    }

    .plot svg {
      display: block;
      width: 100%;
      height: 100%;
      min-height: 480px;
    }

    .plot-empty {
      height: 100%;
      min-height: 480px;
      display: grid;
      place-items: center;
      padding: 24px;
      color: var(--muted);
      font-weight: 800;
      text-align: center;
    }

    .legend {
      display: flex;
      flex-wrap: wrap;
      gap: 9px;
    }

    .legend-item {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      border: 1px solid var(--border);
      border-radius: 999px;
      background: #ffffff;
      padding: 7px 10px;
      color: #41516a;
      font-size: 13px;
      font-weight: 800;
    }

    .legend-color {
      width: 10px;
      height: 10px;
      border-radius: 999px;
      display: inline-block;
    }

    @media (max-width: 920px) {
      .app {
        width: calc(100% - 32px);
        max-width: 100vw;
        padding-top: 14px;
        padding-left: 0;
        padding-right: 0;
      }

      .app-header,
      .workspace {
        grid-template-columns: 1fr;
        width: 100%;
        max-width: 100%;
        overflow: hidden;
      }

      .panel {
        width: 100%;
        max-width: 100%;
      }

      .workspace > * {
        min-width: 0;
      }

      .header-actions {
        justify-content: flex-start;
        flex-wrap: wrap;
      }

      .result-panel {
        min-height: auto;
      }
    }

    @media (max-width: 520px) {
      h1 {
        font-size: 23px;
      }

      .point-row {
        width: 100%;
        max-width: 100%;
        grid-template-columns: 38px minmax(0, 1fr);
      }

      .form,
      .point-grid,
      .segment {
        width: 100%;
        max-width: 100%;
      }

      .coord input {
        width: calc(100vw - 150px);
        max-width: 240px;
      }

      .point-badge {
        grid-row: span 2;
      }

      .segment-title > span:last-child {
        display: none;
      }

      .scenario-grid,
      .actions,
      .result-head {
        grid-template-columns: 1fr;
      }

      .panel-head .panel-note {
        display: none;
      }

      .actions,
      .scenario-grid {
        max-width: 300px;
      }

      .plot,
      .plot svg,
      .plot-empty {
        min-height: 360px;
        max-width: 100%;
      }
    }
  </style>
</head>
<body>
  <main class="app">
    <header class="app-header">
      <div class="brand">
        <div class="brand-mark" aria-hidden="true"></div>
        <div>
          <h1>Przecięcie odcinków</h1>
          <p class="header-subtitle">Odcinek AB oraz odcinek CD</p>
        </div>
      </div>
      <div class="header-actions">
        <span class="chip"><span class="chip-dot"></span>Python + Flask</span>
        <span class="chip">SVG</span>
      </div>
    </header>

    <div class="workspace">
      <section class="panel input-panel">
        <div class="panel-head">
          <h2 class="panel-title">Punkty odcinków</h2>
          <span class="panel-note">A B C D</span>
        </div>

        <form class="form" method="post" action="/intersect">
          <div class="segment">
            <div class="segment-title blue">
              <span class="segment-line"><span class="line-sample blue"></span>Odcinek AB</span>
              <span>A → B</span>
            </div>
            <div class="point-grid">
              <div class="point-row">
                <label class="point-badge blue" for="x1">A</label>
                <label class="coord"><span>x</span><input id="x1" name="x1" type="text" inputmode="decimal" value="{{ values.x1 }}" required></label>
                <label class="coord"><span>y</span><input id="y1" name="y1" type="text" inputmode="decimal" value="{{ values.y1 }}" required></label>
              </div>
              <div class="point-row">
                <label class="point-badge blue" for="x2">B</label>
                <label class="coord"><span>x</span><input id="x2" name="x2" type="text" inputmode="decimal" value="{{ values.x2 }}" required></label>
                <label class="coord"><span>y</span><input id="y2" name="y2" type="text" inputmode="decimal" value="{{ values.y2 }}" required></label>
              </div>
            </div>
          </div>

          <div class="segment">
            <div class="segment-title green">
              <span class="segment-line"><span class="line-sample green"></span>Odcinek CD</span>
              <span>C → D</span>
            </div>
            <div class="point-grid">
              <div class="point-row">
                <label class="point-badge green" for="x3">C</label>
                <label class="coord"><span>x</span><input id="x3" name="x3" type="text" inputmode="decimal" value="{{ values.x3 }}" required></label>
                <label class="coord"><span>y</span><input id="y3" name="y3" type="text" inputmode="decimal" value="{{ values.y3 }}" required></label>
              </div>
              <div class="point-row">
                <label class="point-badge green" for="x4">D</label>
                <label class="coord"><span>x</span><input id="x4" name="x4" type="text" inputmode="decimal" value="{{ values.x4 }}" required></label>
                <label class="coord"><span>y</span><input id="y4" name="y4" type="text" inputmode="decimal" value="{{ values.y4 }}" required></label>
              </div>
            </div>
          </div>

          <div class="actions">
            <button class="btn btn-primary" type="submit">Oblicz</button>
            <a class="btn" href="/?clear=1">Wyczyść</a>
          </div>
        </form>

        <div class="scenarios">
          <div class="scenario-grid">
            {% for key, example in examples.items() %}
              <a class="scenario {% if active_case == key %}active{% endif %}" href="/?case={{ key }}">
                <strong>{{ example.label }}</strong>
                <span>{{ example.detail }}</span>
              </a>
            {% endfor %}
          </div>
        </div>
      </section>

      <section class="panel result-panel">
        <div class="result-head">
          <div class="result-title">
            <span class="status-dot {{ result_type or '' }}"></span>
            <div>
              <p class="panel-note">Wynik</p>
              <h2 class="result-value">{{ result_text or 'Wpisz dane i oblicz przecięcie' }}</h2>
            </div>
          </div>
          {% if result_label %}
            <span class="result-label {{ result_type }}">{{ result_label }}</span>
          {% endif %}
        </div>

        <div class="plot-area">
          <div class="plot">
            {% if svg %}
              {{ svg|safe }}
            {% else %}
              <div class="plot-empty">Brak rysunku do wyświetlenia</div>
            {% endif %}
          </div>
          <div class="legend">
            <span class="legend-item"><span class="legend-color" style="background: var(--blue)"></span>AB</span>
            <span class="legend-item"><span class="legend-color" style="background: var(--green)"></span>CD</span>
            <span class="legend-item"><span class="legend-color" style="background: var(--red)"></span>część wspólna</span>
          </div>
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
        raise ValueError(f'pole {field_name} jest puste')
    return float(value)


def _parse_values(raw_values: dict) -> list:
    return [_read_number(raw_values[field], field) for field in FIELDS]


def _parse_form(form) -> tuple:
    raw_values = {field: form.get(field, '').strip() for field in FIELDS}

    if not any(raw_values.values()) and form.get('vals'):
        parts = form.get('vals', '').split()
        if len(parts) != 8:
            raise ValueError('oczekiwano 8 liczb')
        raw_values = dict(zip(FIELDS, parts))

    return raw_values, _parse_values(raw_values)


def _format_result(res) -> tuple:
    if not res['intersect']:
        return 'NIE', 'no', 'Brak przecięcia'
    if res['type'] == 'point':
        x, y = res['point']
        return f'TAK - punkt: ({x:.6f}, {y:.6f})', 'yes', 'Punkt'
    if res['type'] == 'segment':
        (x1, y1), (x2, y2) = res['segment']
        return f'TAK - odcinek: ({x1:.6f}, {y1:.6f}) - ({x2:.6f}, {y2:.6f})', 'yes', 'Odcinek'
    return 'NIE', 'no', 'Brak przecięcia'


def _solve(values: dict) -> tuple:
    x1, y1, x2, y2, x3, y3, x4, y4 = _parse_values(values)
    s1 = Segment(Point(x1, y1), Point(x2, y2))
    s2 = Segment(Point(x3, y3), Point(x4, y4))
    result = intersect_segments(s1, s2)
    result_text, result_type, result_label = _format_result(result)
    return result_text, result_type, result_label, _make_svg(s1, s2, result)


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
    pad = 0.18 * max(dx, dy)
    minx -= pad
    maxx += pad
    miny -= pad
    maxy += pad

    width = 760
    height = 560

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
        f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Rysunek odcinków AB i CD">',
        '<rect width="100%" height="100%" fill="#fbfdff"/>',
    ]

    x = math.floor(minx / xstep) * xstep
    while x <= math.ceil(maxx / xstep) * xstep + 1e-12:
        sx = tx(x)
        svg.append(f'<line x1="{sx:.2f}" y1="0" x2="{sx:.2f}" y2="{height}" stroke="#e5edf5" stroke-width="1"/>')
        svg.append(f'<text x="{sx + 7:.2f}" y="{height - 10:.2f}" font-size="12" font-weight="700" fill="#708098">{x:g}</text>')
        x += xstep

    y = math.floor(miny / ystep) * ystep
    while y <= math.ceil(maxy / ystep) * ystep + 1e-12:
        sy = ty(y)
        svg.append(f'<line x1="0" y1="{sy:.2f}" x2="{width}" y2="{sy:.2f}" stroke="#e5edf5" stroke-width="1"/>')
        svg.append(f'<text x="10" y="{sy - 7:.2f}" font-size="12" font-weight="700" fill="#708098">{y:g}</text>')
        y += ystep

    if minx <= 0 <= maxx:
        svg.append(f'<line x1="{tx(0):.2f}" y1="0" x2="{tx(0):.2f}" y2="{height}" stroke="#9fb0c1" stroke-width="2"/>')
    if miny <= 0 <= maxy:
        svg.append(f'<line x1="0" y1="{ty(0):.2f}" x2="{width}" y2="{ty(0):.2f}" stroke="#9fb0c1" stroke-width="2"/>')

    svg.append(f'<line x1="{tx(s1.a.x):.2f}" y1="{ty(s1.a.y):.2f}" x2="{tx(s1.b.x):.2f}" y2="{ty(s1.b.y):.2f}" stroke="#2f6fed" stroke-width="6" stroke-linecap="round"/>')
    svg.append(f'<line x1="{tx(s2.a.x):.2f}" y1="{ty(s2.a.y):.2f}" x2="{tx(s2.b.x):.2f}" y2="{ty(s2.b.y):.2f}" stroke="#159a74" stroke-width="6" stroke-linecap="round"/>')

    if res['intersect']:
        if res['type'] == 'point':
            x, y = res['point']
            svg.append(f'<circle cx="{tx(x):.2f}" cy="{ty(y):.2f}" r="10" fill="#d92d20" stroke="#ffffff" stroke-width="4"/>')
        elif res['type'] == 'segment':
            (x1, y1), (x2, y2) = res['segment']
            svg.append(f'<line x1="{tx(x1):.2f}" y1="{ty(y1):.2f}" x2="{tx(x2):.2f}" y2="{ty(y2):.2f}" stroke="#d92d20" stroke-width="10" stroke-linecap="round"/>')

    points = (
        ('A', s1.a, '#2f6fed'),
        ('B', s1.b, '#2f6fed'),
        ('C', s2.a, '#159a74'),
        ('D', s2.b, '#159a74'),
    )
    for label, point, color in points:
        px = tx(point.x)
        py = ty(point.y)
        svg.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="6" fill="{color}" stroke="#ffffff" stroke-width="3"/>')
        svg.append(f'<text x="{px + 12:.2f}" y="{py - 12:.2f}" font-size="16" font-weight="900" fill="#142033">{label}</text>')

    svg.append('</svg>')
    return '\n'.join(svg)


@app.route('/')
def index():
    if request.args.get('clear'):
        return _render(values=EMPTY_VALUES)

    case_name = request.args.get('case', 'point')
    values = _values_for_case(case_name)
    result_text, result_type, result_label, svg = _solve(values)
    return _render(
        values=values,
        result_text=result_text,
        result_type=result_type,
        result_label=result_label,
        svg=svg,
        active_case=case_name,
    )


@app.route('/intersect', methods=['POST'])
def intersect():
    try:
        values, nums = _parse_form(request.form)
        x1, y1, x2, y2, x3, y3, x4, y4 = nums
    except Exception as exc:
        values = {field: request.form.get(field, '').strip() for field in FIELDS}
        return _render(
            values=values,
            result_text=f'Błąd: {exc}',
            result_type='error',
            result_label='Błąd danych',
        )

    s1 = Segment(Point(x1, y1), Point(x2, y2))
    s2 = Segment(Point(x3, y3), Point(x4, y4))
    res = intersect_segments(s1, s2)
    result_text, result_type, result_label = _format_result(res)
    svg = _make_svg(s1, s2, res)
    return _render(values=values, result_text=result_text, result_type=result_type, result_label=result_label, svg=svg)


if __name__ == '__main__':
    app.run(debug=True)
