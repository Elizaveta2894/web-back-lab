from flask import Blueprint, render_template, jsonify, request, session
import json
import os
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import sqlite3
from datetime import datetime
from functools import wraps

lab9 = Blueprint('lab9', __name__,
                 template_folder='templates/lab9',
                 static_folder='static/lab9')

ADMIN_USERS = {
    'admin': 'admin123',
    'santa': 'santa2024',
    'user': 'user123'
}
congratulations = [
    "С Новым годом! Желаю счастья и здоровья!",
    "Пусть новый год принесет много радости!",
    "Желаю исполнения всех желаний в новом году!",
    "Пусть каждый день нового года будет наполнен волшебством!",
    "Счастья, любви и процветания в новом году!",
    "Пусть ангел-хранитель оберегает вас весь год!",
    "Желаю финансового благополучия и стабильности!",
    "Пусть все мечты сбудутся в новом году!",
    "Здоровья вам и вашим близким в новом году!",
    "Желаю интересных путешествий и новых открытий!"
]
special_gifts = {
    7: "🎅 Эксклюзивный подарок от Деда Мороза!",
    8: "⭐ Золотая звезда желаний!",
    9: "🎄 Волшебная еловая шишка!"
}
def init_db():
    """Инициализация базы данных с обновленной структурой"""
    conn = sqlite3.connect('lab9_gifts.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS gift_positions')
    cursor.execute('DROP TABLE IF EXISTS opened_boxes')
    cursor.execute('DROP TABLE IF EXISTS user_sessions')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gift_positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gift_id INTEGER UNIQUE NOT NULL,
            top REAL NOT NULL,
            left_pos REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS opened_boxes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gift_id INTEGER NOT NULL,
            session_id TEXT NOT NULL,
            user_id TEXT,
            ip_address TEXT,
            opened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Таблица для сессий пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE NOT NULL,
            username TEXT,
            is_authenticated BOOLEAN DEFAULT 0,
            login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("База данных инициализирована")

def get_db_connection():
    """Получение соединения с базой данных"""
    conn = sqlite3.connect('lab9_gifts.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    """Декоратор для проверки аутентификации"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return jsonify({'error': 'Требуется авторизация'}), 401
        return f(*args, **kwargs)
    return decorated_function

def check_auth(username, password):
    """Проверка учетных данных"""
    return ADMIN_USERS.get(username) == password

def get_user_session():
    """Получение или создание сессии пользователя"""
    user_session_id = session.get('lab9_session_id')
    if not user_session_id:
        user_session_id = os.urandom(16).hex()
        session['lab9_session_id'] = user_session_id
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR IGNORE INTO user_sessions (session_id, is_authenticated)
        VALUES (?, ?)
    ''', (user_session_id, 0))
    
    conn.commit()
    conn.close()
    
    return user_session_id

def is_user_authenticated():
    """Проверка, авторизован ли пользователь"""
    user_session_id = session.get('lab9_session_id')
    if not user_session_id:
        return False
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT is_authenticated FROM user_sessions WHERE session_id = ?', (user_session_id,))
    result = cursor.fetchone()
    conn.close()
    
    return result and result['is_authenticated'] == 1

def authenticate_user(username):
    """Авторизация пользователя"""
    user_session_id = get_user_session()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE user_sessions 
        SET username = ?, is_authenticated = 1 
        WHERE session_id = ?
    ''', (username, user_session_id))
    
    conn.commit()
    conn.close()
    
    session['authenticated'] = True
    session['username'] = username
    return True

def logout_user():
    """Выход пользователя"""
    user_session_id = session.get('lab9_session_id')
    if user_session_id:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE user_sessions SET is_authenticated = 0 WHERE session_id = ?', (user_session_id,))
        conn.commit()
        conn.close()
    
    session.pop('authenticated', None)
    session.pop('username', None)
    return True

