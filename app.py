from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import sqlite3
import hashlib
import time
import re
import os
from urllib.parse import unquote

app = Flask(__name__)
app.secret_key = 'sqli_labs_secret_key_2024'

# 数据库初始化
def init_db():
    conn = sqlite3.connect('sqli_labs.db')
    cursor = conn.cursor()
    
    # 创建用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            secret_data TEXT DEFAULT 'This is secret information!'
        )
    ''')
    
    # 创建新闻表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 插入测试数据
    test_users = [
        ('admin', hashlib.md5('admin123'.encode()).hexdigest(), 'admin@sqli-labs.com', 'Admin secret data - FLAG{SQLI_ADMIN_ACCESS}'),
        ('user1', hashlib.md5('password1'.encode()).hexdigest(), 'user1@example.com', 'User1 secret data'),
        ('user2', hashlib.md5('password2'.encode()).hexdigest(), 'user2@example.com', 'User2 secret data'),
        ('dumb', hashlib.md5('dumb'.encode()).hexdigest(), 'dumb@dhakkan.com', 'Dumb user secret'),
        ('Angelina', hashlib.md5('I-kill-you'.encode()).hexdigest(), 'angelina@securityidiots.com', 'Angelina secret'),
        ('Dummy', hashlib.md5('p@ssword'.encode()).hexdigest(), 'dummy@dhakkan.local', 'Dummy secret')
    ]
    
    for user in test_users:
        cursor.execute('INSERT OR IGNORE INTO users (username, password, email, secret_data) VALUES (?, ?, ?, ?)', user)
    
    test_news = [
        ('Welcome to SQLi-Labs', 'This is a SQL injection testing platform for educational purposes.', 'admin'),
        ('SQL Injection Basics', 'Learn the fundamentals of SQL injection vulnerabilities.', 'admin'),
        ('Security Best Practices', 'Always sanitize your inputs and use parameterized queries.', 'admin')
    ]
    
    for news in test_news:
        cursor.execute('INSERT OR IGNORE INTO news (title, content, author) VALUES (?, ?, ?)', news)
    
    conn.commit()
    conn.close()

# 主页
@app.route('/')
def index():
    return render_template('index.html')

# 设置数据库
@app.route('/setup')
def setup():
    init_db()
    flash('数据库已成功初始化！', 'success')
    return redirect(url_for('index'))

# Less-1: GET - Error based - Single quotes - String
@app.route('/less-1')
def less1():
    id_param = request.args.get('id', '')
    error_msg = ""
    result = []
    
    if id_param:
        try:
            conn = sqlite3.connect('sqli_labs.db')
            cursor = conn.cursor()
            
            # 故意的SQL注入漏洞 - 直接拼接用户输入
            query = f"SELECT * FROM users WHERE id = '{id_param}' LIMIT 0,1"
            cursor.execute(query)
            result = cursor.fetchall()
            conn.close()
            
        except Exception as e:
            error_msg = str(e)
    
    return render_template('less1.html', id_param=id_param, result=result, error_msg=error_msg)

# Less-2: GET - Error based - Integer based
@app.route('/less-2')
def less2():
    id_param = request.args.get('id', '')
    error_msg = ""
    result = []
    
    if id_param:
        try:
            conn = sqlite3.connect('sqli_labs.db')
            cursor = conn.cursor()
            
            # 整数型SQL注入漏洞
            query = f"SELECT * FROM users WHERE id = {id_param} LIMIT 0,1"
            cursor.execute(query)
            result = cursor.fetchall()
            conn.close()
            
        except Exception as e:
            error_msg = str(e)
    
    return render_template('less2.html', id_param=id_param, result=result, error_msg=error_msg)

# Less-3: GET - Error based - Single quotes with twist (String)
@app.route('/less-3')
def less3():
    id_param = request.args.get('id', '')
    error_msg = ""
    result = []
    
    if id_param:
        try:
            conn = sqlite3.connect('sqli_labs.db')
            cursor = conn.cursor()
            
            # 带括号的字符串型注入
            query = f"SELECT * FROM users WHERE id = ('{id_param}') LIMIT 0,1"
            cursor.execute(query)
            result = cursor.fetchall()
            conn.close()
            
        except Exception as e:
            error_msg = str(e)
    
    return render_template('less3.html', id_param=id_param, result=result, error_msg=error_msg)

# Less-4: GET - Error based - Double Quotes
@app.route('/less-4')
def less4():
    id_param = request.args.get('id', '')
    error_msg = ""
    result = []
    
    if id_param:
        try:
            conn = sqlite3.connect('sqli_labs.db')
            cursor = conn.cursor()
            
            # 双引号型注入
            query = f'SELECT * FROM users WHERE id = ("{id_param}") LIMIT 0,1'
            cursor.execute(query)
            result = cursor.fetchall()
            conn.close()
            
        except Exception as e:
            error_msg = str(e)
    
    return render_template('less4.html', id_param=id_param, result=result, error_msg=error_msg)

# Less-5: GET - Double Injection - Single Quotes - String (Blind)
@app.route('/less-5')
def less5():
    id_param = request.args.get('id', '')
    message = ""
    
    if id_param:
        try:
            conn = sqlite3.connect('sqli_labs.db')
            cursor = conn.cursor()
            
            query = f"SELECT * FROM users WHERE id = '{id_param}' LIMIT 0,1"
            cursor.execute(query)
            result = cursor.fetchone()
            conn.close()
            
            if result:
                message = "You are in..........."
            else:
                message = "You are in... Use outfile....."
                
        except Exception as e:
            message = "You have an error in your SQL syntax"
    
    return render_template('less5.html', id_param=id_param, message=message)

# Less-6: GET - Double Injection - Double Quotes - String (Blind)
@app.route('/less-6')
def less6():
    id_param = request.args.get('id', '')
    message = ""
    
    if id_param:
        try:
            conn = sqlite3.connect('sqli_labs.db')
            cursor = conn.cursor()
            
            query = f'SELECT * FROM users WHERE id = "{id_param}" LIMIT 0,1'
            cursor.execute(query)
            result = cursor.fetchone()
            conn.close()
            
            if result:
                message = "You are in..........."
            else:
                message = "You are in... Use outfile....."
                
        except Exception as e:
            message = "You have an error in your SQL syntax"
    
    return render_template('less6.html', id_param=id_param, message=message)

# Less-7: GET - Dump into outfile - String
@app.route('/less-7')
def less7():
    id_param = request.args.get('id', '')
    message = ""
    
    if id_param:
        try:
            conn = sqlite3.connect('sqli_labs.db')
            cursor = conn.cursor()
            
            query = f"SELECT * FROM users WHERE id = ('{id_param}') LIMIT 0,1"
            cursor.execute(query)
            result = cursor.fetchone()
            conn.close()
            
            if result:
                message = "You are in... Use outfile...."
            else:
                message = "You are in... Use outfile...."
                
        except Exception as e:
            message = "You have an error in your SQL syntax"
    
    return render_template('less7.html', id_param=id_param, message=message)

# Less-8: GET - Blind - Boolean Based - Single Quotes
@app.route('/less-8')
def less8():
    id_param = request.args.get('id', '')
    message = ""
    
    if id_param:
        try:
            conn = sqlite3.connect('sqli_labs.db')
            cursor = conn.cursor()
            
            query = f"SELECT * FROM users WHERE id = '{id_param}' LIMIT 0,1"
            cursor.execute(query)
            result = cursor.fetchone()
            conn.close()
            
            if result:
                message = "You are in..........."
            else:
                message = "You are in... Use Blind injection to extract data"
                
        except Exception as e:
            # 不显示错误信息，这是盲注
            if id_param:
                message = "You are in... Use Blind injection to extract data"
    
    return render_template('less8.html', id_param=id_param, message=message)

# Less-9: GET - Blind - Time based - Single Quotes
@app.route('/less-9')
def less9():
    id_param = request.args.get('id', '')
    message = ""
    start_time = time.time()
    
    if id_param:
        try:
            conn = sqlite3.connect('sqli_labs.db')
            cursor = conn.cursor()
            
            # 模拟时间延迟（简化版）
            if 'sleep' in id_param.lower() or 'benchmark' in id_param.lower():
                time.sleep(2)  # 模拟延迟
            
            query = f"SELECT * FROM users WHERE id = '{id_param}' LIMIT 0,1"
            cursor.execute(query)
            result = cursor.fetchone()
            conn.close()
            
            message = "You are in... Use Time based blind injection to extract data"
                
        except Exception as e:
            message = "You are in... Use Time based blind injection to extract data"
    
    execution_time = time.time() - start_time
    return render_template('less9.html', id_param=id_param, message=message, execution_time=f"{execution_time:.2f}")

# Less-10: GET - Blind - Time based - Double Quotes
@app.route('/less-10')
def less10():
    id_param = request.args.get('id', '')
    message = ""
    start_time = time.time()
    
    if id_param:
        try:
            conn = sqlite3.connect('sqli_labs.db')
            cursor = conn.cursor()
            
            if 'sleep' in id_param.lower() or 'benchmark' in id_param.lower():
                time.sleep(2)
            
            query = f'SELECT * FROM users WHERE id = "{id_param}" LIMIT 0,1'
            cursor.execute(query)
            result = cursor.fetchone()
            conn.close()
            
            message = "You are in... Use Time based blind injection to extract data"
                
        except Exception as e:
            message = "You are in... Use Time based blind injection to extract data"
    
    execution_time = time.time() - start_time
    return render_template('less10.html', id_param=id_param, message=message, execution_time=f"{execution_time:.2f}")

# Less-11: POST - Error Based - Single Quotes
@app.route('/less-11', methods=['GET', 'POST'])
def less11():
    error_msg = ""
    result = []
    login_success = False
    
    if request.method == 'POST':
        username = request.form.get('uname', '')
        password = request.form.get('passwd', '')
        
        try:
            conn = sqlite3.connect('sqli_labs.db')
            cursor = conn.cursor()
            
            # 故意的SQL注入漏洞
            query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
            cursor.execute(query)
            result = cursor.fetchall()
            conn.close()
            
            if result:
                login_success = True
                
        except Exception as e:
            error_msg = str(e)
    
    return render_template('less11.html', error_msg=error_msg, result=result, login_success=login_success)

# Less-12: POST - Error Based - Double Quotes
@app.route('/less-12', methods=['GET', 'POST'])
def less12():
    error_msg = ""
    result = []
    login_success = False
    
    if request.method == 'POST':
        username = request.form.get('uname', '')
        password = request.form.get('passwd', '')
        
        try:
            conn = sqlite3.connect('sqli_labs.db')
            cursor = conn.cursor()
            
            query = f'SELECT * FROM users WHERE username = ("{username}") AND password = ("{password}")'
            cursor.execute(query)
            result = cursor.fetchall()
            conn.close()
            
            if result:
                login_success = True
                
        except Exception as e:
            error_msg = str(e)
    
    return render_template('less12.html', error_msg=error_msg, result=result, login_success=login_success)

# API端点 - 用于AJAX请求
@app.route('/api/user/<int:user_id>')
def api_user(user_id):
    try:
        conn = sqlite3.connect('sqli_labs.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return jsonify({
                'success': True,
                'data': {
                    'id': result[0],
                    'username': result[1],
                    'email': result[2]
                }
            })
        else:
            return jsonify({'success': False, 'message': 'User not found'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    if not os.path.exists('sqli_labs.db'):
        init_db()
    app.run(debug=True, host='0.0.0.0', port=5000) 