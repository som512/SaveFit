import smtplib, ssl
from email.mime.text import MIMEText


def send_message(subject, mail_to, body):
    my_account = 'savefit@outlook.jp'
    my_password = 'xNyScr~~L!H3'

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

if __name__ == '__main__':
    send_message("件名", "daisannsuu@yahoo.co.jp", "テストテスト")
