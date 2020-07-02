def check_params_is_empty(order_name, order_price, order_number, file_name):
    '''
    パラメータが空であるかどうかを確認する関数
​
    Returns
    ----------
    bool
    空のパラメータがあったら、True
    '''
    return order_name == "" or order_price == "" or order_number == "" or file_name == ""

def validate_item_param(order_name, order_price, order_number, file_name)]
        if check_params_is_empty(order_name, order_price, order_number, file_name):
            return "入力欄が不十分です。", False
        # 新商品の価格、在庫が数字であるか、否か
        if not (str.isnumeric(order_price) and str.isnumeric(order_number)):
            return "価格 または 在庫数に問題があります。", False
        # 新商品のファイルネームがPNG,JPEGであるか、否か
        if re.match("([^\s]+(\.(?i)(jpeg|jpg|png))$)", file_name.filename):
            return "ファイルの拡張子は、JPEG or PNG にしてください。", False
        return "", True
​
def insert(order_name, order_price, order_number, file_name):
    cursor = cnx.cursor()
    new_order_query = F"INSERT INTO drink_data(drink_name, price, publicprivate, drink_photo) VALUES ('{order_name}', {order_price}, {publicprivate}, '{file_name.filename}')"
    cursor.execute(new_order_query)
    cnx.commit()
    new_stock_query = F"INSERT INTO manegiment_drink_number(drink_number) VALUES ({order_number})"
    cursor.execute(new_stock_query)
    cnx.commit()
​
@app.route("/manegiment", methods=["GET", "POST"])
def manegiment():
    #中略
​
    # 新商品情報を取得した場合
    if "add" in request.form.keys():
        mes, can_insert = validate_item_param(order_name, order_price, order_number, file_name)
        if can_insert:
            file_name.save(os.path.join(
                app.config['UPLOAD_FOLDER'], file_name.filename))
​
            # 新商品の情報をクエリに追加
            insert(order_name, order_price, order_number, file_name)
            ​
            mes = "商品情報追加完了"

​
def validate_item_param(order_name, order_price, order_number, file_name)]
            if order_name == "" or order_price == "" or order_number == "" or file_name == "":
                mes = "入力欄が不十分です。", False
            # 新商品の価格、在庫が数字であるか、否か
            if not (str.isnumeric(order_price) and str.isnumeric(order_number)):
                return "価格 または 在庫数に問題があります。", False
            # 新商品のファイルネームがPNG,JPEGであるか、否か
            if re.match("([^\s]+(\.(?i)(jpeg|jpg|png))$)", file_name.filename):
                return "ファイルの拡張子は、JPEG or PNG にしてください。", False
            return "", True
​
    def insert(order_name, order_price, order_number, file_name):
        cursor = cnx.cursor()
        new_order_query = F"INSERT INTO drink_data(drink_name, price, publicprivate, drink_photo) VALUES ('{order_name}', {order_price}, {publicprivate}, '{file_name.filename}')"
        cursor.execute(new_order_query)
        cnx.commit()
        new_stock_query = F"INSERT INTO manegiment_drink_number(drink_number) VALUES ({order_number})"
        cursor.execute(new_stock_query)
        cnx.commit()
​
    @app.route("/manegiment", methods=["GET", "POST"])
    def manegiment():
        #中略
​
        # 新商品情報を取得した場合
        if "add" in request.form.keys():
            mes, can_insert = validate_item_param(order_name, order_price, order_number, file_name)
            if can_insert:
                file_name.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], file_name.filename))
​
                # 新商品の情報をクエリに追加
                insert(order_name, order_price, order_number, file_name)
​
                mes = "商品情報追加完了"
    ```
    のように、処理の単位で関数に分離しましょう。  
    場合によっては、関数の中でさらに小さい関数に分離したほうが良い場合もあります。
​
  - booleanの変数に `if some_bool == True:` や `some_bool == False:` と書く必要はないです。  
    `if some_bool:` や `if not some_bool:` で十分です。
​
  - 追加、在庫数変更、公開ステータスの変更などは、それぞれ別のURLに対してリクエストを遅れるようにするといいですね。  
    その際に、共通の処理（今回だと画面の表示）の扱いに困るかと思いますが、リダイレクトを使って解消しましょう。  
    画面表示用のURLに[リダイレクト](https://flask.palletsprojects.com/en/1.1.x/quickstart/?highlight=redirect#redirects-and-errors)するようにしましょう。
折りたたむ



:おじぎ_女性:
1

