# mysql-connector-python　使い方
## MySQLに接続
```
conn = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password"
)
```
## カーソル取得
データベース取得(conn)からカーソルを取得する。
カーソルとは、クエリ実行のための仮想ポインタの事。
```
cursor = conn.cursor()
```
## データベース作成
```
cursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase")
```
## データ取得
```
sql = "select * from test1"
cursor.execute(sql)
result = cursor.fetchall()
```
## データベース変更の確定
```
conn.commit()
```
## 接続を閉じる
```
cursor.close()
conn.close()
```
## テーブル作成
```
cursor.execute("CREATE TABLE test1 (id INT AUTO_INCREMENT PRIMARY KEY, NAME VARCHAR(255))")
```

## テーブル追加
```
sql = "INSERT INTO test2 (user_id, user_pass) VALUE (%s, %s)"
cursor.execute(sql, ("appearhuman", "sannsuu12"))
cnx.commit()
```