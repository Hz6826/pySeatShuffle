"""
Person Model
"""

class Person:
    def __init__(self, name: str, properties: dict):
        self.name = name
        self.properties = properties

    def get_property(self, property_name: str):
        return self.properties.get(property_name)
