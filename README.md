# Vending Machine program
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
<http://localhost:5000/manegiment>  

## Folder
-app.py  
実行ファイルです。

--static  
画像ファイルが入っています。  

--templates  
htmlファイルが入っています。  

## Installation
・Flask  
・Python 3.8.3  
・mysql  

## Usage
python3 -m venv venv  
. venv/bin/activate  
  
export FLASK_APP=app  
export FLASK_ENV=development  
flask run  

実行後、管理画面URL または ユーザ画面URLを開いてください。

## Note
.gitignoreを追加するのを忘れていたので一部ファイルが残っている状態になります。
