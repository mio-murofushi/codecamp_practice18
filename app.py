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

# 管理者側
def add_drink_infomation(order_name, order_price, order_number, file_name, publicprivate):
    order_name = request.form.get("order_name", "")
    order_price = request.form.get("order_price", "")
    order_number = request.form.get("order_number", "")
    file_name = request.files["file_name"]
    publicprivate = request.form.get("publicprivate", "")
    return order_name, order_price, order_number, file_name, publicprivate

def change_stock_button(new_stock, change_id):
    new_stock = request.form.get("new_stock", "")
    change_id = request.form.get("change_id", "")
    return new_stock, change_id

def change_status_button(status, status_id):
    status = request.form.get("status", "")
    status_id = request.form.get("status_id", "")
    # 公開→非公開
    if status == '1':
        change_status = '0'
    # 非公開→公開
    elif status == '0':
        change_status = '1'
    return change_status, status_id

def check_infomation(order_name, order_price, order_number, file_name):
    if order_name=="" or order_price=="" or order_number=="" or file_name=="":
        return "入力欄が不十分です。", False
    # 新商品の価格、在庫が数字であるか、否か
    if not (str.isnumeric(order_price) and str.isnumeric(order_number)):
        return "価格 または 在庫数に問題があります。", False
    # 新商品のファイルネームがPNG,JPEGであるか、否か
    if not re.match("([^\s]+(\.(?i)(jpeg|jpg|png))$)", file_name.filename):
        return "ファイルの拡張子は、JPEG or PNG にしてください。", False
    return "", True

def insert_new_order(order_name, order_price, publicprivate, file_name, order_number, cnx):
    cursor = cnx.cursor()
    new_order_query=F"INSERT INTO drink_data(drink_name, price, publicprivate, drink_photo) VALUES ('{order_name}', {order_price}, {publicprivate}, '{file_name.filename}')"
    cursor.execute(new_order_query)
    cnx.commit()
    new_stock_query=F"INSERT INTO manegiment_drink_number(drink_number) VALUES ({order_number})"
    cursor.execute(new_stock_query)
    cnx.commit()
    mes = "商品情報追加完了"
    return mes

def insert_new_stock(cnx, new_stock, change_id):
    cursor = cnx.cursor()
    change_stock_query=F"UPDATE manegiment_drink_number SET drink_number='{new_stock}' WHERE drink_id = '{change_id}'"
    cursor.execute(change_stock_query)
    cnx.commit()
    mes="在庫の更新が行われました。"
    return mes

def insert_new_status(cnx, change_status, status_id):
    #if change_status == '0' or change_status == '1':
    cursor = cnx.cursor()
    change_status_query=F"UPDATE drink_data SET publicprivate='{change_status}' WHERE drink_id = '{status_id}'"
    cursor.execute(change_status_query)
    cnx.commit()
    mes = "公開非公開の情報が更新されました。"
    return mes

# ユーザー側
def check_order_infomation(add_price, buy_order):
    add_price = request.form.get("add_price", "")
    buy_order = request.form.get("buy_order", "")
    return add_price, buy_order

def check_orderdrink_infomation(mes, add_price, buy_drink_number, buy_publicprivate, buy, price):
    if add_price=="" or str.isnumeric(add_price) == False:
        return "お金を投入してね。", False
    if int(buy_drink_number) == 0:
        return "在庫がありません…申し訳ございません。", False
    if buy_publicprivate == 0:
        return "非公開商品になります。申し訳ございません…", False
    if int(add_price) < buy['price']:
        return "投入金額がたりませんっっ！", False
    return mes, True

def update_stock(cnx, update_drink_number,buy, drink_id):
    # 在庫変更
    cursor = cnx.cursor()
    stock_query = F"UPDATE manegiment_drink_number SET drink_number= {update_drink_number} WHERE drink_id = {buy['drink_id']}"
    cursor.execute(stock_query)
    cnx.commit()

def calculation_of_change(add_price, buy, price):
    # お釣り計算
    if int(add_price) == buy["price"]:
        change_mes = "丁度頂戴いたしました！また買ってくださいね！"
        change=""
    else:
        change = int(add_price) - buy["price"]
    return change_mes, change

