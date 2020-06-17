from flask import Flask, render_template, request

# データベース接続
host = 'localhost' # データベースのホスト名又はIPアドレス
username = 'root'  # MySQLのユーザ名
passwd   = 'Mimu1997'    # MySQLのパスワード
dbname   = 'my_database'    # データベース名

app = Flask(__name__)
@app.route("/manegiment")
def manegiment():
    return render_template("Manegiment_Vendingmachine.html")