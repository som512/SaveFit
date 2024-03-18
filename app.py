from flask import Flask, render_template, request, jsonify, session, url_for, redirect, Response, flash,flash
from werkzeug.security import check_password_hash, generate_password_hash
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import mysql.connector
from datetime import timedelta
import cv2 as cv
import smtplib, ssl
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import json
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
with open('../password.json') as f:
    password_dict = json.load(f)
sqlserver_pass = password_dict['sql_server_pass']
'''
#SQL処理
cnx=mysql.connector.connect(host="localhost", user="root", port="3306",database="test", \
                            password=sqlserver_pass)
cursor = cnx.cursor()

cursor.close()
cnx.close()
'''

'''
Outlookメール送信
'''
def send_message(subject, mail_to, body):
    my_account = password_dict['savefit_outlook_email']
    my_password = password_dict['savefit_outlook_password']

    msg = MIMEText(body, 'plain') #メッセージ本文
    msg['Subject'] = subject #件名
    msg['To'] = mail_to #宛先
    msg['From'] = my_account #送信元

    server = smtplib.SMTP('smtp.office365.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(my_account, my_password)
    server.send_message(msg)

'''
共通鍵作成、暗号化・復号化
'''    
# 鍵の作成
def create_key():
    key = get_random_bytes(AES.block_size)
    return b64encode(key).decode('utf-8')

# 暗号化する
def encrypt(key, data):
    key = b64decode(key)
    data = bytes(data, 'utf-8')
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    return ct, iv

# 復号化する
def decrypt(key, iv, ct):
    key = b64decode(key)
    iv = b64decode(iv)
    ct = b64decode(ct)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode('utf-8')
app = Flask(__name__)
app.secret_key = password_dict['flask_app_secret_key']
app.permanent_session_lifetime = timedelta(days=1)#days=1

@app.route('/')
def index():
    print(app.secret_key)
    if "user_mail" in session:
        user_mail = session["user_mail"]
        #SQL処理
        cnx=mysql.connector.connect(host="localhost", user="root", port="3306",database="test", \
                            password=sqlserver_pass)
        cursor = cnx.cursor()
        sql = "select username from user_info where email=%s"
        cursor.execute(sql, (user_mail,))
        result = cursor.fetchall()
        user_name = result[0][0]
        cursor.close()
        cnx.close()

        return render_template('index.html', user_name=user_name)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_user_mail = request.form['user_mail']
        form_user_pass = request.form['user_pass']
        #SQL処理
        cnx=mysql.connector.connect(host="localhost", user="root", port="3306",database="test", \
                            password=sqlserver_pass)
        cursor = cnx.cursor()
        sql = "select (password, mail_certification) from user_info where email=%s"
        cursor.execute(sql, (form_user_mail,))
        result = cursor.fetchall()
        user_pass = result[0][0]
        mail_certification = result[0][1]
        cursor.close()
        cnx.close()

        if (len(result)==0):
            return render_template('login.html', warning="again")
        elif(user_pass!=form_user_pass):
            return render_template('login.html', warning="pass_different")
        elif(mail_certification!=True):
            return render_template('login.html', warning="certification_different")
        else:
            session.permanent = True
            session["user_mail"] = form_user_mail
            return redirect(url_for("index"))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_mail = request.form['user_mail']
        user_pass = request.form['user_pass']

        #SQL処理
        cnx=mysql.connector.connect(host="localhost", user="root", port="3306",database="test", \
                            password=sqlserver_pass)
        cursor = cnx.cursor()
        #メール重複　確認
        sql = "select * from user_info where email=%s"
        cursor.execute(sql, [user_mail])
        mail_check_result = cursor.fetchall()
        cursor.close()
        cnx.close()

        if len(mail_check_result)!=0:#メール重複あり
            return render_template('register.html', warning="e-mail")
        else:

            #SQL処理
            cnx=mysql.connector.connect(host="localhost", user="root", port="3306",database="test", \
                                        password=sqlserver_pass)
            cursor = cnx.cursor()
            sql = "select * from user_info where email=%s"
            cursor.execute(sql, (user_name, user_mail, user_pass))
            cnx.commit()
            cursor.close()
            cnx.close()

            #暗号化
            key = create_key()
            deadline_time = str(datetime.now() + timedelta(minutes=30))
            ct, iv = encrypt(key, deadline_time)

            #SQL処理
            cnx=mysql.connector.connect(host="localhost", user="root", port="3306",database="test", \
                                        password=sqlserver_pass)
            cursor = cnx.cursor()
            sql = "INSERT INTO temporary_registration_list (username, email, passwrod) VALUE (%s, %s, %s)"
            cursor.execute(sql, (user_name, user_mail, user_pass))
            cnx.commit()
            cursor.close()
            cnx.close()

            return render_template('register_done.html')
    return render_template('register.html')
URL = 'localhost:8000/register_certification?encrypt_text='+str()
@app.route('/register_certification', methods=["GET"])
def register_done():
    encrypt_deadline = request.args.get("encrypt_text")
    #SQL処理
    cnx=mysql.connector.connect(host="localhost", user="root", port="3306",database="test", \
                        password=sqlserver_pass)
    cursor = cnx.cursor()
    #メール重複　確認
    sql = "select * from temporary_registration_list where encrypt_text=%s"
    cursor.execute(sql, [encrypt_deadline])
    temporary_registration_result = cursor.fetchall()
    cursor.close()
    cnx.close()
    if len(temporary_registration_result)!=0:
        id = temporary_registration_result[0][0]
        decrypt_deadline = decrypt(key=temporary_registration_result[0][3], iv=temporary_registration_result[0][5], \
                                ct=temporary_registration_result[0][4])
        deadline_time = temporary_registration_result[0][2]
        decrypt_deadline = datetime.strptime(decrypt_deadline, "%Y-%m-%d %H:%M:%S.%f")
        deadline_time = datetime.strptime(deadline_time, "%Y-%m-%d %H:%M:%S.%f")

        #SQL処理 
        cnx=mysql.connector.connect(host="localhost", user="root", port="3306",database="test", \
                            password=sqlserver_pass)
        cursor = cnx.cursor()
        sql = ('DELETE FROM temporary_registration_list WHERE encrypt_text=%s')
        cursor.execute(sql, [encrypt_deadline])
        cursor.close()
        cnx.close()

        if decrypt_deadline <= deadline_time:

            #SQL処理 
            cnx=mysql.connector.connect(host="localhost", user="root", port="3306",database="test", \
                                password=sqlserver_pass)
            cursor = cnx.cursor()
            sql = ('UPDATE user_info SET mail_certification = %s WHERE id = %s')
            cursor.execute(sql, (True, id))
            cursor.close()
            cnx.close()

            return render_template('register_complete.html')
        else:
            return render_template('register_expired.html')
    else:
        return render_template('register_expired.html')

@app.route("/logout") #ログアウトする
def logout():
  session.pop("user_mail", None) #削除
  return redirect(url_for("index"))

@app.route("/mypage")
def mypage():
  if "user_mail" in session:
        user_mail = session["user_mail"]
        cnx=mysql.connector.connect(host="localhost", user="root", port="3306",database="test", \
                            password=sqlserver_pass)
        cursor = cnx.cursor()
        #SQL処理
        sql = "select username from user_info where email=%s"
        cursor.execute(sql, (user_mail,))
        user_name = cursor.fetchall()
        cursor.close()
        cnx.close()
        return render_template('live.html', user_name=user_name)

@app.route("/live")
def live():
    if "user_mail" in session:
        user_mail = session["user_mail"]
        cnx=mysql.connector.connect(host="localhost", user="root", port="3306",database="test", \
                            password=sqlserver_pass)
        cursor = cnx.cursor()
        #SQL処理
        sql = "select username from user_info where email=%s"
        cursor.execute(sql, (user_mail,))
        user_name = cursor.fetchall()
        cursor.close()
        cnx.close()
        return render_template('register.html', user_name=user_name)
    return redirect(url_for("login"))



@app.route("/get_ip", methods=["GET"])
def get_ip():
    return str(request.remote_addr)

@app.route("/sql", methods=["GET"])
def sql():
    id_arr = []
    user_name_arr = []
    user_mail_arr = []
    
    cnx=mysql.connector.connect(host="localhost", user="root", port="3306",database="test", \
                                password=sqlserver_pass)
    cursor = cnx.cursor()
    #SQL処理
    sql = "select (id, username) from user_info"
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in result:
        id_arr.append(i[0])
        user_name_arr.append(i[1])

    cursor.close()
    cnx.close()
    return render_template('sql.html', id_arr=id_arr, user_name_arr=user_name_arr)

if __name__ == '__main__' :
    app.run(host='0.0.0.0', port=8000, threaded=True, debug=False)