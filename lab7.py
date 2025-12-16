from flask import Blueprint, render_template, request, jsonify, abort
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

lab7 = Blueprint('lab7', __name__)

def db_connect():
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='liza_stabrovskaya_knowledge_base',
        user='liza_stabrovskaya_knowledge_base',
        password='555'       
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

def init_films_table():
    try:
        conn, cur = db_connect()
        cur.execute("SELECT 1 FROM films LIMIT 1;")
        db_close(conn, cur)
        print("Films table exists and accessible")
        return True
    except Exception as e:
        print(f"Error accessing films table: {e}")
        return False

def validate_film_data(film_data, is_update=False):
    errors = {}
    current_year = datetime.now().year
    
    title_ru = film_data.get('title_ru', '').strip()
    title = film_data.get('title', '').strip()
    
    if not title_ru:
        errors['title_ru'] = 'Русское название обязательно для заполнения'
    elif len(title_ru) > 200:
        errors['title_ru'] = 'Русское название слишком длинное (макс. 200 символов)'
    
    if not title and not title_ru: 
        errors['title'] = 'Заполните хотя бы одно название'
    elif not title and title_ru:  

        pass
    elif len(title) > 200:
        errors['title'] = 'Оригинальное название слишком длинное (макс. 200 символов)'
    
    year = film_data.get('year')
    if year is None:
        errors['year'] = 'Год обязателен для заполнения'
    else:
        try:
            year_int = int(year)
            if year_int < 1895:
                errors['year'] = f'Год не может быть раньше 1895 (первый фильм)'
            elif year_int > current_year + 5:  
                errors['year'] = f'Год не может быть больше {current_year + 5}'
        except (ValueError, TypeError):
            errors['year'] = 'Год должен быть числом'
    
    description = film_data.get('description', '').strip()
    if not description:
        errors['description'] = 'Описание обязательно для заполнения'
    elif len(description) > 2000:
        errors['description'] = f'Описание слишком длинное ({len(description)}/2000 символов)'
    
    return errors

@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    try:
        conn, cur = db_connect()
        cur.execute("SELECT * FROM films ORDER BY id;")
        films = cur.fetchall()
        db_close(conn, cur)
        
        result = []
        for film in films:
            result.append(dict(film))
        
        return jsonify(result)
    except Exception as e:
        print(f"Error fetching films: {e}")
        abort(500, description="Ошибка при получении данных из БД")

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    try:
        conn, cur = db_connect()
        cur.execute("SELECT * FROM films WHERE id = %s;", (id,))
        film = cur.fetchone()
        db_close(conn, cur)
        
        if not film:
            abort(404, description=f"Фильм с id {id} не найден")
        
        return jsonify(dict(film))
    except Exception as e:
        print(f"Error fetching film {id}: {e}")
        abort(500, description="Ошибка при получении данных из БД")

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    try:
        conn, cur = db_connect()

        cur.execute("SELECT id FROM films WHERE id = %s;", (id,))
        if not cur.fetchone():
            db_close(conn, cur)
            abort(404, description=f"Фильм с id {id} не найден")
        
        cur.execute("DELETE FROM films WHERE id = %s;", (id,))
        db_close(conn, cur)
        
        return '', 204
    except Exception as e:
        print(f"Error deleting film {id}: {e}")
        abort(500, description="Ошибка при удалении данных из БД")

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    """Обновить фильм в БД"""
    try:
        film_data = request.get_json()
        
        if not film_data:
            abort(400, description="Отсутствуют данные для обновления")

        conn, cur = db_connect()
        cur.execute("SELECT id FROM films WHERE id = %s;", (id,))
        if not cur.fetchone():
            db_close(conn, cur)
            abort(404, description=f"Фильм с id {id} не найден")

        if not film_data.get('title', '').strip() and film_data.get('title_ru', '').strip():
            film_data['title'] = film_data['title_ru']

        errors = validate_film_data(film_data, is_update=True)
        if errors:
            db_close(conn, cur)
            return jsonify(errors), 400
        
        cur.execute("""
            UPDATE films 
            SET title = %s, title_ru = %s, year = %s, description = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING *;
        """, (
            film_data.get('title', ''),
            film_data.get('title_ru', ''),
            film_data.get('year'),
            film_data.get('description', ''),
            id
        ))
        
        updated_film = cur.fetchone()
        db_close(conn, cur)
        
        return jsonify(dict(updated_film))
    except Exception as e:
        print(f"Error updating film {id}: {e}")
        abort(500, description="Ошибка при обновлении данных в БД")

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    """Добавить новый фильм в БД"""
    try:
        film_data = request.get_json()
        
        if not film_data:
            abort(400, description="Отсутствуют данные для создания нового фильма")

        if not film_data.get('title', '').strip() and film_data.get('title_ru', '').strip():
            film_data['title'] = film_data['title_ru']
        
        errors = validate_film_data(film_data)
        if errors:
            return jsonify(errors), 400
        
        conn, cur = db_connect()
        cur.execute("""
            INSERT INTO films (title, title_ru, year, description) 
            VALUES (%s, %s, %s, %s)
            RETURNING *;
        """, (
            film_data.get('title', ''),
            film_data.get('title_ru', ''),
            film_data.get('year'),
            film_data.get('description', '')
        ))
        
        new_film = cur.fetchone()
        db_close(conn, cur)
        
        return jsonify(dict(new_film)), 201
    except Exception as e:
        print(f"Error adding film: {e}")
        abort(500, description="Ошибка при добавлении данных в БД")

if __name__ == "__main__":
    init_films_table()