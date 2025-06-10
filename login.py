# app.py
 
from flask import Flask, render_template, request, redirect, session
import json
import os
import sqlite3
 
app = Flask(__name__)
 
# Set a secret key for encrypting session data
users_file = os.path.join(os.path.dirname(__file__), 'users.json')
app.secret_key = 'my_secret_key'

def verify_user(username: str, password: str) -> bool:
    users = {}
    with open(users_file, 'r') as f:
        users = json.load(f)
    return username in users and users[username] == password

def create_user(username: str, password: str) -> bool:
    users = {}
    with open(users_file, 'r') as f:
        users = json.load(f)
    if username in users:
        return False
    users[username] = password
    with open(users_file, 'w') as f:
        json.dump(users, f)
    return True

# To render a login form 
@app.route('/')
def view_form():
    return render_template('login.html')
 
# For handling get request form we can get
# the form inputs value by using args attribute.
# this values after submitting you will see in the urls.
# e.g http://127.0.0.1:5000/handle_get?username=kunal&password=1234
# this exploits our credentials so that's 
# why developers prefer POST request.
@app.route('/handle_get', methods=['GET'])
def handle_get():
    if request.method == 'GET':
        username = request.args['username']
        password = request.args['password']
        print(username, password)
        if username in users and users[username] == password:
            return '<h1>Welcome!!!</h1>'
        else:
            return '<h1>invalid credentials!</h1>'
    else:
        return render_template('login.html')

@app.route('/handle_create', methods=['POST'])
def handle_create():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        if verify_user(username, password):
            return '<h1>User already created!</h1>'
        else:
            created = create_user(username, password)
            if (created):
                return f'<h1>Created {username}!!!</h1>'
            else:
                return '<h1>User already created!</h1>'
    else:
        return render_template('login.html')

# For handling post request form we can get the form
# inputs value by using POST attribute.
# this values after submitting you will never see in the urls.
@app.route('/handle_post', methods=['POST'])
def handle_post():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        if verify_user(username, password):
            return f'<h1>Welcome {username}!!!</h1>'
        else:
            return '<h1>invalid credentials!</h1>'
    else:
        return render_template('login.html')
 
if __name__ == '__main__':
    app.run()