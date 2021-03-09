class User:
    pass_try = 3

    def __init__(self, username='', role='', status=''):
        self.__Username = username
        self.__Role = role
        self.__Status = status

    def get_username(self):

        return self.__Username

    def get_role(self):

        return self.__Role

    def get_status(self):

        return self.__Status

    def set_username(self, username):

        self.__Username = username

    def set_role(self, role):

        self.__Role = role

    def set_status(self, status):

        self.__Status = status

    def set_all(self, username, role, status):

        self.__Username = username
        self.__Role = role
        self.__Status = status
