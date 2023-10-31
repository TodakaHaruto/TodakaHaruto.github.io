#! /usr/bin/env python3

import sys
import os
import urllib.parse
import sqlite3
  
#入力されたキーワードを取得
form = {} # 辞書を初期化
content_length = os.environ.get('CONTENT_LENGTH') # 入力データ長を取得
if content_length: # 入力データがある場合
  body = sys.stdin.read(int(content_length)) # 入力データを標準入力から読み込み
  params = body.split('&') # 入力データを & で分割
  for param in params: # 分割されたデータを順に処理
    key, value = param.split('=') # 分割データを = で分割
    form[key] = urllib.parse.unquote(value) # キーと値を辞書に登録（値はURLデコードする）
  
searchWord = form['param1'] # ブラウザから送信されたparam1の値を辞書から取得


#検索結果ページの表示
print("Content-type: text/html")
print("")
print("<html>")
print(" <head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/>")
print("<style>") #CSSを設定
print("body{background-color: #dcdcdc}") #背景色を設定
print("h1{font-size: 50px; padding-top: 20px; padding-bottom: 0px; margin-bottom: 10px}") #見出しの設定
print(".again{text-align:center; padding-bottom: 15px}") #aタグを中央寄せ
print("table{width: 70%;  border: solid 4px #000000; margin: auto; border-collapse: collapse;}") #検索結果表の設定
print("th{width: 30%;   border: solid 3px #000000; }")
print("td{border: solid 3px #000000;}")
print("</style>")
print("</head>")
print(" <body>")
print("<h1 align=\"center\"> 検索結果 </h1>")
print("<div class=\"again\">")
print("<a href=\"https://todakaharuto.github.io/\" >もう一度検索</a>") #再検索用タグ
print("</div>")

#書籍を検索
db_path = "bookdb.db"			# データベースファイル名を指定

con = sqlite3.connect(db_path)	# データベースに接続
con.row_factory = sqlite3.Row	# 属性名で値を取り出せるようにする
cur = con.cursor()				# カーソルを取得

try:
	# SQL文の実行
	cur.execute("select * from BOOKLIST where TITLE LIKE ? OR AUTHOR LIKE ?;", ("%" + searchWord + "%","%" + searchWord + "%",))
	rows = cur.fetchall()		# 検索結果をリストとして取得
	if not rows:				# リストが空のとき
		print("<p id=\"notFound\" align=\"center\">書籍は見つかりませんでした</p>")
	else:
		print("<table bgcolor=\"#dcdcdc\">")
		print("<tr bgcolor=\"#a9a9a9\">")
		print("<th> ID </th> <th> タイトル </th> <th> 著者 </th> <th> 出版社 </th> <th> 価格 </th> <th> ISBN </th>")
		print("</tr>")
		for row in rows:		# 検索結果を1つずつ処理
			print("<tr>")
			print("<td  align=\"center\"> %d </td>" % int(row['ID']))
			print("<td> %s </td>" % str(row['TITLE']))
			print("<td> %s </td>" % str(row['AUTHOR']))
			print("<td> %s </td>" % str(row['PUBLISHER']))
			print("<td> %d </td>" % int(row['PRICE']))
			print("<td> %s </td>" % str(row['ISBN']))
			print("</tr>")
		print("</table>")
			
            			
except sqlite3.Error as e:		# エラー処理
	print("Error occurred:", e.args[0])

con.commit()
con.close()


print(" </body>")
print("</html>")
