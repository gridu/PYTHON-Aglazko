from abc import ABCMeta, abstractmethod


class IAnimalCenter:
    __metaclass__ = ABCMeta

    # @staticmethod
    @abstractmethod
    def deserialize(self, record=None, long=False):
        """Create dict from object"""

    @abstractmethod
    def get_centers(self):
        """Show all animal centers"""

    @abstractmethod
    def get_center_inform(self, id):
        """Get detailed information about center"""

    @abstractmethod
    def get_center_by_login(self, user_login):
        """Get center inform by login"""


class IAccessRequest:
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_access_request(self, user_id):
        """Create access request"""


class ISpecies:
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def deserialize(record=None, long=False):
        """To create dictionary"""

    @staticmethod
    @abstractmethod
    def get_species():
        """Get all species"""

    @staticmethod
    @abstractmethod
    def get_species_inform(self, id):
        """Get inform about species"""

    @abstractmethod
    def add_species(self, data):
        """Add new specie."""


class IAnimal:
    __metaclass__ = ABCMeta

    @abstractmethod
    def deserialize(self, record=None, long=False):
        """To create dictionary"""

    @abstractmethod
    def get_animals(self):
        """To show all animals"""

    @abstractmethod
    def get_animal(self, animal_id):
        """Show inform about animal"""

    @abstractmethod
    def delete_animal(self, animal_id):
        """Delete animal"""

    @abstractmethod
    def update_animal(self, animal=None, data_upd=None, animal_id=None):
        """Update animal"""

    @abstractmethod
    def add_animal(self, data, userid):
        """Add animal."""
