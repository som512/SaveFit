# mysql-connector-python　使い方
## 接続
## MySQLに接続
```
conn = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password"
)
```
### カーソル取得
データベース取得(conn)からカーソルを取得する。
カーソルとは、クエリ実行のための仮想ポインタの事。
```
cursor = conn.cursor()
```

### 接続を閉じる
```
cursor.close()
conn.close()
```
<br><br><br>
## データベース
### データベース作成
```
cursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase")
```
<br><br><br>
## テーブル
### テーブル作成
```
cursor.execute("CREATE TABLE test1 (id INT AUTO_INCREMENT PRIMARY KEY, NAME VARCHAR(255))")
```

### テーブル追加
```
sql = "INSERT INTO test2 (user_id, user_pass) VALUE (%s, %s)"
cursor.execute(sql, ("appearhuman", "sannsuu12"))
cnx.commit()
```

### テーブル表示
```
cursor.execute("SHOW TABLES")
print(cursor.fetchall())
```

### テーブル削除
```
sql = ("DROP TABLE テーブル名")
cursor.execute(sql)
```
<br><br><br>
## データ
### データ取得
```
sql = "select * from test1"
cursor.execute(sql)
result = cursor.fetchall()
```

### データ追加
```
sql = "INSERT INTO user_info (username, email, passwrod) VALUE (%s, %s, %s)"
cursor.execute(sql, (user_name, user_mail, user_pass))
cnx.commit()
```

### データ削除
```
sql = ('DELETE FROM student WHERE student_id = %s')
cursor.execute(sql, (2,))
cnx.commit()
```

### データ更新
```
sql = ('UPDATE テーブル名 SET 更新する列名 = %s WHERE username = %s')
cursor.execute(sql, ('', ''))
cnx.commit()
```
<br><br><br>
## メモ
### テーブルメモ
`user_info`
```
cursor.execute("CREATE TABLE user_info (\
               id INT AUTO_INCREMENT PRIMARY KEY, \
               mail_certification BOOL DEFAULT False,\
               username VARCHAR(16),\
               email VARCHAR(50),\
               password VARCHAR(64),\
               self_introduction VARCHAR(160),\
               icon_path VARCHAR(59) DEFAULT 'static/pic/default.png'\
               )")
```

`temporary_registration_list`
```
cursor.execute("CREATE TABLE temporary_registration_list (\
               id INT PRIMARY KEY,\
               email VARCHAR(50),\
               time_limit VARCHAR(30),\
               secret_key VARCHAR(24),\
               encrypt_text VARCHAR(64),\
               padding_text VARCHAR(24)\
               )")
```

`post`
```
cursor.execute("CREATE TABLE temporary_registration_list (\
               id INT PRIMARY KEY,\
               time DATETIME,\
               post_data TEXT,\


               )")
```