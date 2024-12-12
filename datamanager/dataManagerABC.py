from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    """ Abstract class to retrieve data from the database """

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass
