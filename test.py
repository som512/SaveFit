from flask import Flask, render_template, request, jsonify, session, url_for, redirect, Response, flash,flash
from flask_mail import Mail, Messagre
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector
from datetime import timedelta
import cv2 as cv
from win32com import client
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sqlserver_pass = "0bcfd12dead37a0c8e69839e2d9d2e7057af194a07590932077030ebe5eb0650"

cnx=mysql.connector.connect(host="localhost", user="root", port="3306",database="test", \
                            password=sqlserver_pass)
cursor = cnx.cursor()

cursor.execute("CREATE TABLE user_table (\
               id INT AUTO_INCREMENT PRIMARY KEY, \
               username VARCHAR(255), \
               email VARCHAR(255), \
               password VARCHAR(255)\
               )")
#SQL処理
'''
sql = "select %s from user_test where user_id=%s"
cursor.execute(sql, (user_pass, user_id))
result = cursor.fetchall()[0][0]
'''




cursor.close()
cnx.close()