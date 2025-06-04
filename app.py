from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, g
import sqlite3
import hashlib
import time
import re
import os
import threading
import queue
from urllib.parse import unquote
from contextlib import contextmanager

app = Flask(__name__)
app.secret_key = 'sqli_labs_secret_key_2024'

# 环境配置
FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
DEBUG_MODE = os.environ.get('FLASK_DEBUG', '1') == '1' or FLASK_ENV == 'development'

app.config['DEBUG'] = DEBUG_MODE
app.config['DEVELOPMENT'] = DEBUG_MODE

# 数据库连接池配置
DATABASE = 'sqli_labs.db'
POOL_SIZE = 20  # 连接池大小
CONNECTION_TIMEOUT = 30  # 连接超时时间

class DatabasePool:
    """数据库连接池"""
    def __init__(self, database, pool_size=POOL_SIZE):
        self.database = database
        self.pool_size = pool_size
        self.pool = queue.Queue(maxsize=pool_size)
        self.active_connections = 0
        self.lock = threading.Lock()
        self._initialize_pool()
    
    def _initialize_pool(self):
        """初始化连接池"""
        for _ in range(self.pool_size):
            conn = self._create_connection()
            if conn:
                self.pool.put(conn)
    
    def _create_connection(self):
        """创建新的数据库连接"""
        try:
            conn = sqlite3.connect(
                self.database, 
                check_same_thread=False,
                timeout=CONNECTION_TIMEOUT,
                isolation_level=None  # 自动提交模式
            )
            conn.row_factory = sqlite3.Row  # 启用字典式访问
            # 设置SQLite性能优化参数
            conn.execute('PRAGMA journal_mode=WAL')  # 写前日志模式，提升并发性能
            conn.execute('PRAGMA synchronous=NORMAL')  # 平衡性能和安全性
            conn.execute('PRAGMA cache_size=10000')  # 增大缓存
            conn.execute('PRAGMA temp_store=MEMORY')  # 临时表存储在内存中
            return conn
        except Exception as e:
            print(f"创建数据库连接失败: {e}")
            return None
    
    def get_connection(self, timeout=5):
        """从连接池获取连接"""
        try:
            conn = self.pool.get(timeout=timeout)
            # 验证连接是否有效
            conn.execute('SELECT 1')
            return conn
        except queue.Empty:
            # 连接池为空，尝试创建新连接
            with self.lock:
                if self.active_connections < self.pool_size * 2:  # 允许临时超出池大小
                    conn = self._create_connection()
                    if conn:
                        self.active_connections += 1
                        return conn
            raise Exception("数据库连接池已满，请稍后重试")
        except Exception as e:
            # 连接失效，创建新连接
            conn = self._create_connection()
            if conn:
                return conn
            raise Exception(f"获取数据库连接失败: {e}")
    
    def return_connection(self, conn):
        """归还连接到连接池"""
        try:
            if conn and self.pool.qsize() < self.pool_size:
                self.pool.put(conn)
            else:
                # 连接池已满，关闭连接
                if conn:
                    conn.close()
                with self.lock:
                    self.active_connections = max(0, self.active_connections - 1)
        except Exception as e:
            print(f"归还数据库连接失败: {e}")
            if conn:
                conn.close()
    
    def close_all(self):
        """关闭所有连接"""
        while not self.pool.empty():
            try:
                conn = self.pool.get_nowait()
                conn.close()
            except:
                pass

# 创建全局连接池
db_pool = DatabasePool(DATABASE)

@contextmanager
def get_db_connection():
    """数据库连接上下文管理器"""
    conn = None
    try:
        conn = db_pool.get_connection()
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()  # 发生错误时回滚
        raise e
    finally:
        if conn:
            db_pool.return_connection(conn)

def get_db():
    """获取当前请求的数据库连接"""
    if 'db' not in g:
        g.db = db_pool.get_connection()
    return g.db

@app.teardown_appcontext
def close_db(error):
    """请求结束时归还数据库连接"""
    db = g.pop('db', None)
    if db is not None:
        db_pool.return_connection(db)

# 应用关闭时清理连接池
@app.teardown_appcontext
def cleanup_db_pool(error):
    """应用关闭时清理连接池"""
    pass

# 注册应用关闭时的清理函数
import atexit
atexit.register(lambda: db_pool.close_all())

# 数据库初始化
def init_db():
    with get_db_connection() as conn:
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

@app.route('/')
def index():
    return render_template('index.html')

