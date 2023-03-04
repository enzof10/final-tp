from flask import Flask, render_template, request, redirect, url_for, flash, session
import re
import random
import requests
app = Flask(__name__)
app.secret_key = 'mysecretkey'
@app.route("/", methods=['GET', 'POST'])
def main():
    return redirect('http://localhost:5000/sign-in', code=302)

@app.route("/sign-in", methods=['POST', "GET"])
def sign_in():
    error = ''
    if(request.method == "POST"):
        userName = request.form['username']
        if userName:
            password = request.form['password']
            auth_data = {'username': userName, 'password': password}
            resp = requests.post('http://localhost:8000/sign-in', data=auth_data)
            resp = resp.json() 
            print("auth")
            print(resp)
            error = resp["isValid"] 
            if(resp["isValid"]):
                session["user"] = resp["user"]["Username"]
                return redirect('artists',code=302)
    return render_template('signin.html', errorLogin = error)



@app.route("/sign-up", methods=['POST'])
def sign_up():
    userName = request.form['username']
    fullname = request.form['fullname']
    password = request.form['password']
    auth_data = {'username': userName, 'password': password, 'fullname' : fullname}
    resp = requests.post('http://localhost:8000/sign-up', data=auth_data)
    resp = resp.json() 
    print("resp sign-up")
    print(resp)
    error = resp["message"]
    if(not resp["error"]):
        session["user"] = resp["user"]["name"]
        return redirect('artists.html', code=302)
    return render_template('signin.html', errorLogin = error)


@app.route("/artists", methods=['GET'])
def artists():
    artistName = request.args.get('search')
    if(artistName != "" and artistName):
        artists = requests.get('http://localhost:8000/artists' + "?search=" + artistName)
    else:
        artists = requests.get('http://localhost:8000/artists')
    artists = artists.json()
    return render_template('artists.html', artists = artists)

@app.route("/artists/<name>/edit", methods=['GET'])
def edit_artist(name):
    print(name)
    artist = requests.get('http://localhost:8000/artists' + "?search=" + name)
    artist = artist.json()
    print(artist[0])
    return render_template('edit-artist.html', artist = artist[0])


if __name__ == '__main__':
    app.run(debug=True)