# 管理画面
@app.route("/managiment", methods=["GET","POST"])
def managiment_main():
    order_managiment = []
    mes = ""
    add_filename = "" #追加商品のパス指定
    filename=""

    # 初期値
    order_name, order_price, order_number, file_name, publicprivate="","","","",""
    new_stock, change_id = "", ""
    status, status_id = "", ""

    # 商品追加ボタンが押された場合
    if "add" in request.form.keys():
        order_name, order_price, order_number, file_name, publicprivate = add_drink_infomation(order_name, order_price, order_number, file_name, publicprivate)

    # 在庫変更のボタンが押された場合
    if "change" in request.form.keys():
        new_stock, change_id = change_stock_button(new_stock, change_id)

    # ステータスの変更ボタンを押された場合
    if "status" in request.form.keys():
        change_status, status_id = change_status_button(status, status_id)
    
    try:
        # DBに接続
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)

        # 新商品情報を取得した場合
        if "add" in request.form.keys():
            mes, check_insert = check_infomation(order_name, order_price, order_number, file_name)
            if check_insert:
                mes = insert_new_order(order_name, order_price, publicprivate, file_name, order_number, cnx)
                file_name.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name.filename))
    
        # 在庫変更のボタンが押された場合
        if "change" in request.form.keys():
            mes = insert_new_stock(cnx, change_id, new_stock)

        # 公開非公開のボタンを押された場合
        if "status" in request.form.keys():
            mes = insert_new_status(cnx, change_status, status_id)
        
        select_from_database(cnx, order_managiment)

        params = {
            "mes":mes,
            "order_managiment" : order_managiment
        }

# 関数化可能？
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
    
    return render_template("Managiment_Vendingmachine.html", **params)

# 購入者画面
@app.route("/", methods=["GET","POST"])
def user_main():
    # 初期値
    add_price, buy_order, buy_drink, change = "", "", "", ""
    mes, change_mes = "", ""
    buy_drink_order, buy_drink_number, buy_drink_photo = "", "", ""
    order_drink_data = []
    buy = []

    # 購入ボタン選択、投入金額・購入商品情報の取得
    if "buy_order" in request.form.keys():
        add_price, buy_order = check_order_infomation(add_price, buy_order)

    try:
        # データベースの情報を渡し、接続
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)

        # クエリ実行
        cursor = cnx.cursor()
        query = 'SELECT drink_data.drink_id, drink_data.drink_photo, drink_data.drink_name, drink_data.price, manegiment_drink_number.drink_number, drink_data.publicprivate FROM drink_data JOIN manegiment_drink_number ON drink_data.drink_id = manegiment_drink_number.drink_id' #実行するクエリ
        cursor.execute(query)

        order_drink_data = []
        buy = []

        # 実行したクエリ結果の取得
        for (drink_id, drink_photo, drink_name, price, drink_number, publicprivate) in cursor:
            item = {"drink_id":drink_id,"drink_photo":drink_photo, "drink_name":drink_name, "price":price, "drink_number":drink_number, "publicprivate":publicprivate}
            order_drink_data.append(item)

            # どの商品を選択したのか取得
            # 無選択の場合は、0を取得(intによるエラーを避けるため。)
            if buy_order == "":
                buy_order = '0'
            if item["drink_id"] == int(buy_order):
                buy = item
                buy_drink_photo = item["drink_photo"]
                buy_drink_order = item["drink_name"]
                buy_drink_number = buy["drink_number"]
                buy_publicprivate = buy["publicprivate"]
                update_drink_number = buy["drink_number"] -1

        #  購入ボタンが押された場合
        if "buy_drink" in request.form.keys():
            mes, can_buy_order = check_orderdrink_infomation(mes, add_price, buy_drink_number, buy_publicprivate, buy, price) 
            if can_buy_order:
                update_stock(cnx, update_drink_number,buy, drink_id)
                change_mes, change = calculation_of_change(add_price, buy, price)
            
            params = {
            "order_drink_data" : order_drink_data,
            "buy_drink_photo" : buy_drink_photo,
            "add_price":add_price,
            "buy_order":buy_order,
            "mes" : mes,
            "change_mes" : change_mes,
            "change" : change,
            "buy_drink_order" : buy_drink_order
            }
            return render_template("Vendingmachine_result.html", **params)      

        cursor.execute(query)

        params = {
            "order_drink_data" : order_drink_data,
            "buy_drink_photo" : buy_drink_photo,
            "add_price":add_price,
            "buy_order":buy_order,
            "mes" : mes
        }

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
