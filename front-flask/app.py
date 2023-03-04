from flask import Flask, render_template, request, redirect, url_for, flash, session
import re
import random
import requests
app = Flask(__name__)
app.secret_key = 'mysecretkey'
@app.route("/", methods=['GET', 'POST'])
def main():
    return redirect('http://localhost:5000/sign-in', code=302)

@app.route("/sign-in", methods=['POST'])
def sign_in():
    userName = request.form['username']
    error = ''
    if userName:
        password = request.form['password']
        auth_data = {'username': userName, 'password': password}
        resp = requests.post('http://localhost:8000/sign-in', data=auth_data)
        resp = resp.json() 
        print("auth")
        print(resp)
        error = resp["isValid"] 
        if(resp["isValid"]):
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
    print(resp)
    error = resp["message"]
    if(not resp["error"]):
        artists = requests.get('http://localhost:8000/artists')
        artists = artists.json()
        print(artists)
        return render_template('artists.html', artists = artists)
    return render_template('signin.html', errorLogin = error)


@app.route("/artists", methods=['GET'])
def artists():
    artistName = request.args.get('search')
    if(artistName != ""):
        artists = requests.get('http://localhost:8000/artists' + "?search=" + artistName)
    else:
        artists = requests.get('http://localhost:8000/artists')
    artists = artists.json()
    print(artists)
    return render_template('artists.html', artists = artists)


if __name__ == '__main__':
    app.run(debug=True)