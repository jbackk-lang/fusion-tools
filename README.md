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
---
# ⭐ MIT — rób, co chcesz, byle z głową.
Chcesz, żebym przygotował **README na stronę główną Twojej organizacji GitHub** (`jbackk-lang.github.io`) w tym samym stylu?
