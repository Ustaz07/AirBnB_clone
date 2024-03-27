#!/usr/bin/python3
"""
Custom base class for the entire project
"""

from uuid import uuid4
from datetime import datetime

class BaseModel:
    """
    Custom base for all the classes in the AirBnb console project

    Attributes:
        id (str): Handles unique user identity
        created_at (datetime): Assigns current datetime
        updated_at (datetime): Updates current datetime

    Methods:
        __str__(): Prints the class name, id, and creates dictionary representations of the input values
        save(): Updates instance attributes with current datetime
        to_dict(): Returns the dictionary values of the instance object
    """

    DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

    def __init__(self, *args, **kwargs):
        """
        Public instance attributes initialization after creation

        Args:
            *args (args): Arguments
            **kwargs (dict): Attribute values
        """
        if not kwargs:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
        else:
            for key, value in kwargs.items():
                if key in ("updated_at", "created_at"):
                    setattr(self, key, datetime.strptime(value, self.DATE_TIME_FORMAT))
                elif key == "id":
                    setattr(self, key, str(value))
                else:
                    setattr(self, key, value)

    def __str__(self):
        """
        Returns string representation of the class
        """
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """
        Updates the public instance attribute:
        'updated_at' - with the current datetime
        """
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """
        Method returns a dictionary containing all
        keys/values of __dict__ instance
        """
        map_objects = {}
        for key, value in self.__dict__.items():
            if key == "created_at" or key == "updated_at":
                map_objects[key] = value.isoformat()
            else:
                map_objects[key] = value
        map_objects["__class__"] = self.__class__.__name__
        return map_objects

