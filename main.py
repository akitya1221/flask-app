from crypt import methods
from operator import methodcaller
from re import A
from unicodedata import category
from unittest import result
from wsgiref.util import request_uri
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
    sql = 'SELECT b.id, c.category_name, b.title, b.price, b.arrival_day FROM books AS b LEFT OUTER JOIN category AS c ON b.category_id = c.id'
    
    conn = conn_db() #DBに接続
    cursor = conn.cursor() #カーソルを作成
    cursor.execute(sql)
    rows = cursor.fetchall() 
    conn.close()
    
    # 辞書を作成
    books = []
    for row in rows: #カーソルの中身を変数に代入
        books.append({'id': row[0], 'category_name': row[1], 'title': row[2], 'price': row[3], 'arrival_day': row[4]})
    return render_template(
        'index.html',
        # 作成した辞書をindex.htmlへ渡す（引数は何個でも設定可）
        books=books
    )
    
#曖昧検索機能
@app.route('/search', methods=['POST']) 
def search():
    
    text = "'" + '%' + request.form['search-text'] + '%' + "'"
    test = "'" + request.form['search-text'] + "'"
    
    ambiguous = 'SELECT * FROM books WHERE title LIKE %s' % text
    
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute(ambiguous)
    book = cursor.fetchall() 
    conn.close()
    
    search_result = []
    for row in book:
        search_result.append({'id': row[0], 'title': row[1], 'price': row[2], 'arrival_day': row[3], 'category': row[4]})
    
    return render_template('search.html', result_book=search_result)
   
@app.route('/form') 
def form():
    
    c_list = 'SELECT category_name FROM category'
    
    conn = conn_db()
    cursor = conn.cursor()  
    cursor.execute(c_list)
    rows = cursor.fetchall() 
    conn.close()
    
    return render_template('form.html', category=rows)

# INSERT処理
@app.route('/add', methods=['POST'])  
def add():
    # 画面から入力された値を変数に代入する[name]
    category = request.form['category']
    title = request.form['title']
    price = request.form['price']
    arrival_day = request.form['day']
    
    if category == '文学・文芸':
        category_id = 1
    elif category == 'ビジネス':
        category_id = 2
    elif category == '趣味・実用':
        category_id = 3
    elif category == '専門書':
        category_id = 4
    elif category == 'コミック':
        category_id = 5
    elif category == '絵本・児童書':
        category_id = 6
    else:
        pass
    
    # arrival_dayが入力されなかった場合の処理
    if len(arrival_day) == 0:
        arrival_day = '未定'
    else:
        pass
    
    # 「%s」を使用することにより、変数を文字列に入れ込むことができる
    insert_book = 'INSERT INTO books VALUES (0, %s, %s, %s, %s)'
    
    conn = conn_db() #DBに接続
    cursor = conn.cursor()  
    cursor.execute(insert_book, (title, price, arrival_day, category_id))
    conn.commit()
    conn.close()
    
    # 登録後、index画面へリダイレクトする
    return redirect(url_for('index'))

# DELETE処理
# <型:変数名>と記載することで、パスパラメーターを取得することができる
@app.route('/delete/<int:book_id>', methods=['GET'])
def DeletBook(book_id):
    
    sql = 'DELETE FROM books WHERE id = %s' % book_id
    
    conn = conn_db()
    cursor = conn.cursor()  
    cursor.execute(sql)
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

# 編集画面の処理
# booksテーブルのidを元にSELECTし、結果を画面に表示する。
@app.route('/edit/<int:book_id>', methods=['GET'])
def SelectBook(book_id):
        
    # PRIMARY KEYで条件を絞っているため、抽出されるのは1件
    select_book = 'SELECT * FROM books WHERE id = %s' % book_id
    c_list = 'SELECT category_name FROM category'
    
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute(select_book)
    # fetchall()関数にて、テーブルの各カラムを取得
    row = cursor.fetchall() 
    
    cursor.execute(c_list)
    c_list = cursor.fetchall() 
    
    conn.close()
        
    return render_template('edit.html', book=row, category=c_list)

# UPDATE処理(2)
@app.route('/EditBook', methods=['POST'])
def EditBook():
        
    category = request.form['category']
    book_id = request.form['id']
    title = request.form['title']
    price = request.form['price']
    arrival_day = request.form['day']
    
    # arrival_dayが入力されなかった場合の処理
    if len(arrival_day) == 0:
        arrival_day = '未定'
    else:
        pass
    
    if category == '文学・文芸':
        category_id = 1
    elif category == 'ビジネス':
        category_id = 2
    elif category == '趣味・実用':
        category_id = 3
    elif category == '専門書':
        category_id = 4
    elif category == 'コミック':
        category_id = 5
    elif category == '絵本・児童書':
        category_id = 6
    else:
        pass
        
    update_book = 'UPDATE books SET title = %s, price = %s, arrival_day = %s, category_id = %s WHERE id = %s'
    
    conn = conn_db() #DBに接続
    cursor = conn.cursor()  
    cursor.execute(update_book ,(title, price, arrival_day, category_id, book_id))
    conn.commit()
    # commit()関数を忘れないこと！
    conn.close()
    
    return redirect(url_for('index'))