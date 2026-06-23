# fusion-tools

A Python toolkit for fusion experiment data analysis.

## Repository structure

```
fusion-tools/
│
├── data/
│   ├── example_w7x_signal.csv     # Example W7-X time-series signals
│   └── example_metadata.json      # Shot metadata (device, diagnostics, …)
│
├── parsers/                        # Data format parsers
│   ├── __init__.py
│   ├── csv_parser.py              # CSVParser – read CSV signal files
│   ├── hdf5_parser.py             # HDF5Parser – read HDF5 data files
│   └── mdsplus_parser.py          # MDSplusParser – read MDSplus trees
│
├── timdr/                          # Time-Domain Reduction (TIMDR)
│   ├── __init__.py
│   ├── timdr_filter.py            # TimdrFilter – smoothing & filtering
│   └── timdr_visualization.py     # TimdrVisualizer – signal plotting
│
├── latro/                          # Localization & Anomaly Tracking (LATRO)
│   ├── __init__.py
│   ├── latro_core.py              # LatroCore – anomaly detection & segmentation
│   └── latro_features.py          # LatroFeatures – feature extraction
│
├── model_j/                        # Model-J disruption detector
│   ├── __init__.py
│   └── model_j_detector.py        # ModelJDetector – multi-signal warning system
│
└── demo/
    ├── fusion_demo.ipynb           # End-to-end demonstration notebook
    └── example_plots/              # Saved plot outputs
```

## Quick start

```python
from parsers import CSVParser
from timdr import TimdrFilter, TimdrVisualizer
from latro import LatroCore, LatroFeatures
from model_j import ModelJDetector

# Load data
parser = CSVParser('data/example_w7x_signal.csv',
                   metadata_path='data/example_metadata.json')
time     = parser.get_time()
signal   = parser.get_signal('signal_1')
metadata = parser.load_metadata()

# Filter
filt     = TimdrFilter(time, signal)
smoothed = filt.moving_average(window_size=5)

# Detect anomalies
core    = LatroCore(time, signal, threshold=2.5)
summary = core.event_summary()
print(summary)

# Extract features
feat = LatroFeatures(time, signal)
print(feat.feature_vector())

# Disruption check
detector = ModelJDetector(thresholds={'signal_1': (0.0, 0.15)})
detector.set_time(time)
detector.add_signal('signal_1', signal)
print(detector.summary())
```

See `demo/fusion_demo.ipynb` for a full walkthrough.