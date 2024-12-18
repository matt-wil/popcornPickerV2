from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    """ Abstract class to retrieve data from the database """

    @abstractmethod
    def get_all_users(self):
        """Get all users from the database"""
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """Get all movies from the database"""
        pass