def save_gift_position(gift_id, position):
    """Сохранение позиции коробки в БД"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT OR REPLACE INTO gift_positions (gift_id, top, left_pos)
            VALUES (?, ?, ?)
        ''', (gift_id, position['top'], position['left']))
        conn.commit()
    except Exception as e:
        print(f"Error saving gift position: {e}")
    finally:
        conn.close()

def get_gift_position(gift_id):
    """Получение позиции коробки из БД"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT top, left_pos FROM gift_positions WHERE gift_id = ?', (gift_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {'top': result['top'], 'left': result['left_pos']}
    return None

def get_all_gift_positions():
    """Получение всех позиций коробок"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT gift_id, top, left_pos FROM gift_positions ORDER BY gift_id')
    results = cursor.fetchall()
    conn.close()
    
    positions = {}
    for row in results:
        positions[str(row['gift_id'])] = {'top': row['top'], 'left': row['left_pos']}
    return positions

def is_gift_opened(gift_id):
    """Проверка, открыта ли коробка (любым пользователем)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as count FROM opened_boxes WHERE gift_id = ?', (gift_id,))
    result = cursor.fetchone()
    conn.close()
    
    return result['count'] > 0

def mark_gift_as_opened(gift_id, session_id, ip_address):
    """Отметить коробку как открытую"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Получаем username из сессии
    username = session.get('username')
    
    cursor.execute('''
        INSERT INTO opened_boxes (gift_id, session_id, user_id, ip_address)
        VALUES (?, ?, ?, ?)
    ''', (gift_id, session_id, username, ip_address))
    
    conn.commit()
    conn.close()

def count_opened_by_user(session_id):
    """Подсчет коробок, открытых текущим пользователем"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as count FROM opened_boxes WHERE session_id = ?', (session_id,))
    result = cursor.fetchone()
    conn.close()
    
    return result['count']

def count_total_opened():
    """Общее количество открытых коробок"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(DISTINCT gift_id) as count FROM opened_boxes')
    result = cursor.fetchone()
    conn.close()
    
    return result['count']

def get_opened_gifts():
    """Получение списка открытых коробок"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT DISTINCT gift_id FROM opened_boxes ORDER BY gift_id')
    results = cursor.fetchall()
    conn.close()
    
    return [row['gift_id'] for row in results]

def generate_random_position(gift_id, occupied_positions, max_attempts=100):
    """Генерирует случайную позицию, избегая защищенных зон и других коробок"""
    
    protected_areas = [
        {'top': 0, 'left': 0, 'width': 100, 'height': 15},  # Инструкции
        {'top': 85, 'left': 35, 'width': 30, 'height': 15}   # Кнопка сброса
    ]
    
    for attempt in range(max_attempts):
        top = random.uniform(15, 70)  
        left = random.uniform(5, 80)   

        box_size = 15
        
        in_protected_area = False
        for area in protected_areas:
            if not (left + box_size < area['left'] or 
                    left > area['left'] + area['width'] or
                    top + box_size < area['top'] or 
                    top > area['top'] + area['height']):
                in_protected_area = True
                break
        
        if in_protected_area:
            continue

        too_close = False
        for pos in occupied_positions:
            center_x1 = left + box_size / 2
            center_y1 = top + box_size / 2
            center_x2 = pos['left'] + box_size / 2
            center_y2 = pos['top'] + box_size / 2
            
            distance = ((center_x1 - center_x2) ** 2 + (center_y1 - center_y2) ** 2) ** 0.5
            
            if distance < 20:
                too_close = True
                break
        
        if too_close:
            continue
        
        # Если все проверки пройдены, возвращаем позицию
        return {'top': round(top, 2), 'left': round(left, 2)}
    
    # Если не удалось найти позицию, используем предопределенные позиции
    default_positions = [
        {'top': 15, 'left': 10}, {'top': 15, 'left': 30}, {'top': 15, 'left': 50}, {'top': 15, 'left': 70},
        {'top': 35, 'left': 10}, {'top': 35, 'left': 30}, {'top': 35, 'left': 50}, {'top': 35, 'left': 70},
        {'top': 55, 'left': 20}, {'top': 55, 'left': 60}
    ]
    
    if gift_id < len(default_positions):
        return default_positions[gift_id]
    else:
        return {'top': 20, 'left': 20}

