from flask import Flask, render_template, request, redirect, url_for, session
import os
from dotenv import load_dotenv
from db_conn import *
load_dotenv()  # take environment variables from .env.

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# connect to MySQL database
connection = create_connection('website_w6')   

@app.route('/', methods=['GET', 'POST'])
def home():
    hint = request.args.get('hint', None)
    return render_template('home.html', hint=hint)

@app.route('/signin', methods=['GET', 'POST'])
# verification endpoint
def signin():
    if request.method == 'POST':
        session['username'] = request.form.get('username')
        session['password'] = request.form.get('password')
        print("username=", session['username'], "password=", session['password'])
        login_res = verify_member(connection, session['username'], session['password'])    
        if login_res:
            print("log in OK")
            session['signed_in'] = True
            session['id'] = login_res[0]
            session['name'] = login_res[1]
            return redirect(url_for('success'))
        else:
            print("log in Failed")
            return redirect(url_for('error', message='帳號或密碼錯誤')) 

    return redirect('/')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # 1. 檢查資料庫的 member 資料表中是否有重複的帳號 (username)
        register = verify_member(connection, username = request.form.get('username'))
        if register:
            # 1a. 如果有重複，不新增資料，註冊失敗，導向到【失敗⾴⾯】，並顯⽰「帳號已經被註冊」
            print("帳號已經被註冊")
            return redirect(url_for('error', message='帳號已經被註冊'))
        else:
            # 1b. 如果沒有重複，新增資料到資料庫的 member 資料表，註冊成功，導向到【網站⾸⾴】
            print("register username existed?", register)                
            register_member(connection, 
                            request.form.get('name'),  
                            request.form.get('username'), 
                            request.form.get('password'))
            return redirect(url_for('home', hint = "註冊成功，請登入系統"))

    return redirect('/')

@app.route('/signout')
def signout():
    session['signed_in'] = False
    return redirect('/')

@app.route('/member', methods = ['GET', 'POST'])
def success():
    if session['signed_in']:
        # get all messages
        messages = get_messages(connection)
        return render_template('member.html',
                                name = session['name'], messages=messages) 
    else: 
        # if not signed in then direct to home page
        return redirect(url_for('home')) 

@app.route('/createMessage', methods = ['GET', 'POST'])
def createMsg():
    # add messages
    content = request.form.get('content')
    if content:
        print("id", session['id'])
        add_message(connection, session['id'], content)      
    return redirect('/member')

@app.route('/deleteMessage', methods = ['GET', 'POST'])
def delMsg():
    # delete message
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




