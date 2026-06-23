"""
model_j_detector.py - Model-J disruption precursor detector.

Implements a threshold-based disruption warning system for fusion plasma
experiments. Model-J monitors multiple diagnostic signals simultaneously
and issues warnings when configurable danger thresholds are breached.

The name refers to the J-invariant (rotational transform) used in
stellarator physics, but the detector applies broadly to tokamaks and
stellarators alike.
"""

import math


class ModelJDetector:
    """
    Multi-signal disruption precursor detector (Model-J).

    Monitors a set of named diagnostic signals and raises disruption
    warnings when signal values cross preset thresholds.
    """

    def __init__(self, thresholds=None, warning_window=5):
        """
        Initialize the Model-J detector.

        Parameters
        ----------
        thresholds : dict, optional
            Mapping of signal name → (low, high) tuple defining the safe
            operating window. Values outside [low, high] trigger a warning.
            Example::

                {
                    'Te': (0.5, 8.0),
                    'ne': (0.5e19, 5.0e19),
                    'beta': (0.0, 4.0),
                }

        warning_window : int
            Number of consecutive samples that must exceed a threshold
            before a warning is confirmed (debounce filter).
        """
        self.thresholds = thresholds or {}
        self.warning_window = max(1, int(warning_window))
        self._signals = {}
        self._time = None

    # ------------------------------------------------------------------
    # Data ingestion
    # ------------------------------------------------------------------

    def set_time(self, time):
        """
        Set the shared time axis for all signals.

        Parameters
        ----------
        time : list or array-like
            Time values in seconds.
        """
        self._time = list(time)

    def add_signal(self, name, values):
        """
        Register a diagnostic signal with the detector.

        Parameters
        ----------
        name : str
            Signal identifier (must match a key in ``thresholds`` to be
            actively monitored).
        values : list or array-like
            Signal amplitude values (must match the length of the time axis
            if one has been set).
        """
        values = list(values)
        if self._time is not None and len(values) != len(self._time):
            raise ValueError(
                f"Signal '{name}' has {len(values)} samples but time axis "
                f"has {len(self._time)} points."
            )
        self._signals[name] = values

    def set_threshold(self, name, low, high):
        """
        Set or update the safe-operating threshold for a signal.

        Parameters
        ----------
        name : str
            Signal name.
        low : float
            Lower bound of the safe window.
        high : float
            Upper bound of the safe window.
        """
        if low >= high:
            raise ValueError(
                f"Threshold low ({low}) must be less than high ({high})."
            )
        self.thresholds[name] = (low, high)

    # ------------------------------------------------------------------
    # Detection
    # ------------------------------------------------------------------

    def _exceeds_threshold(self, value, low, high):
        """Return True if value is outside [low, high]."""
        return value < low or value > high

    def detect(self):
        """
        Run disruption precursor detection on all registered signals.

        A warning is raised for a signal when ``warning_window`` or more
        consecutive samples fall outside the defined threshold window.

        Returns
        -------
        dict
            Mapping of signal name → list of warning event dicts.
            Each event dict contains:

            - ``'start_index'``: first sample index of the breach
            - ``'end_index'``: last sample index of the breach
            - ``'start_time'``: corresponding start time (None if no time axis)
            - ``'end_time'``: corresponding end time (None if no time axis)
            - ``'max_exceedance'``: maximum distance outside the threshold window
            - ``'direction'``: ``'high'`` or ``'low'``
        """
        results = {}

        for name, values in self._signals.items():
            if name not in self.thresholds:
                continue

            low, high = self.thresholds[name]
            warnings = []
            breach_start = None
            consecutive = 0
            max_exc = 0.0
            direction = None

            for i, v in enumerate(values):
                if self._exceeds_threshold(v, low, high):
                    exc = max(v - high, low - v)
                    dir_i = "high" if v > high else "low"
                    if breach_start is None:
                        breach_start = i
                        direction = dir_i
                        max_exc = exc
                    else:
                        max_exc = max(max_exc, exc)
                    consecutive += 1
                else:
                    if consecutive >= self.warning_window and breach_start is not None:
                        warnings.append(
                            self._make_event(breach_start, i - 1, max_exc, direction)
                        )
                    breach_start = None
                    consecutive = 0
                    max_exc = 0.0
                    direction = None

            # Handle breach that extends to the end of the signal
            if consecutive >= self.warning_window and breach_start is not None:
                warnings.append(
                    self._make_event(breach_start, len(values) - 1, max_exc, direction)
                )

            results[name] = warnings

        return results

    def _make_event(self, start, end, max_exc, direction):
        t_start = self._time[start] if self._time else None
        t_end = self._time[end] if self._time else None
        return {
            "start_index": start,
            "end_index": end,
            "start_time": t_start,
            "end_time": t_end,
            "max_exceedance": max_exc,
            "direction": direction,
        }

    def is_disruption_imminent(self, lookahead=10):
        """
        Perform a quick-look assessment of disruption imminence.

        Inspects only the last ``lookahead`` samples of each signal.

        Parameters
        ----------
        lookahead : int
            Number of recent samples to assess.

        Returns
        -------
        bool
            True if any monitored signal has exceeded its threshold in the
            most recent ``lookahead`` samples for at least one consecutive
            breach.
        """
        for name, values in self._signals.items():
            if name not in self.thresholds:
                continue
            low, high = self.thresholds[name]
            window = values[-lookahead:]
            if any(self._exceeds_threshold(v, low, high) for v in window):
                return True
        return False

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def summary(self):
        """
        Return a high-level summary of the detection results.

        Returns
        -------
        dict
            Keys: ``'monitored_signals'``, ``'total_warnings'``,
            ``'warnings_per_signal'``, ``'disruption_imminent'``.
        """
        results = self.detect()
        warnings_per_signal = {k: len(v) for k, v in results.items()}
        total = sum(warnings_per_signal.values())

        return {
            "monitored_signals": list(results.keys()),
            "total_warnings": total,
            "warnings_per_signal": warnings_per_signal,
            "disruption_imminent": self.is_disruption_imminent(),
        }