def init_gifts():
    """Инициализация данных о подарках"""
    # Инициализируем базу данных
    init_db()
    
    # Проверяем наличие папки для статики
    static_path = Path(__file__).parent / "static" / "lab9"
    static_path.mkdir(parents=True, exist_ok=True)
    
    # Создаем тестовые изображения подарков, если их нет
    for i in range(1, 11):
        gift_file = static_path / f"gift{i}.jpg"
        if not gift_file.exists():
            img = Image.new('RGB', (200, 200), color=(random.randint(100, 255), 
                                                      random.randint(100, 255), 
                                                      random.randint(100, 255)))
            d = ImageDraw.Draw(img)
            
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            d.text((100, 100), f"Подарок {i}", fill="white", font=font, anchor="mm")
            img.save(gift_file)
            print(f"Создано изображение: static/lab9/gift{i}.jpg")

def get_gifts_data():
    """Получение данных о всех подарках"""
    # Получаем все позиции из БД
    positions = get_all_gift_positions()
    
    # Перемешиваем поздравления
    random_congrats = congratulations.copy()
    random.shuffle(random_congrats)
    
    # Получаем список открытых коробок
    opened_gifts = get_opened_gifts()
    
    # Создаем словарь с данными о подарках
    gifts = {}
    for i in range(10):
        gift_id = str(i)
        
        # Получаем или создаем позицию
        if gift_id in positions:
            position = positions[gift_id]
        else:
            # Получаем занятые позиции
            occupied = []
            for j in range(i):
                occupied_id = str(j)
                if occupied_id in positions:
                    occupied.append(positions[occupied_id])
            
            # Генерируем новую позицию
            position = generate_random_position(i, occupied)
            save_gift_position(i, position)
        
        # Проверяем, открыта ли коробка
        opened = int(gift_id) in opened_gifts
        
        gifts[gift_id] = {
            'id': i,
            'congratulation': random_congrats[i],
            'gift_image': f'gift{i+1}.jpg',
            'opened': opened,
            'position': position
        }
    
    return gifts

@lab9.route('/')
def lab9_index():
    """Главная страница lab9"""
    init_gifts()
    return render_template('lab9/lab9.html')

