from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import errorcode
import glob

# データベース接続
host = 'localhost' # データベースのホスト名又はIPアドレス
username = 'root'  # MySQLのユーザ名
passwd   = 'Mimu1997'    # MySQLのパスワード
dbname   = 'my_database'    # データベース名

# 管理画面
app = Flask(__name__)
@app.route("/manegiment", methods=["GET"])
def manegiment():
    order_name = request.form.get("order_name", "")
    print(order_name)
    order_price = request.form.get("order_price", "")
    print(order_price)
    order_number = request.form.get("order_number", "")
    print(order_number)

    order_manegiment = []
    mes = ""
    
    try:
        # データベースの情報を渡し、接続
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        
        # クエリ実行
        cursor = cnx.cursor()
        query = 'SELECT drink_data.drink_photo, drink_data.drink_name, drink_data.price, manegiment_drink_number.drink_number, drink_data.publicprivate FROM drink_data JOIN manegiment_drink_number ON drink_data.drink_id = manegiment_drink_number.drink_id' #実行するクエリ
        cursor.execute(query)

        # 実行したクエリ結果の取得
        for (drink_photo, drink_name, price, drink_number, publicprivate) in cursor:
            item = {"drink_photo":drink_photo, "drink_name":drink_name, "price":price, "drink_number":drink_number, "publicprivate":publicprivate}
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

# 購入者画面
@app.route("/", methods=["GET","POST"])
def buy():
    # 初期値
    add_price="" #投入金額
    buy_order="" #購入商品
    buy_drink="" #購入ボタン選択
    change = "" #お釣り
    mes = "" #購入確認メッセージ

    # 購入ボタン選択、投入金額・購入商品情報の取得
    if "add_price" in request.form.keys() and "buy_order" in request.form.keys():
        add_price = request.form.get("add_price", "")
        buy_order = request.form.get("buy_order", "")
    
    #print("buy_drink:{}".format(buy_drink))
    #print("add_price:{}".format(add_price))
    #print("buy_order:{}".format(buy_order))

    try:
        # データベースの情報を渡し、接続
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)

        # クエリ実行
        cursor = cnx.cursor()
        query = 'SELECT drink_data.drink_id, drink_data.drink_photo, drink_data.drink_name, drink_data.price, manegiment_drink_number.drink_number FROM drink_data JOIN manegiment_drink_number ON drink_data.drink_id = manegiment_drink_number.drink_id' #実行するクエリ
        cursor.execute(query)

        order_drink_data = []
        buy = []

        # 実行したクエリ結果の取得
        for (drink_id, drink_photo, drink_name, price, drink_number) in cursor:
            item = {"drink_id":drink_id,"drink_photo":drink_photo, "drink_name":drink_name, "price":price, "drink_number":drink_number}
            order_drink_data.append(item)
            #print(item["drink_id"])

            # どの商品を選択したのか取得
            # 無選択の場合は、0を取得(intによるエラーを避けるため。)
            if buy_order == "":
                buy_order = '0'
            if item["drink_id"] == int(buy_order):
                buy = item
        
        # 購入金額計算
        if add_price == "":
            add_price = '0'

        # 投入金額が数字であるかの確認
        if str.isnumeric(add_price) == True:
            #  購入ボタンが押された場合
            if "buy_drink" in request.form.keys():
                add_price = int(add_price)

                # 投入金額の確認
                #   投入金額が商品金額よりも多い（お釣り計算）
                if add_price >= buy["price"]:
                    change = add_price - buy["price"]
                    """
                    # 在庫変更
                    stock_query = f'UPDATE drink_data SET drink_number = (buy["buy_number"]-1) WHERE drink_id = "buy["id"]"'
                    cursor.execute(stock_query)
                    cnx.commit()
                    """
                #   投入金額が商品金額より少ない
                else:
                    mes = "投入金額が足りていません。"

        # 投入金額が数値以外の場合
        elif str.isnumeric(add_price) == False:
            mes = "金額を入力してください。" 

        params = {
            "order_drink_data" : order_drink_data,
            "add_price":add_price,
            "buy_order":buy_order,
            "mes" : mes,
            "change" : change
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

    return render_template("Vendingmachine_buy.html", **params)

@app.route("/buy_result", methods=["GET","POST"])
def buy_result():
    #print("add_price:{}".format(add_price))
    #print("buy_order:{}".format(buy_order))
    
    return render_template("Vendingmachine_result.html")