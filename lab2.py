from flask import Blueprint, render_template, request, redirect, url_for, abort
lab2= Blueprint('lab2', __name__)


@lab2.route('/lab2')
def lab2_main():
    return render_template('lab2_main.html')


@lab2.route('/lab2/a')
def a():
    return 'без слеша'


@lab2.route('/lab2/a/')
def a2():
    return 'со слешем'


flower_list = [
    {'name': 'роза', 'price': 300},
    {'name': 'тюльпан', 'price': 310},
    {'name': 'незабудка', 'price': 320},
    {'name': 'ромашка', 'price': 330},
    {'name': 'георгин', 'price': 300},
    {'name': 'гладиолус', 'price': 310}
]


@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list) or flower_id < 0:
        abort(404)
    else:
        flower = flower_list[flower_id]
        return render_template('flower_detail.html', 
                             flower_id=flower_id, 
                             flower=flower)


@lab2.route('/lab2/add_flower/', methods=['GET', 'POST'])
def add_flower():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        if name and price:
            flower_list.lab2end({'name': name, 'price': int(price)})
            return redirect('/lab2/all_flowers')
        else:
            return render_template('add_flower_form.html', error="Заполните все поля")
    
    return render_template('add_flower_form.html')


@lab2.route('/lab2/add_flower/<name>')
def add_flower_with_name(name):
    flower_list.lab2end({'name': name, 'price': 300}) 
    return redirect('/lab2/all_flowers')


@lab2.route('/lab2/all_flowers')
def all_flowers():
    return render_template('all_flowers.html', flower_list=flower_list)


