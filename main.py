from flaskr import app
from flask import render_template, request, redirect, url_for
import mysql.connector

#DB接続情報
def conn_db():
    conn = mysql.connector.connect(
        host = '127.0.0.1',
        user = 'root',
        passwd = 'password',
        db = 'flask_db'
    )
    return conn 
                    
# top画面にアクセスした際に実行される
@app.route('/')
def index():
    # SQL文
    sql = 'SELECT * FROM books'
    
    conn = conn_db() #DBに接続
    cursor = conn.cursor() #カーソルを作成
    cursor.execute(sql)
    rows = cursor.fetchall() 
    conn.close()
    
    # 辞書を作成
    books = []
    for row in rows: #カーソルの中身を変数に代入
        books.append({'id': row[0], 'title': row[1], 'price': row[2], 'arrival_day': row[3]})
    return render_template(
        'index.html',
        # 作成した辞書をindex.htmlへ渡す（引数は何個でも設定可）
        books=books
    )
   
@app.route('/form') 
def form():
    return render_template(
        'form.html'
    )

# INSERT処理
@app.route('/add', methods=['POST'])  
def add():
    # 画面から入力された値を変数に代入する[name]
    title = request.form['title']
    price = request.form['price']
    arrival_day = request.form['day']
    
    # 「%s」を使用することにより、変数を文字列に入れ込むことができる
    sql = "INSERT INTO books VALUES (0, %s, %s, %s)"
    
    conn = conn_db() #DBに接続
    cursor = conn.cursor()  
    cursor.execute(sql, (title, price, arrival_day))
    conn.commit()
    conn.close()
    
    # 登録後、index画面へリダイレクトする
    return redirect(url_for('index'))