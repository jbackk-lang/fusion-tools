# fusion-tools

Narzędzia do analizy danych z fuzji jądrowej (W7-X, JET, DIII-D, EAST) 
oparte na modelach GIA, TIMDR, Λ–τ–ρ oraz Modelu J.

Projekt łączy klasyczne podejście do diagnostyki plazmy z 
redukcją informacji, analizą strukturalną i detekcją punktów skrętu sygnału.

---

## 🔥 Cele projektu

- uproszczenie analizy sygnałów z diagnostyk plazmy,
- wykrywanie anomalii i defektów w czasie rzeczywistym,
- redukcja szumu i nadmiarowości danych,
- ekstrakcja cech strukturalnych (Λ–τ–ρ),
- detekcja punktów skrętu (Model J),
- przygotowanie narzędzi kompatybilnych z open‑data W7‑X i innymi tokamakami/stellaratorami.

---

## 📁 Struktura

fusion-tools/
│
├── data/                     # przykładowe sygnały i metadane
│
├── parsers/                 # wczytywanie danych (HDF5, MDSplus, CSV)
│
├── timdr/                   # filtr redukcji informacji TIMDR
│
├── latro/                   # analiza strukturalna Λ–τ–ρ
│
├── model_j/                 # detekcja punktów skrętu sygnału
│
└── demo/                    # notebook z przykładową analizą

---

## 🧩 Moduły

### **parsers/**
Obsługa formatów używanych w diagnostyce plazmy:
- **HDF5** – dane z W7‑X, JET, DIII‑D  
- **MDSplus** – standard w tokamakach  
- **CSV** – szybkie testy i prototypy  

### **timdr/**
TIMDR (Topological Information Minimal Defect Reduction):
- redukcja szumu,
- kompresja informacji,
- detekcja defektów,
- segmentacja sygnału.

### **latro/**
Λ–τ–ρ:
- analiza struktury sygnału,
- gradienty, skręty, rezonanse,
- ekstrakcja cech do modeli ML/AI.

### **model_j/**
Model J:
- detekcja punktów skrętu,
- wykrywanie gwałtownych zmian dynamiki,
- idealne do turbulencji i przejść fazowych.

### **demo/**
Przykładowy pipeline:
- wczytanie sygnału,
- TIMDR → redukcja,
- Λ–τ–ρ → analiza,
- Model J → punkty skrętu,
- wizualizacje.

---
## 🔬 Offline Demo — TIMDR + Λ–τ–ρ + Model J

Ten demo pokazuje działanie pipeline’u na lokalnym sygnale Mirnova (`w7x_mirnov_example.csv`).

### Etapy analizy

1. **TIMDR (Filter)** – redukcja szumu poprzez różnicę kolejnych próbek.  
2. **Λ–τ–ρ (Metryki)** – obliczenie trzech parametrów charakteryzujących sygnał:  
    - Λ – amplituda zakresu,  
    - τ – średnia wartość bezwzględna,  
    - ρ – energia sygnału.  
3. **Model J (Detekcja)** – wykrywanie lokalnych maksimów w sygnale magnetycznym.

### Uruchomienie demo

```python
import csv
import matplotlib.pyplot as plt
from demo_pipeline import timdr_filter, latro, model_j_points

time, signal = [], []
with open("w7x_mirnov_example.csv") as f:
    reader = csv.reader(f)
    next(reader)
    for t, s in reader:
        time.append(float(t))
        signal.append(float(s))

reduced = timdr_filter(signal)
lam, tau, rho = latro(signal)
points = model_j_points(signal)

print("Λ–τ–ρ:", lam, tau, rho)

plt.figure(figsize=(12,5))
plt.plot(time, signal, label="sygnał")
plt.scatter([time[i] for i in points], [signal[i] for i in points],
            color="red", s=10, label="Model J")
plt.legend()
plt.show()

## 🔬 Offline Demo — TIMDR + Λ–τ–ρ + Model J

Ten demo pokazuje działanie pipeline’u na lokalnym sygnale Mirnova (`w7x_mirnov_example.csv`).

### Etapy analizy

1. **TIMDR (Filter)** – redukcja szumu poprzez różnicę kolejnych próbek.  
2. **Λ–τ–ρ (Metryki)** – obliczenie trzech parametrów charakteryzujących sygnał:  
    - Λ – amplituda zakresu,  
    - τ – średnia wartość bezwzględna,  
    - ρ – energia sygnału.  
3. **Model J (Detekcja)** – wykrywanie lokalnych maksimów w sygnale magnetycznym.

### Uruchomienie demo

```python
import csv
import matplotlib.pyplot as plt
from demo_pipeline import timdr_filter, latro, model_j_points

time, signal = [], []
with open("w7x_mirnov_example.csv") as f:
    reader = csv.reader(f)
    next(reader)
    for t, s in reader:
        time.append(float(t))
        signal.append(float(s))

