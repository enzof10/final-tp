from flask import Flask, render_template, request, redirect, url_for, flash
import re
import random
from db.config import get_db_connection
from utils.functions import create_user, logIn, getColumns, albumAndArtist, getLastRegister, create_artist

app = Flask(__name__)
app.secret_key = 'mysecretkey'

@app.route("/")
def main():
    return render_template('signin.html')

@app.route("/signup", methods = ['POST'])
def newUser():
    cur, conn  = get_db_connection()
    try:
        with conn:
            username = request.form['username']
            fullname = request.form['fullname']
            password = request.form['password']


            if len(username) < 4:
                 raise Exception("El nombre de usuario debe tener una longitud mayor a 4 caracteres")
            if not re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
                 raise Exception("La contraseña no cumple los requisitos")
            
            if username and fullname and password:
                user = username, fullname, password, 0

                create_user(conn, cur, user)

                return redirect('/users')
            else:
                raise Exception("Debes ingresar todos los campos")
    except Exception:
        return {
            'error': True,
            'message': f'Algo salió mal'
        }

@app.route("/login", methods = ['POST'])
def login():
    cur, conn  = get_db_connection()
    with conn:
        username = request.form['username']
        password = request.form['password']

        user = logIn(conn, cur, username, password)
        isLogged = True if user else False

        if isLogged:
            return redirect('/search')
        else:
            return render_template('signin.html')

@app.route("/users")
def getUsers():
    cur, conn  = get_db_connection()
    users = cur.execute('SELECT * FROM Users')
    return render_template('users.html', users=users)

@app.route("/artist", methods=['GET', 'POST'])
def getArtist():
    cur, conn  = get_db_connection()
    lastId = getLastRegister(conn, cur, 'Artist', 'ArtistId')[0]

    if request.method == 'GET':
        cur.execute('SELECT * FROM Artist')
        artists = cur.fetchall()

        return render_template('artists.html', artists=artists)
  
    elif request.method == 'POST':
        name = request.form['artist-name']
        artist = lastId + 1, name

        create_artist(conn, cur, artist)
        flash(f'Artist {name} added succesfully')
        return redirect(url_for('getArtist'))

@app.route("/edit/artist/<string:id>")
def editArtist(id):
    cur, conn  = get_db_connection()
    cur.execute(f'SELECT * FROM Artist WHERE ArtistId = {id}')
    artist = cur.fetchone()

    return render_template('edit-artist.html', artist=artist)

@app.route("/update/artist/<string:id>", methods=['POST'])
def updateArtist(id):
    if request.method == 'POST':
        cur, conn  = get_db_connection()
        newName = request.form['new-name']
        data = (newName, id)
        query = (f'''
            Update Artist 
            set Name = ? 
            WHERE ArtistId = ?
            ''')
        cur.execute(query, data)
        conn.commit()
        flash(f'Artist {newName} updated successfully')
        return redirect(url_for('getArtist'))


@app.route("/delete/artist/<string:id>")
def deleteArtist(id):
    cur, conn  = get_db_connection()
    cur.execute(f'DELETE FROM Artist WHERE ArtistId = {id}')
    conn.commit()
    flash(f'Artist with id {id} removed succesfully')
    return redirect(url_for('getArtist'))



@app.route("/search", methods=['GET', 'POST'])
def searchImages():
    cur, conn  = get_db_connection()
    album = albumAndArtist(conn, cur)
    
    myList = []

    for artist in album:
        data = ('id', 'album', 'artist', 'track')
        if len(artist) == len(data):
            res = {data[i] : artist[i] for i, _ in enumerate(artist)}
            myList.append(res)

    filteredData = []

    if request.method == 'POST':
        filter = request.form['filtering']
        for album in myList:
            filter = filter.upper()
            if album['album'].upper().startswith(filter) or album['artist'].upper().startswith(filter) or album['track'].upper().startswith(filter):

                filteredData.append(album)    


    return render_template('finder.html', myList=myList, filteredData=filteredData)

if __name__ == '__main__':
    app.run(debug=True)