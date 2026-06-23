"""
timdr_filter.py - Time-Domain Reduction (TIMDR) filtering for fusion signals.

Provides noise reduction, smoothing, and signal conditioning methods
for fusion diagnostic time-series data.
"""

import math


class TimdrFilter:
    """Apply time-domain reduction and filtering to fusion signal data."""

    def __init__(self, time, signal):
        """
        Initialize the TIMDR filter with a time-series signal.

        Parameters
        ----------
        time : list or array-like
            Time axis values (seconds).
        signal : list or array-like
            Signal amplitude values corresponding to each time point.
        """
        self.time = list(time)
        self.signal = list(signal)

        if len(self.time) != len(self.signal):
            raise ValueError(
                f"time and signal must have the same length "
                f"(got {len(self.time)} and {len(self.signal)})."
            )

    # ------------------------------------------------------------------
    # Low-level helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _mean(values):
        return sum(values) / len(values) if values else 0.0

    @staticmethod
    def _std(values):
        if len(values) < 2:
            return 0.0
        m = TimdrFilter._mean(values)
        variance = sum((v - m) ** 2 for v in values) / (len(values) - 1)
        return math.sqrt(variance)

    # ------------------------------------------------------------------
    # Filters
    # ------------------------------------------------------------------

    def moving_average(self, window_size=5):
        """
        Smooth the signal using a centred moving average.

        Parameters
        ----------
        window_size : int
            Number of samples in the averaging window. Must be odd and >= 1.

        Returns
        -------
        list
            Smoothed signal values (same length as input).
        """
        if window_size < 1:
            raise ValueError("window_size must be >= 1.")
        if window_size % 2 == 0:
            raise ValueError("window_size must be odd for a centred filter.")

        half = window_size // 2
        n = len(self.signal)
        smoothed = []
        for i in range(n):
            start = max(0, i - half)
            end = min(n, i + half + 1)
            smoothed.append(self._mean(self.signal[start:end]))
        return smoothed

    def exponential_smoothing(self, alpha=0.3):
        """
        Apply first-order exponential smoothing (EWM).

        Parameters
        ----------
        alpha : float
            Smoothing factor in (0, 1]. Higher values give more weight to
            recent observations.

        Returns
        -------
        list
            Exponentially smoothed signal.
        """
        if not (0 < alpha <= 1):
            raise ValueError("alpha must be in the range (0, 1].")

        smoothed = [self.signal[0]]
        for i in range(1, len(self.signal)):
            smoothed.append(alpha * self.signal[i] + (1 - alpha) * smoothed[-1])
        return smoothed

    def bandpass_filter(self, dt, low_freq, high_freq):
        """
        Apply a simple finite-difference bandpass filter via running means.

        This is a lightweight approximation suitable for exploratory analysis.
        For production use, consider scipy.signal.butter with sosfiltfilt.

        Parameters
        ----------
        dt : float
            Sampling interval in seconds.
        low_freq : float
            Lower cut-off frequency in Hz.
        high_freq : float
            Upper cut-off frequency in Hz.

        Returns
        -------
        list
            Band-passed signal values.
        """
        if low_freq >= high_freq:
            raise ValueError("low_freq must be less than high_freq.")
        if dt <= 0:
            raise ValueError("dt must be positive.")

        low_window = max(1, int(round(1.0 / (high_freq * dt))))
        high_window = max(1, int(round(1.0 / (low_freq * dt))))

        if low_window % 2 == 0:
            low_window += 1
        if high_window % 2 == 0:
            high_window += 1

        low_pass_high = self._apply_centered_average(self.signal, low_window)
        low_pass_low = self._apply_centered_average(self.signal, high_window)

        return [h - l for h, l in zip(low_pass_high, low_pass_low)]

    @staticmethod
    def _apply_centered_average(signal, window):
        half = window // 2
        n = len(signal)
        result = []
        for i in range(n):
            start = max(0, i - half)
            end = min(n, i + half + 1)
            result.append(sum(signal[start:end]) / (end - start))
        return result

    def subtract_baseline(self, baseline_fraction=0.1):
        """
        Remove a baseline computed from the beginning of the signal.

        Parameters
        ----------
        baseline_fraction : float
            Fraction of the signal (from the start) used to estimate the
            baseline. Must be in (0, 1).

        Returns
        -------
        list
            Baseline-subtracted signal.
        """
        if not (0 < baseline_fraction < 1):
            raise ValueError("baseline_fraction must be in (0, 1).")

        n_baseline = max(1, int(len(self.signal) * baseline_fraction))
        baseline = self._mean(self.signal[:n_baseline])
        return [v - baseline for v in self.signal]

    def normalize(self, method="minmax"):
        """
        Normalize the signal to a standard range.

        Parameters
        ----------
        method : str
            Normalization method. Options:
            - ``'minmax'``: Scale to [0, 1].
            - ``'zscore'``: Zero-mean, unit-variance standardization.

        Returns
        -------
        list
            Normalized signal values.
        """
        if method == "minmax":
            sig_min = min(self.signal)
            sig_max = max(self.signal)
            span = sig_max - sig_min
            if span == 0:
                return [0.0] * len(self.signal)
            return [(v - sig_min) / span for v in self.signal]

        if method == "zscore":
            mean = self._mean(self.signal)
            std = self._std(self.signal)
            if std == 0:
                return [0.0] * len(self.signal)
            return [(v - mean) / std for v in self.signal]

        raise ValueError(f"Unknown normalization method: '{method}'.")

    def downsample(self, factor):
        """
        Reduce the signal by keeping every *factor*-th sample.

        Parameters
        ----------
        factor : int
            Decimation factor (>= 1).

        Returns
        -------
        tuple
            ``(time_downsampled, signal_downsampled)`` as lists.
        """
        if factor < 1:
            raise ValueError("factor must be >= 1.")
        t_ds = self.time[::factor]
        s_ds = self.signal[::factor]
        return t_ds, s_ds

    def detect_outliers(self, threshold=3.0):
        """
        Identify outlier indices using a z-score threshold.

        Parameters
        ----------
        threshold : float
            Number of standard deviations beyond which a point is an outlier.

        Returns
        -------
        list of int
            Indices of detected outlier samples.
        """
        mean = self._mean(self.signal)
        std = self._std(self.signal)
        if std == 0:
            return []
        return [
            i for i, v in enumerate(self.signal)
            if abs((v - mean) / std) > threshold
        ]
