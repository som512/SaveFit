from flask import Flask, render_template, request, jsonify, session, url_for, redirect, Response, flash,flash
from werkzeug.security import check_password_hash, generate_password_hash
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import mysql.connector
from datetime import timedelta, datetime
import cv2 as cv
import smtplib, ssl
from email.mime.text import MIMEText
import json
import os


os.chdir(os.path.dirname(os.path.abspath(__file__)))

a = "6DIAEAWvLi4wv/uZWd/XSM9nxiHR8HAFFLFq+d/BnS0="
print(a)
print(a.replace("+", "%2B"))