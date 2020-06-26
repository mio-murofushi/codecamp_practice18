from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import errorcode
import glob
import re
import os
#from PIL import Image
from werkzeug.utils import secure_filename


# データベース接続
host = 'localhost' # データベースのホスト名又はIPアドレス
username = 'root'  # MySQLのユーザ名
passwd   = 'Mimu1997'    # MySQLのパスワード
dbname   = 'my_database'    # データベース名


app = Flask(__name__)

# フォルダ
UPLOAD_FOLDER = './static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 管理画面
@app.route("/manegiment", methods=["GET","POST"])
def manegiment():
    order_manegiment = []
    mes = ""
    add_filename = "" #追加商品のパス指定
    file_name = ""
    filename=""
    
    # 商品追加のボタンをおした時、新商品情報を取得
    if "add" in request.form.keys():
        order_name = request.form.get("order_name", "")
        order_price = request.form.get("order_price", "")
        order_number = request.form.get("order_number", "")
        #file_name = request.form.get("file_name", "")
        file_name = request.files["file_name"]
        """
        # ファイル情報取得
        if "file_name" in request.files:
            file_name = request.files["file_name"]
        else:
            file_name = ""
        """

        publicprivate = request.form.get("publicprivate", "")
    
    try:
        # データベースの情報を渡し、接続
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        
        # 新商品情報を取得した場合
        if "add" in request.form.keys():
            # 入力欄に記入漏れがあるか、否か
            if order_name=="" or order_price=="" or order_number=="" or file_name=="":
                mes = "入力欄が不十分です。"
            else:
                # 新商品の価格、在庫が数字であるか、否か
                if str.isnumeric(order_price) == True and str.isnumeric(order_number) == True:
                    # 新商品のファイルネームがPNG,JPEGであるか、否か
                    if re.match("([^\s]+(\.(?i)(jpeg|jpg|png))$)", file_name.filename):
                        file_name.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name.filename))
                        
                        # 新商品の情報をクエリに追加
                        cursor = cnx.cursor()
                        new_order_query=F"INSERT INTO drink_data(drink_name, price, publicprivate, drink_photo) VALUES ('{order_name}', {order_price}, {publicprivate}, '{file_name.filename}')"
                        cursor.execute(new_order_query)
                        cnx.commit()
                        new_stock_query=F"INSERT INTO manegiment_drink_number(drink_number) VALUES ({order_number})"
                        cursor.execute(new_stock_query)
                        cnx.commit()

                        mes = "商品情報追加完了"
                    else:
                        mes = "ファイルの拡張子は、JPEG or PNG にしてください。"
                else:
                    mes = "価格 または 在庫数に問題があります。"

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
    buy_order="" #購入商品のdrink_id
    buy_drink="" #購入ボタン選択
    change = "" #お釣り

    mes = "" #購入確認メッセージ
    change_mes = "" #お釣りの無い時のメッセージ
    
    buy_drink_order="" #購入商品
    buy_drink_number="" #購入商品の現在庫

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
                buy_drink_order = item["drink_name"]
                buy_drink_number = buy["drink_number"]
                update_drink_number = buy["drink_number"] -1
        
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
                if add_price >= int(buy["price"]):
                    if add_price == buy["price"]:
                        change_mes = "丁度頂戴いたしました！また買ってくださいね！"
                    else:
                        change = add_price - buy["price"]
                    
                    # 在庫変更
                    stock_query = F"UPDATE manegiment_drink_number SET drink_number= {update_drink_number} WHERE drink_id = {buy['drink_id']}"
                    cursor.execute(stock_query)
                    cnx.commit()
                    

                #   投入金額が商品金額より少ない
                else:
                    mes = "投入金額が足りていません。"
                
                params = {
                "order_drink_data" : order_drink_data,
                "add_price":add_price,
                "buy_order":buy_order,
                "mes" : mes,
                "change_mes" : change_mes,
                "change" : change,
                "buy_drink_order" : buy_drink_order
                }
                return render_template("Vendingmachine_result.html", **params)

        # 投入金額が数値以外の場合
        elif str.isnumeric(add_price) == False:
            mes = "金額を入力してください。" 

        params = {
            "order_drink_data" : order_drink_data,
            "add_price":add_price,
            "buy_order":buy_order,
            "mes" : mes
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