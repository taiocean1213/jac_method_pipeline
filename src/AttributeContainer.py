class AttributeContainer:
    """A class for setting class attributes based on dictionary keys."""
    
    def _setAttributes(self, myDict):
        """Set class attributes based on dictionary keys.

        Args:
            myDict (dict): A dictionary with the keys being the attribute names
                and the values being the attribute values.
        """
        for key in myDict:
            setattr(self, key, myDict[key]) # Set each attribute using setattr()

    def __init__(self, myDict):
        """Initialize an instance of AttributeContainer.

        Args:
            myDict (dict): A dictionary with the keys being the attribute names
                and the values being the attribute values.
        """
        self._setAttributes(myDict) # Call the _setAttributes method to set the attributes
        return
    
    def getAttributes(self):
        """Return a dictionary of instance attributes.

        Returns:
            dict: A dictionary with the keys being the attribute names
                and the values being the attribute values.
        """
        return {attr: getattr(self, attr) for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")}

