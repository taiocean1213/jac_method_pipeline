import yaml
import pickle
import numpy as np
import json
import csv
from typing import Optional
from AttributeContainer import AttributeContainer

class AttributeContainerFactory:
    """A factory class for creating and saving instances of AttributeContainer."""


    def __init__(self):
        """Initialize an instance of AttributeContainerFactory."""
        return
    
    
    @staticmethod
    def load(self, filename: str) -> AttributeContainer:
        """Load data from a file and create an instance of AttributeContainer.

        Args:
            filename (str): The path to the data file.

        Returns:
            AttributeContainer: An instance of the AttributeContainer class.
        """
        data = None
        if filename.endswith(".yaml"):
            data = self._fromYaml(filename)
        elif filename.endswith(".pickle"):
            data = self._fromPickle(filename)
        elif filename.endswith(".npz"):
            data = self._fromNpz(filename)
        elif filename.endswith(".json"):
            data = self._fromJson(filename)
        elif filename.endswith(".csv"):
            data = self._fromCsv(filename)
        else:
            raise ValueError("Unsupported file type: {}".format(filename))
        return AttributeContainer(data)
    
    @staticmethod
    def _fromYaml(filename: str) -> AttributeContainer:
        """Create an instance of AttributeContainer from a YAML file.

        Args:
            filename (str): The path to the YAML file.

        Returns:
            AttributeContainer: An instance of the AttributeContainer class.
        """
        try:
            with open(filename, 'r') as f:
                data = yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError("Input file not found: {}".format(filename))
        except yaml.YAMLError:
            raise ValueError("Invalid YAML data in file: {}".format(filename))
        return AttributeContainer(data)
    
    @staticmethod
    def _fromPickle(filename: str) -> AttributeContainer:
        """Create an instance of AttributeContainer from a pickle file.

        Args:
            filename (str): The path to the pickle file.

        Returns:
            AttributeContainer: An instance of the AttributeContainer class.
        """
        try:
            with open(filename, 'rb') as f:
                data = pickle.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("Input file not found: {}".format(filename))
        except pickle.UnpicklingError:
            raise ValueError("Invalid pickle data in file: {}".format(filename))
        return data
    
    @staticmethod
    def _fromNpz(filename: str) -> AttributeContainer:
        """Create an instance of AttributeContainer from a npz file.

        Args:
            filename (str): The path to the npz file.

        Returns:
            AttributeContainer: An instance of the AttributeContainer class.
        """
        try:
            data = np.load(filename)
        except FileNotFoundError:
            raise FileNotFoundError("Input file not found: {}".format(filename))
        except ValueError:
            raise ValueError("Invalid npz data in file: {}".format(filename))
        return AttributeContainer(data)

    @staticmethod
    def _fromJson(filename: str) -> AttributeContainer:
        """Create an instance of AttributeContainer from a JSON file.

        Args:
            filename (str): The path to the JSON file.

        Returns:
            AttributeContainer: An instance of the AttributeContainer class.
        """
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("Input file not found: {}".format(filename))
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON data in file: {}".format(filename))
        return AttributeContainer(data)
    
    @staticmethod
    def _fromCsv(filename: str) -> AttributeContainer:
        """Create an instance of AttributeContainer from a CSV file.

        Args:
            filename (str): The path to the CSV file.

        Returns:
            AttributeContainer: An instance of the AttributeContainer class.
        """
        try:
            with open(filename, 'r') as f:
                reader = csv.reader(f)
                headers = next(reader)
                if not headers:
                    raise ValueError("CSV file must have a header row.")
                data = {header: [] for header in headers}
                for row in reader:
                    if len(row) != len(headers):
                        raise ValueError("CSV file has missing or extra columns.")
                    for i, value in enumerate(row):
                        data[headers[i]].append(value)
        except FileNotFoundError:
            raise FileNotFoundError("Input file not found: {}".format(filename))
        except csv.Error:
            raise ValueError("Invalid CSV data in file: {}".format(filename))
        return AttributeContainer(data)
