import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash
#database="test",
cnx=mysql.connector.connect(host="localhost", user="root", port="3306",database="test", \
                            password="0bcfd12dead37a0c8e69839e2d9d2e7057af194a07590932077030ebe5eb0650")

cursor = cnx.cursor()

#cursor.execute("CREATE TABLE user_test (id INT AUTO_INCREMENT PRIMARY KEY, user_id VARCHAR(16), user_pass VARCHAR(255))")


sql = "select user_pass as 'user_pass' from user_test where user_id='appearhuman'"
cursor.execute(sql)
for i in cursor.fetchall():
    print(i)

cursor.close()
cnx.close()

import cv2

# VideoCapture オブジェクトを取得します
capture = cv2.VideoCapture(0)

while(True):
    ret, frame = capture.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()