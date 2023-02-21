from pprint import pprint
def create_user(conn, cur, user):
    """
    Inserts the user into the database
    
    :param conn: the connection to the database
    :param cur: the cursor object
    :param user: a tuple of the form (username, fullname, password, isAdmin)
    :return: The user id
    """
    sql = '''INSERT INTO Users (Username,Fullname,Password,IsAdmin) VALUES (?,?,?,?)'''

    cur.execute(sql, user)
    
    conn.commit()

    return cur.lastrowid

def logIn(conn, cur, username, password):
    """
    Inserts the user into the database
    
    :param conn: the connection to the database
    :param cur: the cursor object
    :param user: a tuple of the form (username, fullname, password, isAdmin)
    :return: The user id
    """
    sql = f'''SELECT Username FROM Users WHERE Username = "{username}" AND Password = "{password}"'''

    cur.execute(sql)
    
    response = cur.fetchone()

    return response

def albumAndArtist(conn, cur):
    sql = f'''SELECT Album.ArtistId, Album.title, Artist.name, Track.name
                FROM Album 
                INNER JOIN Artist
                ON Album.ArtistId = Artist.ArtistId
                INNER JOIN Track ON Album.AlbumId=Track.AlbumId
                '''

    cur.execute(sql)
    
    response = cur.fetchall()
    return response

def getColumns(conn, cur, table):
    sql = f'''SELECT * FROM "{table}" '''
    data = cur.execute(sql)
    columns = []
    for column in data.description:
        columns.append(column[0])

    return columns

def getLastRegister(conn, cur, table, column):
    sql = f'''SELECT * FROM {table} ORDER BY {column} DESC LIMIT 1; '''
    cur.execute(sql)
    data = cur.fetchone()

    return data

def create_artist(conn, cur, artist):
    """
    Inserts the artist into the database
    
    :param conn: the connection to the database
    :param cur: the cursor object
    :param user: a tuple of the form (username, fullname, password, isAdmin)
    :return: The user id
    """
    sql = '''INSERT INTO Artist (ArtistId, Name) VALUES (?,?)'''

    cur.execute(sql, artist)
    
    conn.commit()

    return cur.lastrowid