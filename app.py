from flask import Flask, render_template, request, jsonify, session, url_for, redirect, Response, flash,flash
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector
from datetime import timedelta
import cv2 as cv
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

sqlserver_pass = "0bcfd12dead37a0c8e69839e2d9d2e7057af194a07590932077030ebe5eb0650"
'''
cnx=mysql.connector.connect(host="localhost", user="root", port="3306",database="test", \
                            password=sqlserver_pass)
cursor = cnx.cursor()
#SQL処理

cursor.close()
cnx.close()
'''

camera = cv.VideoCapture(0)
def gen_frames():
   while True:
       success, frame = camera.read()
       if not success:
           break
       else:
           #フレームデータをjpgに圧縮
           ret, buffer = cv.imencode('.jpg',frame)
           # bytesデータ化
           frame = buffer.tobytes()
           yield (b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
app = Flask(__name__)
app.secret_key = '442cb7c65e15d1d4742dc5acce2ad073008310e4bdb67e7453851acefa90f708'
app.permanent_session_lifetime = timedelta(days=1)#days=1
@app.route('/')
def index():
    if "user_id" in session:
        user_id = session["user_id"]
        return render_template('index.html', user_id=user_id)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_pass = generate_password_hash(request.form['user_pass'])
        cnx=mysql.connector.connect(host="localhost", user="root", port="3306",database="test", \
                            password=sqlserver_pass)
        cursor = cnx.cursor()
        #SQL処理
        sql = "select %s from user_test where user_id=%s"
        cursor.execute(sql, (user_pass, user_id))
        result = cursor.fetchall()[0][0]
        #IDとパスワードが一致している時
        if (len(result)!=0)&(user_pass==result):
            session.permanent = True
            session["user_id"] = user_id
            cursor.close()
            cnx.close()
            return redirect(url_for("index"))
        #IDとパスワードが一致していない時
        else:
            cursor.close()
            cnx.close()
            return render_template('login.html', warning="pass_different")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_pass = generate_password_hash(request.form['user_pass'])
        
        cnx=mysql.connector.connect(host="localhost", user="root", port="3306",database="test", \
                            password=sqlserver_pass)
        cursor = cnx.cursor()
        #SQL処理
        sql = "select * from user_test where user_id=%s"
        cursor.execute(sql, [user_id])
        result = cursor.fetchall()
        cursor.close()
        cnx.close()
        #idが重複していないかチェック
        if result:#重複あり
            return render_template('register.html', warning="id")
        else:#重複なし
            cnx=mysql.connector.connect(host="localhost", user="root", port="3306",database="test", \
                                        password=sqlserver_pass)
            cursor = cnx.cursor()
            #SQL処理
            sql = "INSERT INTO user_test (user_id, user_pass) VALUE (%s, %s)"
            cursor.execute(sql, (user_id, user_pass))
            cnx.commit()
            cursor.close()
            cnx.close()
            return redirect(url_for("index"))
    return render_template('register.html')

@app.route("/logout") #ログアウトする
def logout():
  session.pop("user_id", None) #削除
  return redirect(url_for("index"))

@app.route("/live")
def live():
    if "user_id" in session:
        user_id = session["user_id"]
        return render_template('live.html', user_id=user_id)
    return redirect(url_for("login"))



@app.route("/get_ip", methods=["GET"])
def get_ip():
    return str(request.remote_addr)

@app.route("/sql", methods=["GET"])
def sql():
    id_arr = []
    user_id_arr = []
    cnx=mysql.connector.connect(host="localhost", user="root", port="3306",database="test", \
                                password=sqlserver_pass)
    cursor = cnx.cursor()
    #SQL処理
    sql = "select * from user_test"
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in result:
        id_arr.append(i[0])
        user_id_arr.append(i[1])
    cursor.close()
    cnx.close()
    return render_template('sql.html', id_arr=id_arr, user_id_arr=user_id_arr)

if __name__ == '__main__' :
    app.run(host='0.0.0.0', port=8000, threaded=True, debug=False)