import sqlite3


class HandleDB():
    def __init__(self):
        self._con = sqlite3.connect('model/tfinal.db')
        self._cur = self._con.cursor()

    def get_users(self):
        users = []
        data = self._cur.execute("SELECT * FROM Users")
        for user in data:
            users.append({
                'Id': user[0],
                'Username': user[1],
                'Fullname': user[2],
                'isAdmin': False if user[4] == 0 else True
            })
        return users

    def get_user(self, userName="", Id=0):
        userDict = {}
        data = self._cur.execute(
            "SELECT Id, Username, Fullname, Password, isAdmin FROM Users where username = '{}' OR id = '{}' ".format(userName, Id))
        userData = data.fetchone()
        print(userData)
        if (userData):
            userDict["Id"] = userData[0]
            userDict["Username"] = userData[1]
            userDict["Fullname"] = userData[2]
            userDict["Password"] = userData[3]
            userDict["isAdmin"] = userData[4]
        return userDict

    def create_user(self, data_user):
        algo = self._cur.execute(
            "INSERT INTO Users VALUES('{}','{}', '{}', '{}', '{}')" .format(
                data_user["Id"],
                data_user["Username"],
                data_user["Fullname"],
                data_user["Password"],
                data_user["isAdmin"]
            ))
        self._con.commit()
        return self.get_user("", data_user["Id"])

    def validateUser(self, username, password):
        data = self._cur.execute(
            "SELECT * FROM Users where username = '{}' AND password = '{}' ".format(username, password))
        userValid = data.fetchone()
        if (userValid):
            user = self.get_user(userValid[1], userValid[0])
            self._con.close()
            return {'user': user, 'isValid': True}
        else:
            self._con.close()
            return {'user': {}, 'isValid': False}

    def get_artists(self, search):
        data = self._cur.execute(
            "SELECT * FROM Artist WHERE Name LIKE '%{}%' ORDER BY ArtistId DESC ".format(search))
        data = data.fetchall()
        self._con.close()
        return data

    def delete_artist(self, artistId):
        data = self._cur.execute(
            "DELETE FROM Artist WHERE ArtistId = '{}' ".format(artistId))
        data = data.fetchall()
        self._con.commit()
        self._con.close()
        return data

    def create_artist(self, nameArtist):
        algo = self._cur.execute(
            "INSERT INTO Artist (Name) VALUES('{}')" .format(nameArtist))
        algo = algo.fetchall()
        self._con.commit()
        return algo

    def __dell__(self):
        self._con.close()
