# Projekt: Zbiór punktów przecięcia dwóch odcinków

Krótka instrukcja uruchomienia projektu lokalnie (Windows / PowerShell).

Pliki istotne:
- [projekt/app.py](projekt/app.py) — prosty interfejs webowy (Flask) z SVG
- [projekt/main.py](projekt/main.py) — CLI (8 argumentów lub interaktywnie)
- [projekt/geometry.py](projekt/geometry.py) — implementacja algorytmu
- [projekt/tests](projekt/tests) — testy jednostkowe (pytest)
- [projekt/requirements.txt](projekt/requirements.txt) — wymagania dla katalogu `projekt`

Zainstaluj zależności (zalecane w virtualenv):

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Uruchom aplikację Flask (z katalogu głównego projektu):

```powershell
python projekt\app.py
# lub
$env:FLASK_APP='projekt/app.py'
flask run
```

Otwórz w przeglądarce: http://127.0.0.1:5000/

Uruchom CLI (przykład):

```powershell
python projekt\main.py 0 0 2 2 0 2 2 0
```

Uwagi:
- Domyślne pole formularza w UI (po restarcie serwera) to `0 0 0 0 0 0 0 0`. Po wpisaniu wartości pozostają one w polu dopóki nie klikniesz `Reset`.
- Jeśli chcesz wygenerować bardziej rozbudowaną dokumentację lub plik `requirements.txt` z dokładnymi wersjami, daj znać.
