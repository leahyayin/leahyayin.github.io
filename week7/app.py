from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from dotenv import load_dotenv
from db_conn import *
load_dotenv()  # take environment variables from .env.

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# connect to MySQL database
connection = create_connection('website_w6')   

@app.route('/', methods=['GET'])
def home():
    hint = request.args.get('hint', None)
    return render_template('home.html', hint=hint)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        login_res = verify_member(connection, username, password)    
        if login_res:
            print("log in OK")
            session['signed_in'] = True
            session['username'] = username
            session['password'] = password
            session['id'] = login_res[0]
            session['name'] = login_res[1]
            return redirect(url_for('success'))
        
        print("log in Failed")
        return redirect(url_for('error', message='帳號或密碼錯誤')) 

    return redirect('/')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('name')
        password = request.form.get('password')
        register = verify_member(connection, username)
        if register:
            print("帳號已經被註冊")
            return redirect(url_for('error', message='帳號已經被註冊'))
        else:
            print("register username existed?", register)                
            register_member(connection,name, username, password)
            return redirect(url_for('home', hint = "註冊成功，請登入系統"))

    return redirect('/')

@app.route('/signout')
def signout():
    session['signed_in'] = False # session.clear()
    return redirect('/')

@app.route('/member', methods = ['GET'])
def success():
    if session['signed_in']:
        # get all messages
        messages = get_messages(connection)
        return render_template('member.html',
                                name = session['name'], messages=messages) 

    return redirect(url_for('home')) 

@app.route('/api/member', methods=['GET'])
def api_member():
    if (session['signed_in']):
        username = request.args.get("username", None).strip()
        print("search name of user", username)
        if (username):
            data = get_member_info(connection, username)
            if data: return jsonify({'data': data})
    return jsonify({'data': None})

@app.route('/api/member/update_name', methods=['GET', 'PATCH'])
def api_update_name():
    if (request.method == 'PATCH' and session['signed_in']):
        new_name = request.json.get("name", None)
        if (new_name):
            if update_name(connection, new_name, session['id']):
                session['name'] = new_name
                return jsonify({"ok": True})
    return jsonify({"error":True})

@app.route('/createMessage', methods = ['GET', 'POST'])
def createMsg():
    # add messages
    if session["signed_in"]:
        content = request.form.get('content')
        if content:
            add_message(connection, session['id'], content)      
    return redirect('/member')

@app.route('/deleteMessage', methods = ['GET', 'POST'])
def delMsg():
    # delete message
    if session["signed_in"]:
        message_id = request.form.get('delBtn')
        if message_id:
            delete_message(connection, message_id)
    
    return redirect('/member')

@app.route('/error')
def error():
    message = request.args.get('message', 'An error occurred')
    return f"<h1>Error: {message}</h1><a href='/'>Home</a>"

@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=3000)




