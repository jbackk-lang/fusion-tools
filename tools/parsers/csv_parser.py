import numpy as np
import pandas as pd

def load_csv(path):
    df = pd.read_csv(path)
    time = df.iloc[:, 0].values
    signal = df.iloc[:, 1].values
    return time, signal