# 设置数据库
@app.route('/setup')
def setup():
    try:
        init_db()
        flash('数据库已成功初始化！', 'success')
    except Exception as e:
        flash(f'数据库初始化失败: {str(e)}', 'danger')
    return redirect(url_for('index'))

# Less-1: GET - Error based - Single quotes - String
@app.route('/less-1')
def less1():
    id_param = request.args.get('id', '')
    error_msg = ""
    result = []
    
    if id_param:
        try:
            conn = get_db()
            cursor = conn.cursor()
            
            # 故意的SQL注入漏洞 - 直接拼接用户输入
            query = f"SELECT * FROM users WHERE id = '{id_param}' LIMIT 0,1"
            cursor.execute(query)
            result = cursor.fetchall()
            
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
            conn = get_db()
            cursor = conn.cursor()
            
            # 整数型SQL注入漏洞
            query = f"SELECT * FROM users WHERE id = {id_param} LIMIT 0,1"
            cursor.execute(query)
            result = cursor.fetchall()
            
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
            conn = get_db()
            cursor = conn.cursor()
            
            # 带括号的字符串型注入
            query = f"SELECT * FROM users WHERE id = ('{id_param}') LIMIT 0,1"
            cursor.execute(query)
            result = cursor.fetchall()
            
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
            conn = get_db()
            cursor = conn.cursor()
            
            # 双引号型注入
            query = f'SELECT * FROM users WHERE id = ("{id_param}") LIMIT 0,1'
            cursor.execute(query)
            result = cursor.fetchall()
            
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
            conn = get_db()
            cursor = conn.cursor()
            
            query = f"SELECT * FROM users WHERE id = '{id_param}' LIMIT 0,1"
            cursor.execute(query)
            result = cursor.fetchone()
            
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
            conn = get_db()
            cursor = conn.cursor()
            
            query = f'SELECT * FROM users WHERE id = "{id_param}" LIMIT 0,1'
            cursor.execute(query)
            result = cursor.fetchone()
            
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
            conn = get_db()
            cursor = conn.cursor()
            
            query = f"SELECT * FROM users WHERE id = ('{id_param}') LIMIT 0,1"
            cursor.execute(query)
            result = cursor.fetchone()
            
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
            conn = get_db()
            cursor = conn.cursor()
            
            query = f"SELECT * FROM users WHERE id = '{id_param}' LIMIT 0,1"
            cursor.execute(query)
            result = cursor.fetchone()
            
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
            conn = get_db()
            cursor = conn.cursor()
            
            # 模拟时间延迟（简化版）
            if 'sleep' in id_param.lower() or 'benchmark' in id_param.lower():
                time.sleep(2)  # 模拟延迟
            
            query = f"SELECT * FROM users WHERE id = '{id_param}' LIMIT 0,1"
            cursor.execute(query)
            result = cursor.fetchone()
            
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
            conn = get_db()
            cursor = conn.cursor()
            
            if 'sleep' in id_param.lower() or 'benchmark' in id_param.lower():
                time.sleep(2)
            
            query = f'SELECT * FROM users WHERE id = "{id_param}" LIMIT 0,1'
            cursor.execute(query)
            result = cursor.fetchone()
            
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
            conn = get_db()
            cursor = conn.cursor()
            
            # 故意的SQL注入漏洞
            query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
            cursor.execute(query)
            result = cursor.fetchall()
            
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
            conn = get_db()
            cursor = conn.cursor()
            
            query = f'SELECT * FROM users WHERE username = "{username}" AND password = "{password}"'
            cursor.execute(query)
            result = cursor.fetchall()
            
            if result:
                login_success = True
                
        except Exception as e:
            error_msg = str(e)
    
    return render_template('less12.html', error_msg=error_msg, result=result, login_success=login_success)

# API端点 - 用于AJAX请求
@app.route('/api/user/<int:user_id>')
def api_user(user_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        
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
    # 确保数据库文件存在
    if not os.path.exists(DATABASE):
        try:
            init_db()
            print("✅ 数据库初始化完成")
        except Exception as e:
            print(f"❌ 数据库初始化失败: {e}")
    
    print(f"🚀 启动Flask应用 (调试模式: {DEBUG_MODE})")
    print(f"🔗 数据库连接池大小: {POOL_SIZE}")
    print(f"🌐 访问地址: http://localhost:5000")
    
    try:
        app.run(debug=DEBUG_MODE, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n🛑 正在关闭应用...")
        db_pool.close_all()
        print("✅ 数据库连接池已清理")
    except Exception as e:
        print(f"❌ 应用启动失败: {e}")
        db_pool.close_all() 