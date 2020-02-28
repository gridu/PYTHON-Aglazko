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
