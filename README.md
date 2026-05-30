# Zbiór punktów przecięcia dwóch odcinków

Projekt z geometrii obliczeniowej. Program wyznacza przecięcie dwóch odcinków
na płaszczyźnie i zwraca pełną informację o części wspólnej.

## Spis treści

- [Opis zadania](#opis-zadania)
- [Co potrafi program](#co-potrafi-program)
- [Struktura projektu](#struktura-projektu)
- [Uruchomienie w konsoli](#uruchomienie-w-konsoli)
- [Uruchomienie aplikacji webowej](#uruchomienie-aplikacji-webowej)
- [Format danych](#format-danych)
- [Przykłady wyników](#przykłady-wyników)
- [Opis algorytmu](#opis-algorytmu)
- [Opis plików](#opis-plików)
- [Szybka instrukcja na prezentację](#szybka-instrukcja-na-prezentację)

## Opis zadania

Dane są dwa odcinki:

- odcinek `AB`, gdzie `A = (x1, y1)` oraz `B = (x2, y2)`,
- odcinek `CD`, gdzie `C = (x3, y3)` oraz `D = (x4, y4)`.

Celem programu jest sprawdzenie, czy odcinki się przecinają. Jeżeli tak,
program określa, czy częścią wspólną jest pojedynczy punkt, czy odcinek.

## Co potrafi program

Program obsługuje:

- przecięcie w jednym punkcie,
- brak przecięcia,
- odcinki współliniowe z częścią wspólną,
- styk końcami,
- przypadek, w którym koniec jednego odcinka leży na drugim odcinku,
- odcinki pionowe,
- odcinki poziome,
- liczby całkowite i zmiennoprzecinkowe.

Wynik jest wypisywany w jednej z trzech postaci:

```text
NIE
```

```text
TAK - punkt: (x, y)
```

```text
TAK - odcinek: (x1, y1) - (x2, y2)
```

## Struktura projektu

```text
.
|-- app.py            # aplikacja webowa Flask
|-- geometry.py       # algorytm i funkcje geometryczne
|-- main.py           # wersja konsolowa programu
|-- README.md         # dokumentacja projektu
`-- requirements.txt  # zależności dla wersji webowej
```

Projekt jest celowo prosty. Nie ma katalogu `.venv`, cache, frameworka testowego
ani dodatkowej konfiguracji.

## Uruchomienie w konsoli

Wersja konsolowa nie wymaga instalowania bibliotek.

### Sposób 1: dane jako argumenty

```powershell
python main.py 0 0 2 2 0 2 2 0
```

Wynik:

```text
TAK - punkt: (1.000000, 1.000000)
```

Kolejność argumentów:

```text
x1 y1 x2 y2 x3 y3 x4 y4
```

### Sposób 2: wpisywanie punktów po kolei

```powershell
python main.py
```

Program zapyta o punkty:

```text
Podaj współrzędne punktów końcowych odcinków.
A.x (x1):
A.y (y1):
B.x (x2):
B.y (y2):
C.x (x3):
C.y (y3):
D.x (x4):
D.y (y4):
```

To jest wygodniejsze podczas prezentacji, bo nie trzeba pamiętać kolejności
ośmiu liczb.

## Uruchomienie aplikacji webowej

Wersja webowa daje prosty formularz i rysunek odcinków.

Najpierw zainstaluj Flask:

```powershell
python -m pip install -r requirements.txt
```

Potem uruchom aplikację:

```powershell
python app.py
```

Otwórz w przeglądarce:

```text
http://127.0.0.1:5000/
```

Na stronie wpisuje się punkty osobno:

```text
Odcinek AB:
A = (x1, y1)
B = (x2, y2)

Odcinek CD:
C = (x3, y3)
D = (x4, y4)
```

Interfejs ma też szybkie przykłady:

- `Punkt` - odcinki przecinają się w jednym punkcie,
- `Odcinek` - odcinki mają wspólny fragment,
- `Brak` - odcinki się nie przecinają,
- `Styk` - odcinki dotykają się końcami.

Po kliknięciu `Oblicz` aplikacja pokazuje:

- wynik tekstowy,
- rysunek obu odcinków,
- punkt przecięcia albo wspólny fragment zaznaczony na czerwono.

Zatrzymanie serwera:

```text
Ctrl + C
```

## Format danych

Program przyjmuje osiem liczb:

```text
x1 y1 x2 y2 x3 y3 x4 y4
```

Ich znaczenie:

| Wartość | Punkt | Opis |
| --- | --- | --- |
| `x1`, `y1` | `A` | początek pierwszego odcinka |
| `x2`, `y2` | `B` | koniec pierwszego odcinka |
| `x3`, `y3` | `C` | początek drugiego odcinka |
| `x4`, `y4` | `D` | koniec drugiego odcinka |

Przykład:

```text
0 0 2 2 0 2 2 0
```

Oznacza:

```text
A = (0, 0)
B = (2, 2)
C = (0, 2)
D = (2, 0)
```

## Przykłady wyników

### 1. Przecięcie w jednym punkcie

```powershell
python main.py 0 0 2 2 0 2 2 0
```

```text
TAK - punkt: (1.000000, 1.000000)
```

### 2. Brak przecięcia

```powershell
python main.py 0 0 1 0 2 0 3 0
```

```text
NIE
```

### 3. Wspólny fragment odcinków

```powershell
python main.py 0 0 4 0 2 0 6 0
```

```text
TAK - odcinek: (2.000000, 0.000000) - (4.000000, 0.000000)
```

### 4. Styk końcami

```powershell
python main.py 0 0 1 0 1 0 2 0
```

```text
TAK - punkt: (1.000000, 0.000000)
```

### 5. Koniec jednego odcinka leży na drugim

```powershell
python main.py 0 0 4 0 2 0 2 1
```

```text
TAK - punkt: (2.000000, 0.000000)
```

### 6. Odcinki pionowe ze wspólnym fragmentem

```powershell
python main.py 0 0 0 4 0 2 0 6
```

```text
TAK - odcinek: (0.000000, 2.000000) - (0.000000, 4.000000)
```

## Opis algorytmu

Najważniejsza funkcja znajduje się w pliku `geometry.py`:

```python
intersect_segments(s1, s2)
```

Program wykorzystuje orientację trzech punktów. Orientacja jest obliczana za
pomocą iloczynu wektorowego:

```text
(B - A) x (C - A)
```

Znak wyniku mówi, czy punkt leży po lewej stronie prostej, po prawej stronie,
czy na tej samej prostej.

Ogólna idea:

1. Obliczane są orientacje punktów względem obu odcinków.
2. Jeżeli końce jednego odcinka leżą po przeciwnych stronach drugiego odcinka
   i odwrotnie, przecięcie jest punktem.
3. Jeżeli wszystkie istotne orientacje są równe zero, odcinki są współliniowe.
4. Dla odcinków współliniowych program sprawdza nakładanie rzutów na oś `X`
   albo `Y`.
5. Jeżeli nakładanie ma długość dodatnią, wynikiem jest odcinek.
6. Jeżeli nakładanie ma długość zerową, wynikiem jest punkt.
7. Jeżeli żaden z tych warunków nie zachodzi, wynikiem jest `NIE`.

Do porównywania liczb zmiennoprzecinkowych używana jest tolerancja:

```python
EPS = 1e-9
```

Dzięki temu program jest odporniejszy na drobne błędy dokładności obliczeń.

## Opis plików

### `geometry.py`

Zawiera część obliczeniową:

- klasę `Point`,
- klasę `Segment`,
- funkcję orientacji punktów,
- sprawdzanie, czy punkt leży na odcinku,
- obliczanie punktu przecięcia prostych,
- rozpoznawanie przecięcia typu punkt albo odcinek.

### `main.py`

Zawiera wersję konsolową:

- przyjmuje osiem argumentów z terminala,
- albo pyta po kolei o punkty `A`, `B`, `C`, `D`,
- tworzy dwa odcinki,
- wywołuje algorytm,
- wypisuje wynik.

### `app.py`

Zawiera wersję webową:

- formularz z osobnymi polami dla punktów `A`, `B`, `C`, `D`,
- szybkie przykłady,
- wynik tekstowy,
- rysunek SVG z siatką, osiami i zaznaczonym przecięciem.

### `requirements.txt`

Zawiera zależność potrzebną do strony:

```text
Flask>=2.0
```

## Szybka instrukcja na prezentację

1. Pokaż wersję konsolową:

```powershell
python main.py 0 0 2 2 0 2 2 0
```

2. Pokaż przecięcie w punkcie:

```text
TAK - punkt: (1.000000, 1.000000)
```

3. Pokaż wspólny odcinek:

```powershell
python main.py 0 0 4 0 2 0 6 0
```

4. Pokaż brak przecięcia:

```powershell
python main.py 0 0 1 0 2 0 3 0
```

5. Uruchom stronę:

```powershell
python app.py
```

6. W przeglądarce otwórz:

```text
http://127.0.0.1:5000/
```

7. Użyj przycisków `Punkt`, `Odcinek`, `Brak` i `Styk`, żeby szybko pokazać
   najważniejsze przypadki.

## Autorzy

Projekt zaliczeniowy z geometrii obliczeniowej.
