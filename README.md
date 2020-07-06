# Vending Machine program
### 修正版 2020.07.06
app.py内を関数化しました。  
新規ドリンクの追加、ステータス変更、在庫変更ごとに違うリクエストを送る変更はわかりづらくなりそうなので、一度関数化までになっています。  
よろしくお願いいたします。  

## 18章課題 実習”自動販売機”
研修で作成している自動販売機のプログラムです。  
htmlファイル3つ、pythonファイル1つで構成されています。

## Feature
①「管理ページ」  
・販売する予定ドリンクの情報を追加  
・販売しているドリンクの在庫情報変更（公開非公開/在庫数）  
<http://localhost:5000/>  

②「購入ページ」  
・ドリンクの購入  
<http://localhost:5000/managiment>  

## Folder
-app.py  
実行ファイルです。

--static  
画像ファイルが入っています。  

--templates  
htmlファイルが入っています。  

## Installation
・必要なものはrequirements.txtに記載してあります。  
・Python 3.8.3  

## Usage
最初にinitialize.sqlを使用して、DBの作成をしてください。
  
export FLASK_APP=app  
export FLASK_ENV=development  
flask run  

実行後、管理画面URL または ユーザ画面URLを開いてください。

## Note
.gitignoreを追加するのを忘れていたので一部ファイルが残っている状態になります。
