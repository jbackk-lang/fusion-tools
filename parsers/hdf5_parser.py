"""
hdf5_parser.py - Parser for HDF5-formatted fusion experiment data.

HDF5 (Hierarchical Data Format 5) is widely used in fusion research
for storing large, structured scientific datasets.
"""

from pathlib import Path


class HDF5Parser:
    """Parse HDF5 files containing fusion experiment data."""

    def __init__(self, filepath):
        """
        Initialize the HDF5 parser.

        Parameters
        ----------
        filepath : str or Path
            Path to the HDF5 file.
        """
        self.filepath = Path(filepath)
        self._file = None
        self._datasets = None

    def open(self):
        """
        Open the HDF5 file for reading.

        Requires the ``h5py`` package to be installed.

        Returns
        -------
        self
            Returns the parser instance to allow chaining.

        Raises
        ------
        ImportError
            If h5py is not installed.
        FileNotFoundError
            If the HDF5 file does not exist.
        """
        try:
            import h5py
        except ImportError as exc:
            raise ImportError(
                "h5py is required to read HDF5 files. "
                "Install it with: pip install h5py"
            ) from exc

        if not self.filepath.exists():
            raise FileNotFoundError(f"HDF5 file not found: {self.filepath}")

        self._file = h5py.File(self.filepath, "r")
        return self

    def close(self):
        """Close the HDF5 file."""
        if self._file is not None:
            self._file.close()
            self._file = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def list_datasets(self, group="/"):
        """
        List all dataset paths within a group.

        Parameters
        ----------
        group : str
            HDF5 group path to inspect. Defaults to root '/'.

        Returns
        -------
        list of str
            Absolute dataset paths.
        """
        if self._file is None:
            raise RuntimeError("File is not open. Call open() first.")

        datasets = []

        def _visitor(name, obj):
            import h5py
            if isinstance(obj, h5py.Dataset):
                datasets.append("/" + name)

        self._file[group].visititems(_visitor)
        return datasets

    def read_dataset(self, path):
        """
        Read a dataset by its HDF5 path.

        Parameters
        ----------
        path : str
            Full path to the HDF5 dataset (e.g. '/diagnostics/thomson/Te').

        Returns
        -------
        numpy.ndarray
            Dataset values as a NumPy array.

        Raises
        ------
        KeyError
            If the dataset path does not exist.
        """
        if self._file is None:
            raise RuntimeError("File is not open. Call open() first.")

        if path not in self._file:
            raise KeyError(f"Dataset not found: {path}")

        return self._file[path][()]

    def read_attributes(self, path="/"):
        """
        Read attributes attached to a group or dataset.

        Parameters
        ----------
        path : str
            HDF5 path to the group or dataset.

        Returns
        -------
        dict
            Attribute key-value pairs.
        """
        if self._file is None:
            raise RuntimeError("File is not open. Call open() first.")

        if path not in self._file:
            raise KeyError(f"Path not found: {path}")

        return dict(self._file[path].attrs)

    def read_all(self):
        """
        Read all datasets from the file into a nested dictionary.

        Returns
        -------
        dict
            Nested dictionary mapping dataset paths to NumPy arrays.
        """
        result = {}
        for path in self.list_datasets():
            result[path] = self.read_dataset(path)
        return result