reduced = timdr_filter(signal)
lam, tau, rho = latro(signal)
points = model_j_points(signal)

print("Λ–τ–ρ:", lam, tau, rho)

plt.figure(figsize=(12,5))
plt.plot(time, signal, label="sygnał")
plt.scatter([time[i] for i in points], [signal[i] for i in points],
            color="red", s=10, label="Model J")
plt.legend()
plt.show()

---
## 🚀 Przykład użycia

```python
from parsers.csv_parser import load_csv
from timdr.timdr_filter import timdr
from latro.latro_core import latro
from model_j.model_j_detector import model_j

time, signal = load_csv("data/example_w7x_signal.csv")

reduced = timdr(signal)
lam, tau, rho = latro(signal)
points = model_j(signal)

print("Λ–τ–ρ:", lam, tau, rho)
print("Punkty Modelu J:", points[:10])


---
# jbackk-lang — Struktury Informacji, Modele Skrętu i Analiza Sygnałów

Organizacja skupiona na badaniu struktury informacji, redukcji wymiarów,
modelach skrętu oraz narzędziach do analizy sygnałów — od języka naturalnego,
przez dane techniczne, aż po diagnostykę plazmy w fuzji jądrowej.

Nasze projekty łączą:
- modele abstrakcyjne (GIA, Λ–τ–ρ, Model J),
- redukcję informacji (TIMDR),
- analizę sygnałów,
- narzędzia open‑source,
- zastosowania naukowe i inżynieryjne.

---

## 🔥 Projekty

### **fusion-tools**
Narzędzia do analizy danych z fuzji jądrowej (W7‑X, JET, DIII‑D, EAST)  
z wykorzystaniem modeli:
- TIMDR — redukcja informacji i defektów,
- Λ–τ–ρ — analiza strukturalna,
- Model J — detekcja punktów skrętu,
- GIA — interpretacja warstwowa.

Repozytorium zawiera:
- parsowanie danych (HDF5, MDSplus, CSV),
- filtry i ekstrakcję cech,
- wykrywanie anomalii,
- przykładowe notebooki,
- pipeline analizy plazmy.

---

## 🧠 Filozofia

Każdy sygnał — językowy, fizyczny, techniczny — ma strukturę.  
Naszym celem jest:
- wydobyć tę strukturę,
- zredukować szum,
- znaleźć punkty skrętu,
- zrozumieć transformacje,
- opisać defekty.

Modele GIA, TIMDR, Λ–τ–ρ i Model J powstały jako narzędzia
do pracy z informacją w sposób spójny, warstwowy i logiczny.

---

## 🌍 Zastosowania

- analiza sygnałów z fuzji jądrowej,
- wykrywanie anomalii w czasie rzeczywistym,
- przetwarzanie języka naturalnego,
- analiza danych technicznych,
- redukcja wymiarów,
- modele predykcyjne,
- wizualizacja struktury informacji.

---

## 🤝 Współpraca

Projekty są otwarte.  
Jeśli chcesz dołożyć własne moduły, diagnostyki, filtry lub modele — zapraszamy.

---

## 📜 Licencja

MIT — wolność tworzenia, wolność eksperymentowania.

---
## 🧪 Offline Demo — TIMDR + Λ–τ–ρ + Model J

Demo działa w pełni offline na sygnale `w7x_mirnov_example.csv`.

### Pipeline
1. **TIMDR** — redukcja szumu (różnica kolejnych próbek)  
2. **Λ–τ–ρ** — metryki strukturalne sygnału  
3. **Model J** — detekcja punktów skrętu (lokalne maksima)

### Kod demo

```python
import csv
import matplotlib.pyplot as plt

time = []
signal = []

with open("w7x_mirnov_example.csv") as f:
    reader = csv.reader(f)
    next(reader)
    for t, s in reader:
        time.append(float(t))
        signal.append(float(s))

def timdr_filter(x):
    return [x[i+1] - x[i] for i in range(len(x)-1)]

def latro(x):
    lam = max(x) - min(x)
    tau = sum(abs(v) for v in x) / len(x)
    rho = sum(v*v for v in x) / len(x)
    return lam, tau, rho

def model_j_points(x):
    pts = []
    for i in range(1, len(x)-1):
        if x[i] > x[i-1] and x[i] > x[i+1]:
            pts.append(i)
    return pts

reduced = timdr_filter(signal)
lam, tau, rho = latro(signal)
points = model_j_points(signal)

print("Λ–τ–ρ:", lam, tau, rho)

plt.figure(figsize=(12,5))
plt.plot(time, signal, label="sygnał")
plt.scatter([time[i] for i in points], [signal[i] for i in points],
            color="red", s=10, label="Model J")
plt.legend()
plt.show()
---
Wynik
Wykres pokazuje sygnał Mirnova z zaznaczonymi punktami Modelu J (czerwone markery).
---
# ⭐ MIT — rób, co chcesz, byle z głową.
