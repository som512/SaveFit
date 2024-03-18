from flask import Flask, render_template, request, jsonify, session, url_for, redirect, Response, flash,flash
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector
from datetime import timedelta
import cv2 as cv
from win32com import client
import os
from time import time
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sqlserver_pass = "0bcfd12dead37a0c8e69839e2d9d2e7057af194a07590932077030ebe5eb0650"



cnx=mysql.connector.connect(host="localhost", user="root", port="3306",database="test", \
                            password=sqlserver_pass)

cursor = cnx.cursor()

sql = ("DROP TABLE user_info")
cursor.execute(sql)
cursor.execute("CREATE TABLE user_info (\
               id INT AUTO_INCREMENT PRIMARY KEY, \
               mail_certification BOOL DEFAULT False,\
               username VARCHAR(16),\
               email VARCHAR(50),\
               password VARCHAR(64),\
               self_introduction VARCHAR(160),\
               icon_path VARCHAR(59) DEFAULT '/pic/default.png'\
               )")

sql = ("DROP TABLE temporary_registration_list")
cursor.execute(sql)
cursor.execute("CREATE TABLE temporary_registration_list (\
               id INT PRIMARY KEY,\
               email VARCHAR(50),\
               time_limit VARCHAR(30),\
               secret_key VARCHAR(24),\
               encrypt_text VARCHAR(64),\
               padding_text VARCHAR(24)\
               )")

#SQL処理
'''
sql = "select %s from user_test where user_id=%s"
cursor.execute(sql, (user_pass, user_id))
result = cursor.fetchall()[0][0]


sql = "select (password, mail_certification) from user_info where email=%s"
cursor.execute(sql, ("daisannsuu@yahoo.co.jp",))
print(cursor.fetchall())
'''




cursor.close()
cnx.close()