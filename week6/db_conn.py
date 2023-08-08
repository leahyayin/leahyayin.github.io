import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv

load_dotenv() 

def create_connection(db):
    config = {
        'user': 'root',
        'password': os.getenv('SECRET_KEY'),
        'host': '127.0.0.1',
        'database': db,
        'raise_on_warnings': True
    }
    try:
        print(f"password: {os.getenv('SECRET_KEY')}")
        cnx = mysql.connector.connect(
            host=config['host'], user=config['user'], password=config['password'])
        print("Connected to the MySQL")
        mycursor = cnx.cursor()
        mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['database']}")
        mycursor.execute(f"USE {config['database']}")
        mycursor.execute(
            """CREATE TABLE IF NOT EXISTS member (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            follower_count INT UNSIGNED NOT NULL DEFAULT 0,
            time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP)
            """)
        mycursor.execute(
            """CREATE TABLE if not exists message (
                id bigint AUTO_INCREMENT PRIMARY KEY,
                member_id bigint NOT NULL,
                content varchar(255) NOT NULL,
                like_count int unsigned NOT NULL DEFAULT 0,
                time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT FK_memberId FOREIGN KEY (member_id) REFERENCES member(id))
            """)
        
        cnx.commit()
        print("connected to db", config['database'])
        return cnx
    
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        else:
            print("Error occur: " + err)
    # finally:
    #     mycursor.close()
    #     cnx.close()
    #     print("Connection closed.")

    return None

def verify_member(connection, username, password=None):
    cursor = connection.cursor()
    if password:
        # login
        query = "SELECT * FROM member WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
    else:
        # register   
        query = "SELECT * FROM member WHERE username = %s"
        cursor.execute(query, (username, ))
    user = cursor.fetchone()
    cursor.close()
    print("user=",user)
    return user

def register_member(connection, name, username, password):
    cursor = connection.cursor()
    query = "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, username, password))
    cursor.close()
    connection.commit()
    print(f"insert member name=  {name}")

def get_messages(connection):
    cursor = connection.cursor()
    query = "SELECT message.id, member.name, message.content"\
        " FROM message JOIN member ON message.member_id = member.id;"
    cursor.execute(query)
    messages = cursor.fetchall()

    cursor.close()
    return messages

def add_message(connection, member_id, content):
    cursor = connection.cursor()
    query = "INSERT INTO message (member_id, content) VALUES (%s, %s);"
    cursor.execute(query, (member_id, content))
    connection.commit()
    cursor.close()

def delete_message(connection, message_id):
    cursor = connection.cursor()
    query = "DELETE FROM message WHERE id = %s"
    cursor.execute(query, (message_id,))
    connection.commit()
    cursor.close()


# create_connection('testWeb1')