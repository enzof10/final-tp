from model.handle_db import HandleDB


class Users():
    data_user = {}

    def __init__(self, data_user):
        self.db = HandleDB()
        self.data_user =  data_user

    def save(self):
        # add id
        self._add_id()
        newUser = self.db.create_user(self.data_user)
        return newUser
    
    def get(self):
        print(self.data_user)
        # add id
        return "!ass"

    def _add_id(self):
        users = self.db.get_users()
        lastUser = users[-1]
        idUser = int(lastUser["Id"])
        self.data_user["Id"] = str(idUser + 1)






