"""
latro_features.py - Feature extraction for LATRO anomaly analysis.

Computes statistical and physics-motivated features from fusion signal
segments to support downstream classification and machine learning tasks.
"""

import math


class LatroFeatures:
    """Extract features from fusion diagnostic signal segments."""

    def __init__(self, time, signal):
        """
        Initialize feature extractor for a signal segment.

        Parameters
        ----------
        time : list or array-like
            Time axis values (seconds).
        signal : list or array-like
            Signal amplitude values for the segment.
        """
        self.time = list(time)
        self.signal = list(signal)

        if len(self.time) != len(self.signal):
            raise ValueError("time and signal must have the same length.")

        if len(self.signal) == 0:
            raise ValueError("Signal must not be empty.")

    # ------------------------------------------------------------------
    # Low-level helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _mean(values):
        return sum(values) / len(values)

    @staticmethod
    def _std(values):
        if len(values) < 2:
            return 0.0
        m = LatroFeatures._mean(values)
        return math.sqrt(sum((v - m) ** 2 for v in values) / (len(values) - 1))

    # ------------------------------------------------------------------
    # Statistical features
    # ------------------------------------------------------------------

    def mean(self):
        """Return the arithmetic mean of the signal."""
        return self._mean(self.signal)

    def std(self):
        """Return the standard deviation of the signal."""
        return self._std(self.signal)

    def variance(self):
        """Return the variance of the signal."""
        return self.std() ** 2

    def rms(self):
        """Return the root-mean-square (RMS) amplitude."""
        return math.sqrt(self._mean([v ** 2 for v in self.signal]))

    def peak_to_peak(self):
        """Return the peak-to-peak amplitude (max - min)."""
        return max(self.signal) - min(self.signal)

    def skewness(self):
        """
        Return the sample skewness (third standardised moment).

        Returns
        -------
        float
            Skewness value. 0 for a symmetric distribution.
        """
        n = len(self.signal)
        if n < 3:
            return 0.0
        m = self._mean(self.signal)
        s = self._std(self.signal)
        if s == 0:
            return 0.0
        return sum(((v - m) / s) ** 3 for v in self.signal) * n / ((n - 1) * (n - 2))

    def kurtosis(self):
        """
        Return the excess kurtosis (fourth standardised moment minus 3).

        Returns
        -------
        float
            Excess kurtosis. 0 for a normal distribution.
        """
        n = len(self.signal)
        if n < 4:
            return 0.0
        m = self._mean(self.signal)
        s = self._std(self.signal)
        if s == 0:
            return 0.0
        k4 = sum(((v - m) / s) ** 4 for v in self.signal)
        return (n * (n + 1) * k4 / ((n - 1) * (n - 2) * (n - 3))
                - 3 * (n - 1) ** 2 / ((n - 2) * (n - 3)))

    def zero_crossing_rate(self):
        """
        Compute the fraction of consecutive sample pairs that cross zero.

        Returns
        -------
        float
            Zero-crossing rate in [0, 1].
        """
        if len(self.signal) < 2:
            return 0.0
        crossings = sum(
            1 for i in range(len(self.signal) - 1)
            if self.signal[i] * self.signal[i + 1] < 0
        )
        return crossings / (len(self.signal) - 1)

    def energy(self):
        """Return the total signal energy (sum of squared amplitudes)."""
        return sum(v ** 2 for v in self.signal)

    # ------------------------------------------------------------------
    # Temporal features
    # ------------------------------------------------------------------

    def duration(self):
        """Return the time span of the segment (last time - first time)."""
        return self.time[-1] - self.time[0]

    def rise_time(self, low_frac=0.1, high_frac=0.9):
        """
        Estimate the signal rise time from low_frac to high_frac of peak.

        Parameters
        ----------
        low_frac : float
            Lower amplitude fraction (default 10 %).
        high_frac : float
            Upper amplitude fraction (default 90 %).

        Returns
        -------
        float or None
            Rise time in seconds, or None if thresholds are not crossed.
        """
        sig_max = max(self.signal)
        lo = low_frac * sig_max
        hi = high_frac * sig_max

        t_lo = t_hi = None
        for t, v in zip(self.time, self.signal):
            if t_lo is None and v >= lo:
                t_lo = t
            if t_hi is None and v >= hi:
                t_hi = t

        if t_lo is not None and t_hi is not None:
            return t_hi - t_lo
        return None

    def centroid_time(self):
        """
        Compute the energy-weighted temporal centroid of the signal.

        Returns
        -------
        float
            Centroid time in seconds.
        """
        total_energy = sum(v ** 2 for v in self.signal)
        if total_energy == 0:
            return self._mean(self.time)
        return sum(t * v ** 2 for t, v in zip(self.time, self.signal)) / total_energy

    # ------------------------------------------------------------------
    # Aggregate feature vector
    # ------------------------------------------------------------------

    def feature_vector(self):
        """
        Compute all scalar features and return them as a dictionary.

        Returns
        -------
        dict
            Feature name → scalar value mapping.
        """
        return {
            "mean": self.mean(),
            "std": self.std(),
            "variance": self.variance(),
            "rms": self.rms(),
            "peak_to_peak": self.peak_to_peak(),
            "skewness": self.skewness(),
            "kurtosis": self.kurtosis(),
            "zero_crossing_rate": self.zero_crossing_rate(),
            "energy": self.energy(),
            "duration": self.duration(),
            "rise_time": self.rise_time(),
            "centroid_time": self.centroid_time(),
        }

    def feature_names(self):
        """
        Return the ordered list of feature names produced by feature_vector().

        Returns
        -------
        list of str
        """
        return list(self.feature_vector().keys())
