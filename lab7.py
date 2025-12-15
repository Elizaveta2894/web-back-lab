from flask import Blueprint, render_template, request, jsonify, abort


lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html')


films = [
    {
        "title": "Avatar",
        "title_ru": "Аватар",
        "year": 2009,
        "description": """Бывший морпех Джейк Салли прикован к инвалидному креслу. Несмотря на немощное тело,
        Джейк в душе по-прежнему остается воином. Он получает задание совершить путешествие в несколько световых лет
        к базе землян на планете Пандора, где корпорации добывают редкий минерал, имеющий огромное значение для выхода
        Земли из энергетического кризиса.""",
    },
    {
        "title": "Greyhound",
        "title_ru": "Грейхаунд",
        "year": 2020,
        "description": """Февраль 1942 года, Северная Атлантика. Морской конвой с войсками и грузами для союзников под  
        патрулированием направляется в порт Ливерпуля. Войдя в недосягаемый для авиации сектор, известный как 
        «чёрная яма», суда подвергаются нападению группы немецких подлодок. Капитану головного эсминца «Грейхаунд» Эрнсту 
        Краузе, до этого не принимавшему участия в военных действиях, приходится руководить обороной и отбиваться от так 
        называемой «волчьей стаи».""",
    },
    {
        "title": "F1",
        "title_ru": "F1",
        "year": 2025,
        "description": """В 1990-х Сонни Хейс был восходящей звездой «Формулы-1», но после серьёзной аварии ушёл из большого 
        спорта. 30 лет спустя Сонни живёт в трейлере и зарабатывает участием в различных гонках и чемпионатах. Однажды к нему 
        обращается старый друг Рубен Сервантес, тоже в прошлом гонщик, а ныне владелец гоночной команды-аутсайдера, с просьбой 
        присоединиться к ним в качестве второго пилота и наставника для молодого многообещающего новичка.""",
    },
    {
        "title": "Demolition",
        "title_ru": "Разрушение",
        "year": 2015,
        "description": """Когда Дэвис узнал, что его жена умерла, он захотел купить шоколадные конфеты в торговом автомате, 
        но пачка застряла. Пытаясь выяснить, почему он ничего не чувствует по поводу смерти жены, Дэвис начинает писать длинные 
        письма в обслуживающую торговые автоматы фирму. А в письмах он рассказывает о себе и об отношениях с погибшей женой.
        Вскоре ему отвечает Карен, менеджер компании. Попутно Дэвис понимает, что ему совершенно необходимо разобрать холодильник, 
        разломать кабинку туалета, рабочий компьютер и разрушить собственный дом.""",
    },
    {
        "title": "Jungle",
        "title_ru": "Джунгли",
        "year": 2017,
        "description": """Группа друзей отправляется в непроходимые джунгли Боливии в поисках экзотических впечатлений. Однако когда 
        проводник исчезает и приятели остаются один на один с дикой природой, путешествие, начавшееся как забавное приключение, 
        превращается в борьбу за выживание.""",
    }
]


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404, description=f"Фильм с id {id} не найден")
    
    return jsonify(films[id])


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        abort(404, description=f"Фильм с id {id} не найден")
    
    del films[id]
    return '', 204


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        abort(404, description=f"Фильм с id {id} не найден")
    
    film = request.get_json()
    
    if not film:
        abort(400, description="Отсутствуют данные для обновления")
    
    if not film.get('title', '').strip() and film.get('title_ru', '').strip():
        film['title'] = film['title_ru']
    
    if film.get('description', '') == '':
        return {'description': 'Заполните описание'}, 400
    
    if not film.get('title', '').strip() and not film.get('title_ru', '').strip():
        return {'title_ru': 'Заполните хотя бы одно название'}, 400
    
    films[id] = film
    
    return jsonify(films[id])

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film_data = request.get_json()
    
    if not film_data:
        abort(400, description="Отсутствуют данные для создания нового фильма")

    if not film_data.get('title', '').strip() and film_data.get('title_ru', '').strip():
        film_data['title'] = film_data['title_ru']

    required_fields = ['title', 'title_ru', 'year', 'description']
    for field in required_fields:
        if field not in film_data:
            abort(400, description=f"Отсутствует обязательное поле: {field}")
    
    if film_data.get('description', '') == '':
        return {'description': 'Заполните описание'}, 400
    
    if not film_data.get('title', '').strip() and not film_data.get('title_ru', '').strip():
        return {'title_ru': 'Заполните хотя бы одно название'}, 400
    
    films.append(film_data)
    return jsonify({"id": len(films) - 1}), 201
