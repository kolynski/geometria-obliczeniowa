# Projekt: Zbiór punktów przecięcia dwóch odcinków

Program wyznacza przecięcie dwóch odcinków na płaszczyźnie.

Wynik:

- `NIE` - odcinki się nie przecinają,
- `TAK - punkt: (x, y)` - odcinki przecinają się w jednym punkcie,
- `TAK - odcinek: (x1, y1) - (x2, y2)` - odcinki mają wspólny fragment.

## Pliki

- `geometry.py` - obliczenia geometryczne,
- `main.py` - uruchomienie w konsoli,
- `app.py` - prosta strona we Flasku,
- `requirements.txt` - zależność potrzebna tylko do wersji webowej.

## Uruchomienie w konsoli

Wersja konsolowa nie wymaga instalowania bibliotek:

```powershell
python main.py 0 0 2 2 0 2 2 0
```

Przykłady:

```powershell
python main.py 0 0 2 2 0 2 2 0
# TAK - punkt: (1.000000, 1.000000)

python main.py 0 0 4 0 2 0 6 0
# TAK - odcinek: (2.000000, 0.000000) - (4.000000, 0.000000)

python main.py 0 0 1 0 2 0 3 0
# NIE
```

Można też uruchomić bez argumentów:

```powershell
python main.py
```

Program poprosi wtedy o osiem liczb:

```text
x1 y1 x2 y2 x3 y3 x4 y4
```

## Uruchomienie strony

Najpierw zainstaluj Flask:

```powershell
python -m pip install -r requirements.txt
```

Potem uruchom:

```powershell
python app.py
```

Adres w przeglądarce:

```text
http://127.0.0.1:5000/
```