@lab9.route('/lab9/login', methods=['POST'])
def login():
    """Авторизация пользователя"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'success': False, 'error': 'Введите логин и пароль'})
    
    if check_auth(username, password):
        authenticate_user(username)
        return jsonify({
            'success': True,
            'username': username,
            'message': f'Добро пожаловать, {username}!'
        })
    
    return jsonify({'success': False, 'error': 'Неверный логин или пароль'})

@lab9.route('/lab9/logout', methods=['POST'])
def logout():
    """Выход пользователя"""
    logout_user()
    return jsonify({'success': True, 'message': 'Вы вышли из системы'})

@lab9.route('/lab9/auth_status')
def auth_status():
    """Проверка статуса авторизации"""
    return jsonify({
        'authenticated': is_user_authenticated(),
        'username': session.get('username')
    })

@lab9.route('/lab9/get_gifts')
def get_gifts():
    """Получение данных о подарках"""
    gifts_data = get_gifts_data()
    user_session_id = get_user_session()
    unopened_count = sum(1 for gift in gifts_data.values() if not gift['opened'])
    user_opened_count = count_opened_by_user(user_session_id)
    authenticated = is_user_authenticated()
    if not authenticated:
        for gift_id in special_gifts.keys():
            if str(gift_id) in gifts_data:
                gifts_data[str(gift_id)]['hidden'] = True
    
    return jsonify({
        'gifts': gifts_data,
        'unopened_count': unopened_count,
        'opened_count': user_opened_count,
        'total_gifts': len(gifts_data),
        'authenticated': authenticated,
        'username': session.get('username'),
        'special_gifts': list(special_gifts.keys()) if authenticated else []
    })

@lab9.route('/lab9/open_gift', methods=['POST'])
def open_gift():
    """Открытие подарка"""
    data = request.json
    gift_id = int(data.get('gift_id', -1))
    
    if gift_id < 0 or gift_id >= 10:
        return jsonify({'error': 'Неверный ID подарка'}), 400
    
    # Проверяем, является ли подарок специальным и доступен только авторизованным
    if gift_id in special_gifts and not is_user_authenticated():
        return jsonify({'error': 'Этот подарок доступен только авторизованным пользователям!'}), 403
    
    # Получаем ID сессии
    user_session_id = get_user_session()
    
    # Проверяем, сколько коробок уже открыл пользователь
    user_opened_count = count_opened_by_user(user_session_id)
    if user_opened_count >= 3:
        return jsonify({'error': 'Вы уже открыли максимальное количество коробок (3)!'}), 400
    
    # Проверяем, не открыта ли уже эта коробка
    if is_gift_opened(gift_id):
        return jsonify({'error': 'Эта коробка уже пуста!'}), 400
    
    # Получаем IP-адрес пользователя
    ip_address = request.remote_addr
    
    # Отмечаем коробку как открытую
    mark_gift_as_opened(gift_id, user_session_id, ip_address)
    
    # Получаем обновленные данные
    gifts_data = get_gifts_data()
    
    # Подсчитываем количество неоткрытых коробок
    unopened_count = sum(1 for gift in gifts_data.values() if not gift['opened'])
    
    # Увеличиваем счетчик открытых пользователем коробок
    user_opened_count += 1
    
    # Выбираем поздравление
    if gift_id in special_gifts and is_user_authenticated():
        congratulation = special_gifts[gift_id]
    else:
        congratulation = congratulations[gift_id % len(congratulations)]
    
    return jsonify({
        'success': True,
        'congratulation': congratulation,
        'gift_image': f'gift{gift_id + 1}.jpg',
        'opened_count': user_opened_count,
        'unopened_count': unopened_count,
        'total_gifts': len(gifts_data),
        'is_special': gift_id in special_gifts
    })

@lab9.route('/lab9/santa_refill', methods=['POST'])
@login_required
def santa_refill():
    """Дед Мороз наполняет все коробки снова"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM opened_boxes')
    cursor.execute('DELETE FROM gift_positions')
    conn.commit()
    gifts_data = get_gifts_data()
    
    conn.close()
    
    return jsonify({
        'success': True,
        'message': '🎅 Дед Мороз наполнил все коробки новыми подарками!',
        'refilled_by': session.get('username')
    })

@lab9.route('/lab9/reset', methods=['POST'])
def reset_gifts():
    """Сброс всех подарков (для тестирования)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Очищаем таблицы
    cursor.execute('DELETE FROM opened_boxes')
    cursor.execute('DELETE FROM gift_positions')
    cursor.execute('DELETE FROM user_sessions')
    
    # Сбрасываем автоинкремент
    cursor.execute('DELETE FROM sqlite_sequence')
    
    conn.commit()
    conn.close()
    
    # Очищаем сессию
    session.clear()
    
    return jsonify({
        'success': True,
        'message': 'Все подарки сброшены!'
    })

@lab9.route('/lab9/check_opened')
def check_opened():
    """Проверка открытых коробок текущим пользователем"""
    user_session_id = get_user_session()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT gift_id FROM opened_boxes WHERE session_id = ?', (user_session_id,))
    results = cursor.fetchall()
    conn.close()
    
    opened_boxes = [row['gift_id'] for row in results]
    
    return jsonify({
        'opened_boxes': opened_boxes,
        'count': len(opened_boxes)
    })

@lab9.route('/lab9/get_stats')
def get_stats():
    """Получение статистики по подаркам"""
    gifts_data = get_gifts_data()
    
    total = len(gifts_data)
    
    opened_total = count_total_opened()

    user_session_id = get_user_session()
    opened_user = count_opened_by_user(user_session_id) if user_session_id else 0

    available = total - opened_total

    user_can_open = min(3 - opened_user, available)
    
    return jsonify({
        'total': total,
        'opened_total': opened_total,
        'opened_user': opened_user,
        'available': available,
        'user_can_open': user_can_open
    })

@lab9.route('/lab9/admin/reset_all', methods=['POST'])
def admin_reset_all():
    """Полный сброс (только для администратора)"""
    return reset_gifts()