from flask import Flask, render_template, request, redirect, url_for, session
import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.debug = True

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/signin', methods=['GET', 'POST'])
# verification endpoint
def signin():
    if request.method == 'POST':
        session['username'] = request.form.get('username')
        session['password'] = request.form.get('password')
        username = session['username']
        password = session['password']
        print("username=", username, "password=", password)
        if (not username or not password):
            return redirect(url_for('error', message= 'Please enter username or password'))
        if username == 'test' and password == 'test':
            session['signed_in'] = True
            return redirect(url_for('success'))
        else:
            return redirect(url_for('error', message='帳號或密碼錯誤'))
    
    return redirect('/')

@app.route('/signout')
def signout():
    session['signed_in'] = False
    return redirect(url_for('home'))


@app.route('/member')
def success():
    if session['signed_in']:
        return f"<h1>Welcome! {session['username']}</h1><h2>Signin Successful!</h2><a href='/signout'>Sign Out</a>"
    else: return redirect(url_for('home'))

@app.route('/error')
def error():
    message = request.args.get('message', 'An error occurred')
    return f"<h1>Error: {message}</h1><a href='/'>Home</a>"

@app.route('/square/<number>')
def square_number(number):
    if (not number.isnumeric() or int(number) <= 0):
        return redirect(url_for("home"))
    else: squared_value = int(number) ** 2
    return render_template('squared.html', number=number, squared_value=squared_value)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)
