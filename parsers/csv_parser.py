"""
csv_parser.py - Parser for CSV-formatted fusion experiment signal data.
"""

import csv
import json
import os
from pathlib import Path


class CSVParser:
    """Parse CSV files containing fusion experiment time-series signals."""

    def __init__(self, filepath, metadata_path=None):
        """
        Initialize the CSV parser.

        Parameters
        ----------
        filepath : str or Path
            Path to the CSV data file.
        metadata_path : str or Path, optional
            Path to a JSON metadata file associated with the data.
        """
        self.filepath = Path(filepath)
        self.metadata_path = Path(metadata_path) if metadata_path else None
        self._data = None
        self._metadata = None

    def load(self):
        """
        Load data from the CSV file.

        Returns
        -------
        dict
            Dictionary with column names as keys and lists of values.
        """
        if not self.filepath.exists():
            raise FileNotFoundError(f"CSV file not found: {self.filepath}")

        data = {}
        with open(self.filepath, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                for key, value in row.items():
                    if key not in data:
                        data[key] = []
                    try:
                        data[key].append(float(value))
                    except (ValueError, TypeError):
                        data[key].append(value)

        self._data = data
        return data

    def load_metadata(self):
        """
        Load associated metadata from a JSON file.

        Returns
        -------
        dict
            Metadata dictionary, or empty dict if no metadata file is set.
        """
        if self.metadata_path is None:
            return {}

        if not self.metadata_path.exists():
            raise FileNotFoundError(
                f"Metadata file not found: {self.metadata_path}"
            )

        with open(self.metadata_path) as f:
            self._metadata = json.load(f)

        return self._metadata

    @property
    def data(self):
        """Return loaded data, loading from file if not yet loaded."""
        if self._data is None:
            self.load()
        return self._data

    @property
    def metadata(self):
        """Return loaded metadata, loading from file if not yet loaded."""
        if self._metadata is None:
            self.load_metadata()
        return self._metadata

    def get_signal(self, name):
        """
        Retrieve a single signal column by name.

        Parameters
        ----------
        name : str
            Column name of the signal to retrieve.

        Returns
        -------
        list
            List of signal values.

        Raises
        ------
        KeyError
            If the signal name is not found in the data.
        """
        return self.data[name]

    def get_time(self):
        """
        Return the time axis, assumed to be the first column or named 'time'.

        Returns
        -------
        list
            List of time values.
        """
        if "time" in self.data:
            return self.data["time"]
        columns = list(self.data.keys())
        if columns:
            return self.data[columns[0]]
        raise ValueError("No time column found in data.")

    def list_signals(self):
        """
        List all available signal names (excluding the time column).

        Returns
        -------
        list of str
            Signal column names.
        """
        return [col for col in self.data.keys() if col != "time"]

    def to_dict(self):
        """
        Return all loaded data as a plain dictionary.

        Returns
        -------
        dict
        """
        return dict(self.data)
