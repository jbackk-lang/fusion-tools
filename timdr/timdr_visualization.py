"""
timdr_visualization.py - Visualization utilities for TIMDR-processed signals.

Generates time-series plots and comparative views of raw vs. filtered
fusion diagnostic data using matplotlib.
"""


class TimdrVisualizer:
    """Create plots for TIMDR-processed fusion diagnostic signals."""

    def __init__(self, time, signal, label="Signal", units="a.u."):
        """
        Initialize the visualizer.

        Parameters
        ----------
        time : list or array-like
            Time axis values (seconds).
        signal : list or array-like
            Signal amplitude values.
        label : str
            Human-readable name for the signal (used in plot legends).
        units : str
            Physical units for the signal amplitude axis.
        """
        self.time = list(time)
        self.signal = list(signal)
        self.label = label
        self.units = units

    # ------------------------------------------------------------------
    # Plot helpers
    # ------------------------------------------------------------------

    def _get_axes(self, ax):
        """Return the provided axes or create a new figure/axes pair."""
        try:
            import matplotlib.pyplot as plt
        except ImportError as exc:
            raise ImportError(
                "matplotlib is required for visualization. "
                "Install it with: pip install matplotlib"
            ) from exc

        if ax is None:
            _, ax = plt.subplots()
        return ax

    # ------------------------------------------------------------------
    # Public plotting methods
    # ------------------------------------------------------------------

    def plot_signal(self, ax=None, color="steelblue", title=None):
        """
        Plot the raw signal.

        Parameters
        ----------
        ax : matplotlib.axes.Axes, optional
            Axes to draw on. Creates a new figure if None.
        color : str
            Line colour.
        title : str, optional
            Plot title. Defaults to the signal label.

        Returns
        -------
        matplotlib.axes.Axes
        """
        ax = self._get_axes(ax)
        ax.plot(self.time, self.signal, color=color, label=self.label)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel(f"{self.label} ({self.units})")
        ax.set_title(title or self.label)
        ax.legend()
        return ax

    def plot_comparison(self, filtered_signal, filtered_label="Filtered",
                        ax=None, title=None):
        """
        Plot raw and filtered signals on the same axes for comparison.

        Parameters
        ----------
        filtered_signal : list or array-like
            Filtered signal values (same length as raw signal).
        filtered_label : str
            Legend label for the filtered trace.
        ax : matplotlib.axes.Axes, optional
            Axes to draw on.
        title : str, optional
            Plot title.

        Returns
        -------
        matplotlib.axes.Axes
        """
        ax = self._get_axes(ax)
        ax.plot(self.time, self.signal, color="lightsteelblue",
                alpha=0.7, label=f"{self.label} (raw)")
        ax.plot(self.time, filtered_signal, color="steelblue",
                linewidth=2, label=filtered_label)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel(f"{self.label} ({self.units})")
        ax.set_title(title or f"{self.label}: Raw vs Filtered")
        ax.legend()
        return ax

    def plot_spectrum(self, dt, ax=None, title=None):
        """
        Plot the power spectral density of the signal using a simple DFT.

        Requires numpy for FFT computation.

        Parameters
        ----------
        dt : float
            Sampling interval in seconds.
        ax : matplotlib.axes.Axes, optional
            Axes to draw on.
        title : str, optional
            Plot title.

        Returns
        -------
        matplotlib.axes.Axes
        """
        try:
            import math
        except ImportError:
            pass

        ax = self._get_axes(ax)

        n = len(self.signal)
        mean = sum(self.signal) / n
        centered = [v - mean for v in self.signal]

        try:
            import numpy as np
            freqs = np.fft.rfftfreq(n, d=dt)
            fft_vals = np.fft.rfft(centered)
            psd = (np.abs(fft_vals) ** 2) / n
        except ImportError:
            # Fallback: plot frequency index vs squared amplitude (no numpy)
            half = n // 2
            freqs = [i / (n * dt) for i in range(half)]
            psd = []
            for k in range(half):
                re = sum(centered[j] * math.cos(2 * math.pi * k * j / n)
                         for j in range(n))
                im = sum(centered[j] * math.sin(2 * math.pi * k * j / n)
                         for j in range(n))
                psd.append((re ** 2 + im ** 2) / n)

        ax.semilogy(freqs, psd, color="steelblue")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Power Spectral Density")
        ax.set_title(title or f"{self.label}: Power Spectrum")
        return ax

    def plot_outliers(self, outlier_indices, ax=None, title=None):
        """
        Highlight detected outlier points on a signal plot.

        Parameters
        ----------
        outlier_indices : list of int
            Indices of outlier samples to mark.
        ax : matplotlib.axes.Axes, optional
            Axes to draw on.
        title : str, optional
            Plot title.

        Returns
        -------
        matplotlib.axes.Axes
        """
        ax = self.plot_signal(ax=ax, title=title or f"{self.label}: Outliers")
        if outlier_indices:
            t_out = [self.time[i] for i in outlier_indices]
            s_out = [self.signal[i] for i in outlier_indices]
            ax.scatter(t_out, s_out, color="crimson", zorder=5,
                       label="Outliers")
            ax.legend()
        return ax

    def save(self, filepath, dpi=150):
        """
        Save the current matplotlib figure to a file.

        Parameters
        ----------
        filepath : str or Path
            Output file path (extension determines format, e.g. '.png', '.pdf').
        dpi : int
            Resolution in dots per inch.
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError as exc:
            raise ImportError(
                "matplotlib is required. Install it with: pip install matplotlib"
            ) from exc
        plt.savefig(filepath, dpi=dpi, bbox_inches="tight")
