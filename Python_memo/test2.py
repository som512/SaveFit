import json
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
'''
a = {"flask_app_secret_key": "442cb7c65e15d1d4742dc5acce2ad073008310e4bdb67e7453851acefa90f708",
	"savefit_outlook_email": "savefit@outlook.jp",
	"savefit_outlook_password": "xNyScr~~L!H3",
	"sql_server_pass": "0bcfd12dead37a0c8e69839e2d9d2e7057af194a07590932077030ebe5eb0650"}
'''
with open('../password.json') as f:
    password_dict = json.load(f)

with open('../password.json', 'w') as f:
    json.dump(a, f, indent=2)