@lab2.route('/lab2/del_flower/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id >= len(flower_list) or flower_id < 0:
        abort(404)
    flower_list.pop(flower_id)
    return redirect('/lab2/all_flowers')


@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return redirect('/lab2/all_flowers')


@lab2.route('/lab2/example')
def example():
    name, lab_num, group, course = 'Стабровская Лиза', 2, 'ФБИ-33',3
    fruits=[
        {'name': 'яблоки', 'price': 100}, 
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
        
    return render_template('example.html',
                            name=name, lab_num=lab_num,group=group,
                            course=course, fruits=fruits)


@lab2.route('/lab2/')
def lab2_2():
    return render_template('lab2.html')


@lab2.route('/lab2/filtres')
def filtres():
    phrase="О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)


@lab2.route('/lab2/calc/')
def calc_default():
    """Перенаправление на калькулятор с значениями по умолчанию"""
    return redirect('/lab2/calc/1/1')


@lab2.route('/lab2/calc/<int:a>')
def calc_single(a):
    """Перенаправление на калькулятор с одним числом и вторым по умолчанию"""
    return redirect(f'/lab2/calc/{a}/1')


@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    operations = {
        'sum': a + b,
        'difference': a - b,
        'product': a * b,
        'quotient': a / b if b != 0 else 'Ошибка: деление на ноль',
        'power': a ** b
    }
    
    return render_template('calc.html', a=a, b=b, operations=operations)

books = [
    {'author': 'Фёдор Достоевский', 'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 671},
    {'author': 'Лев Толстой', 'title': 'Война и мир', 'genre': 'Роман-эпопея', 'pages': 1225},
    {'author': 'Антон Чехов', 'title': 'Рассказы', 'genre': 'Рассказ', 'pages': 320},
    {'author': 'Михаил Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Роман', 'pages': 480},
    {'author': 'Александр Пушкин', 'title': 'Евгений Онегин', 'genre': 'Роман в стихах', 'pages': 240},
    {'author': 'Николай Гоголь', 'title': 'Мёртвые души', 'genre': 'Поэма', 'pages': 352},
    {'author': 'Иван Тургенев', 'title': 'Отцы и дети', 'genre': 'Роман', 'pages': 288},
    {'author': 'Александр Островский', 'title': 'Гроза', 'genre': 'Драма', 'pages': 120},
    {'author': 'Михаил Лермонтов', 'title': 'Герой нашего времени', 'genre': 'Роман', 'pages': 224},
    {'author': 'Иван Гончаров', 'title': 'Обломов', 'genre': 'Роман', 'pages': 640},
    {'author': 'Александр Грибоедов', 'title': 'Горе от ума', 'genre': 'Комедия', 'pages': 160},
    {'author': 'Николай Лесков', 'title': 'Левша', 'genre': 'Повесть', 'pages': 96}
]


@lab2.route('/lab2/books')
def books_list():
    return render_template('books.html', books=books)

cats = [
    {
        'name': 'Такса',
        'image': 'a7675d70f12e9911ea69fe9666ceae42.jpg',
        'description': 'Милая сосиска.'
    },
    {
        'name': 'Пудель',
        'image': 'cc8658fbaa3f9622235a0e3be8759a29.jpg',
        'description': 'Белое облачко.'
    },
    {
        'name': 'Хаски',
        'image': '59cd46c3fa80363b2267f9b142b21301.jpg',
        'description': 'Разные глазки.'
    },
    {
        'name': 'Немецкая овчарка',
        'image': '2dc3c030431710c0eccf56c376376c2f.jpg',
        'description': 'Серьезная собака.'
    },
    {
        'name': 'Алабай',
        'image': '1f83db3c6aa33be78e996d717ec7ac2e.jpg',
        'description': 'Не люблю эту породу, покусали в детстве.'
    },
    {
        'name': 'Доберман',
        'image': '6766da6bba7e9db14e6d94e873276e6d.jpg',
        'description': 'Зверь, а не собака.'
    },
    {
        'name': 'Сиба-ину',
        'image': '5864bbc3fb2a2034a0c619d82427d31e.jpg',
        'description': 'Плачу как впервый раз, смотря "Хатико".'
    },
    {
        'name': 'Бульдог',
        'image': '0e80503c2a88ad187c1777875086ce74.jpg',
        'description': 'Похож на милую свинку.'
    },
    {
        'name': 'Шпиц',
        'image': '420ae034ee040ce2a5232e6cf845453b.jpg',
        'description': 'Собака истинных леди.'
    },
    {
        'name': 'Бишон фризе',
        'image': '8847d87ad716fcd9f8440ecdfccae916.jpg',
        'description': 'У меня моя краостка такой породы.'
    },
    {
        'name': 'Бобтейл',
        'image': '0011c5dd8b82085fcfcf2773da9e98ed.jpg',
        'description': 'Обладатель самой длинной челки.'
    },
    {
        'name': 'Спаниель',
        'image': '63a0d555b2dc45b7f200ef303ee44870.jpg',
        'description': 'Кудряшка Сью.'
    },
    {
        'name': 'Бирманский',
        'image': '5f5ac46a1738e48ca1c086e67fd52b3e.jpg',
        'description': 'Полудлинношёрстный кот с белыми "носочками" и голубыми глазами.'
    },
    {
        'name': 'Турецкий ван',
        'image': '4493397b1c48dfa5af562a9263bf2b74.jpg',
        'description': 'Порода, которая любит воду и имеет характерный красно-белый окрас.'
    },
    {
        'name': 'Египетский мау',
        'image': 'c66fa40e31beb6ff86abd5bce1cf5e71.jpg',
        'description': 'Единственная естественная порода с пятнистым окрасом.'
    },
    {
        'name': 'Тонкинский',
        'image': '8ee07b304e6dcfa26adea336bb50eefa.jpg',
        'description': 'Гибрид сиамской и бурманской пород с аквамариновыми глазами.'
    },
    {
        'name': 'Корат',
        'image': 'e1d36188aa88cba858b5e26b12072338.jpg',
        'description': 'Древняя порода из Таиланда с серебристо-голубой шерстью.'
    },
    {
        'name': 'Манчкин',
        'image': 'static/on.jpg',  # <- Исправлено: закрыты кавычки и добавлено расширение
        'description': 'Порода с короткими лапами и игривым характером.'
    },
    {
        'name': 'Девон-рекс',
        'image': 'd0d1069a1148c58fdf930a3f3f8f37d4.jpg',
        'description': 'Кот с волнистой шерстью, большими ушами и озорным характером.'
    },
    {
        'name': 'Сибирский',
        'image': 'acee46c88e8b3dad7dee4673204f97da.jpg',
        'description': 'Русская порода с густой шерстью и гипоаллергенными свойствами.'
    }  
]


@lab2.route('/lab2/catsanddog')
def cats_gallery():
    return render_template('catsanddog.html', cats=cats)


