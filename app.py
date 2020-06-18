from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import errorcode
import glob

# データベース接続
host = 'localhost' # データベースのホスト名又はIPアドレス
username = 'root'  # MySQLのユーザ名
passwd   = 'Mimu1997'    # MySQLのパスワード
dbname   = 'my_database'    # データベース名

app = Flask(__name__)
@app.route("/manegiment", methods=["GET"])
def manegiment():
    order_manegiment = []
    
    try:
        # データベースの情報を渡し、接続
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        
        # クエリ実行
        cursor = cnx.cursor()
        query = 'SELECT drink_data.drink_name, drink_data.price, manegiment_drink_number.drink_number, drink_data.publicprivate FROM drink_data JOIN manegiment_drink_number ON drink_data.drink_id = manegiment_drink_number.drink_id' #実行するクエリ
        cursor.execute(query)

        # 実行したクエリ結果の取得
        for (drink_name, price, drink_number, publicprivate) in cursor:
            item = {"drink_name":drink_name, "price":price, "drink_number":drink_number, "publicprivate":publicprivate}
            order_manegiment.append(item)
        
        params = {
            "order_manegiment" : order_manegiment
        }
        #ローカルフォルダから画像を配列にいれる
        #glob.glob("./templates/img/*")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ユーザ名かパスワードに問題があります。")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("データベースが存在しません。")
        else:
            print(err)
    else:

        # DB切断
        cnx.close()
    
    return render_template("Manegiment_Vendingmachine.html", **params)

@app.route("/", methods=["GET"])
def buy_order():
    add_price=""

    #if "add_price" in request.form():
    add_price = request.form.get("add_price", "")
    
    return render_template("Vendingmachine_buy.html")

@app.route("/buy_result", methods=["POST"])
def buy_result():
    return render_template("Vendingmachine_result.html")