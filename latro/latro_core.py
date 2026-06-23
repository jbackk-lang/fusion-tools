"""
latro_core.py - Core algorithms for Localization and Anomaly Tracking (LATRO).

Implements event detection, segmentation, and anomaly scoring for
fusion diagnostic time-series signals.
"""

import math


class LatroCore:
    """Core LATRO analysis engine for fusion signal anomaly tracking."""

    def __init__(self, time, signal, threshold=2.5):
        """
        Initialize LATRO core with a time-series signal.

        Parameters
        ----------
        time : list or array-like
            Time axis values (seconds).
        signal : list or array-like
            Signal amplitude values.
        threshold : float
            Z-score threshold above which a sample is flagged as anomalous.
        """
        self.time = list(time)
        self.signal = list(signal)
        self.threshold = threshold

        if len(self.time) != len(self.signal):
            raise ValueError(
                "time and signal must have the same length."
            )

    # ------------------------------------------------------------------
    # Statistical helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _mean(values):
        return sum(values) / len(values) if values else 0.0

    @staticmethod
    def _std(values):
        if len(values) < 2:
            return 0.0
        m = LatroCore._mean(values)
        return math.sqrt(sum((v - m) ** 2 for v in values) / (len(values) - 1))

    # ------------------------------------------------------------------
    # Anomaly detection
    # ------------------------------------------------------------------

    def zscore(self):
        """
        Compute the z-score of each sample relative to the full signal.

        Returns
        -------
        list of float
            Z-score for each time point.
        """
        mean = self._mean(self.signal)
        std = self._std(self.signal)
        if std == 0:
            return [0.0] * len(self.signal)
        return [(v - mean) / std for v in self.signal]

    def detect_anomalies(self):
        """
        Identify time indices where the z-score exceeds the threshold.

        Returns
        -------
        list of int
            Indices of anomalous samples.
        """
        scores = self.zscore()
        return [i for i, z in enumerate(scores) if abs(z) > self.threshold]

    def anomaly_score(self):
        """
        Return per-sample anomaly scores (absolute z-scores).

        Returns
        -------
        list of float
        """
        return [abs(z) for z in self.zscore()]

    # ------------------------------------------------------------------
    # Event segmentation
    # ------------------------------------------------------------------

    def segment_events(self, min_gap=5):
        """
        Group consecutive anomalous indices into discrete events.

        Parameters
        ----------
        min_gap : int
            Minimum number of non-anomalous samples required to separate
            two distinct events.

        Returns
        -------
        list of dict
            Each dict contains:
            - ``'start'``: index of event start
            - ``'end'``: index of event end (inclusive)
            - ``'peak_index'``: index of peak anomaly within the event
            - ``'peak_score'``: anomaly score at peak
            - ``'time_start'``: time at event start
            - ``'time_end'``: time at event end
        """
        indices = self.detect_anomalies()
        if not indices:
            return []

        scores = self.anomaly_score()
        groups = []
        current = [indices[0]]

        for idx in indices[1:]:
            if idx - current[-1] <= min_gap:
                current.append(idx)
            else:
                groups.append(current)
                current = [idx]
        groups.append(current)

        events = []
        for group in groups:
            peak_idx = max(group, key=lambda i: scores[i])
            events.append({
                "start": group[0],
                "end": group[-1],
                "peak_index": peak_idx,
                "peak_score": scores[peak_idx],
                "time_start": self.time[group[0]],
                "time_end": self.time[group[-1]],
            })
        return events

    # ------------------------------------------------------------------
    # Localization
    # ------------------------------------------------------------------

    def localize_peak(self):
        """
        Return the time of the maximum anomaly score.

        Returns
        -------
        float or None
            Time (seconds) of the peak anomaly, or None if no anomaly found.
        """
        anomalies = self.detect_anomalies()
        if not anomalies:
            return None
        scores = self.anomaly_score()
        peak_idx = max(anomalies, key=lambda i: scores[i])
        return self.time[peak_idx]

    def event_summary(self):
        """
        Produce a summary of detected events.

        Returns
        -------
        dict
            Keys: ``'n_anomalous_samples'``, ``'n_events'``,
            ``'peak_time'``, ``'peak_score'``, ``'events'``.
        """
        anomalies = self.detect_anomalies()
        events = self.segment_events()
        scores = self.anomaly_score()

        peak_time = None
        peak_score = 0.0
        if anomalies:
            peak_idx = max(anomalies, key=lambda i: scores[i])
            peak_time = self.time[peak_idx]
            peak_score = scores[peak_idx]

        return {
            "n_anomalous_samples": len(anomalies),
            "n_events": len(events),
            "peak_time": peak_time,
            "peak_score": peak_score,
            "events": events,
        }
