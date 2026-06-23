"""
mdsplus_parser.py - Parser for MDSplus data from fusion experiments.

MDSplus is a data acquisition and management system widely used in
tokamak and stellarator fusion experiments worldwide (e.g. Alcator C-Mod,
ASDEX Upgrade, EAST, W7-X).
"""

from pathlib import Path


class MDSplusParser:
    """Read signal data from an MDSplus tree."""

    def __init__(self, server=None, tree=None, shot=None):
        """
        Initialize the MDSplus parser.

        Parameters
        ----------
        server : str, optional
            Hostname or IP of the MDSplus server. Use None for a local tree.
        tree : str, optional
            Name of the MDSplus tree (e.g. 'electrons', 'magnetics').
        shot : int, optional
            Shot (pulse) number to open.
        """
        self.server = server
        self.tree = tree
        self.shot = shot
        self._connection = None
        self._tree_obj = None

    def connect(self):
        """
        Connect to the MDSplus server or open a local tree.

        Requires the ``MDSplus`` Python package to be installed.

        Returns
        -------
        self

        Raises
        ------
        ImportError
            If the MDSplus package is not installed.
        """
        try:
            import MDSplus
        except ImportError as exc:
            raise ImportError(
                "MDSplus Python package is required. "
                "See https://www.mdsplus.org/ for installation instructions."
            ) from exc

        if self.server:
            self._connection = MDSplus.Connection(self.server)
        else:
            self._connection = None

        return self

    def open_tree(self, tree=None, shot=None):
        """
        Open a tree for a specific shot.

        Parameters
        ----------
        tree : str, optional
            Tree name. Overrides the value set in __init__ if provided.
        shot : int, optional
            Shot number. Overrides the value set in __init__ if provided.

        Returns
        -------
        self
        """
        try:
            import MDSplus
        except ImportError as exc:
            raise ImportError(
                "MDSplus Python package is required. "
                "See https://www.mdsplus.org/ for installation instructions."
            ) from exc

        tree = tree or self.tree
        shot = shot or self.shot

        if tree is None or shot is None:
            raise ValueError("Both tree and shot must be specified.")

        if self._connection is not None:
            self._connection.openTree(tree, shot)
        else:
            self._tree_obj = MDSplus.Tree(tree, shot)

        self.tree = tree
        self.shot = shot
        return self

    def get_signal(self, node_path):
        """
        Retrieve the data array for a given MDSplus node.

        Parameters
        ----------
        node_path : str
            Dotted node path within the tree (e.g. '\\TOP.ELECTRONS:TE').

        Returns
        -------
        numpy.ndarray
            Signal data values.
        """
        return self._evaluate(node_path)

    def get_time(self, node_path):
        """
        Retrieve the time dimension for a signal node.

        Parameters
        ----------
        node_path : str
            Dotted node path.

        Returns
        -------
        numpy.ndarray
            Time axis values in seconds.
        """
        return self._evaluate(f"DIM_OF({node_path})")

    def get_units(self, node_path):
        """
        Retrieve the physical units of a node's data.

        Parameters
        ----------
        node_path : str
            Dotted node path.

        Returns
        -------
        str
            Unit string (e.g. 'keV', 'm^-3').
        """
        return self._evaluate(f"UNITS_OF({node_path})")

    def _evaluate(self, expression):
        """
        Evaluate an MDSplus TDI expression.

        Parameters
        ----------
        expression : str
            TDI expression string.

        Returns
        -------
        object
            Result of the TDI evaluation (typically a numpy array or scalar).
        """
        try:
            import MDSplus
        except ImportError as exc:
            raise ImportError(
                "MDSplus Python package is required."
            ) from exc

        if self._connection is not None:
            result = self._connection.get(expression)
        elif self._tree_obj is not None:
            result = self._tree_obj.tdiExecute(expression)
        else:
            raise RuntimeError(
                "No active connection or open tree. "
                "Call connect() and open_tree() first."
            )
        return result.data()

    def list_nodes(self, path="\\TOP", usage="SIGNAL"):
        """
        List nodes under a given path with the specified usage type.

        Parameters
        ----------
        path : str
            Node path to search under.
        usage : str
            MDSplus node usage type (e.g. 'SIGNAL', 'NUMERIC', 'TEXT').

        Returns
        -------
        list of str
            Matching node path strings.
        """
        expression = f"GETNCI({path},'NODE_NAME')"
        try:
            result = self._evaluate(expression)
            if hasattr(result, "tolist"):
                return result.tolist()
            return list(result)
        except Exception:
            return []

    def close(self):
        """Close the tree and connection."""
        try:
            if self._connection is not None:
                self._connection.closeAllTrees()
        except Exception:
            pass
        self._connection = None
        self._tree_obj = None

    def __enter__(self):
        self.connect()
        if self.tree and self.shot:
            self.open_tree()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
