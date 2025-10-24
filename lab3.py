from flask import Blueprint, render_template, url_for, request, make_response, redirect

lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')

    display_name = name if name else "Аноним"

    display_age = age if age else "не указан"
    
    return render_template('lab3/lab3.html', 
                         name=display_name, 
                         name_color=name_color,
                         age=display_age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')  
    if age == '': 
        errors['age'] = 'Заполните поле!'

    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')  
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price=0
    drink=request.args.get('drink')
    if drink=='cofee':
        price=120
    elif drink =='black-tea':
        price=80
    else:
        price=70

    if request.args.get('milk')=='on':
        price+=30
    if request.args.get('sugar')=='on':
        price+=10

    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = 0
    drink = request.args.get('drink')
    
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    
    if color or bg_color or font_size:
        resp = make_response(redirect('/lab3/settings'))
        if color: resp.set_cookie('color', color)
        if bg_color: resp.set_cookie('bg_color', bg_color)
        if font_size: resp.set_cookie('font_size', font_size)
        return resp
    
    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    font_size = request.cookies.get('font_size')
    return render_template('lab3/settings.html', color=color, bg_color=bg_color, font_size=font_size)


@lab3.route('/lab3/train', methods=['GET', 'POST'])
def train():
    errors = {}
    if request.method == 'POST':
        fio = request.form.get('fio')
        shelf = request.form.get('shelf')
        linen = request.form.get('linen')
        baggage = request.form.get('baggage')
        age = request.form.get('age')
        start = request.form.get('start')
        end = request.form.get('end')
        date = request.form.get('date')
        insurance = request.form.get('insurance')

        if not all([fio, shelf, age, start, end, date]):
            errors['form'] = 'Заполните все обязательные поля!'
        else:
            try:
                age = int(age)
                if not (1 <= age <= 120):
                    errors['age'] = 'Возраст должен быть от 1 до 120!'
            except ValueError:
                errors['age'] = 'Возраст должен быть числом!'

        if not errors:
            if age < 18:
                price = 700
                ticket_type = 'Детский билет'
            else:
                price = 1000
                ticket_type = 'Взрослый билет'

            if shelf in ['нижняя', 'нижняя боковая']:
                price += 100
            if linen == 'on':
                price += 75
            if baggage == 'on':
                price += 250
            if insurance == 'on':
                price += 150

            return render_template('lab3/train_ticket.html',
                                   fio=fio, shelf=shelf, start=start, end=end,
                                   date=date, age=age, price=price,
                                   ticket_type=ticket_type)

    return render_template('lab3/train_form.html', errors=errors)


@lab3.route('/lab3/settings_clear')
def settings_clear():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('bg_color')
    resp.delete_cookie('font_size')
    return resp

    
books_products = [
    {"name": "Война и мир", "price": 1200, "author": "Лев Толстой", "genre": "Роман-эпопея"},
    {"name": "Преступление и наказание", "price": 850, "author": "Фёдор Достоевский", "genre": "Роман"},
    {"name": "Мастер и Маргарита", "price": 950, "author": "Михаил Булгаков", "genre": "Роман"},
    {"name": "Евгений Онегин", "price": 600, "author": "Александр Пушкин", "genre": "Роман в стихах"},
    {"name": "Отцы и дети", "price": 750, "author": "Иван Тургенев", "genre": "Роман"},
    {"name": "Герой нашего времени", "price": 700, "author": "Михаил Лермонтов", "genre": "Роман"},
    {"name": "Мёртвые души", "price": 800, "author": "Николай Гоголь", "genre": "Поэма"},
    {"name": "Анна Каренина", "price": 1100, "author": "Лев Толстой", "genre": "Роман"},
    {"name": "Идиот", "price": 900, "author": "Фёдор Достоевский", "genre": "Роман"},
    {"name": "Братья Карамазовы", "price": 1300, "author": "Фёдор Достоевский", "genre": "Роман"},
    {"name": "Капитанская дочка", "price": 550, "author": "Александр Пушкин", "genre": "Повесть"},
    {"name": "Ревизор", "price": 500, "author": "Николай Гоголь", "genre": "Комедия"},
    {"name": "Горе от ума", "price": 480, "author": "Александр Грибоедов", "genre": "Комедия"},
    {"name": "Обломов", "price": 780, "author": "Иван Гончаров", "genre": "Роман"},
    {"name": "Гроза", "price": 450, "author": "Александр Островский", "genre": "Драма"},
    {"name": "Бесы", "price": 950, "author": "Фёдор Достоевский", "genre": "Роман"},
    {"name": "Дубровский", "price": 520, "author": "Александр Пушкин", "genre": "Повесть"},
    {"name": "Нос", "price": 400, "author": "Николай Гоголь", "genre": "Повесть"},
    {"name": "Шинель", "price": 420, "author": "Николай Гоголь", "genre": "Повесть"},
    {"name": "Станционный смотритель", "price": 380, "author": "Александр Пушкин", "genre": "Повесть"},
    {"name": "Бесприданница", "price": 470, "author": "Александр Островский", "genre": "Драма"},
    {"name": "Левша", "price": 430, "author": "Николай Лесков", "genre": "Повесть"},
    {"name": "Очарованный странник", "price": 680, "author": "Николай Лесков", "genre": "Повесть"},
    {"name": "Детство", "price": 590, "author": "Лев Толстой", "genre": "Повесть"},
    {"name": "Муму", "price": 350, "author": "Иван Тургенев", "genre": "Рассказ"}
]

@lab3.route("/lab3/books")
def books_page():
    min_price_all = min(b["price"] for b in books_products)
    max_price_all = max(b["price"] for b in books_products)
    min_price = request.args.get("min_price", request.cookies.get("min_price", ""))
    max_price = request.args.get("max_price", request.cookies.get("max_price", ""))

    if "reset" in request.args:
        resp = make_response(redirect("/lab3/books"))
        resp.delete_cookie("min_price")
        resp.delete_cookie("max_price")
        return resp

    filtered = books_products.copy()
    if min_price or max_price:
        try:
            min_p = int(min_price) if min_price else min_price_all
            max_p = int(max_price) if max_price else max_price_all

            if min_p > max_p:
                min_p, max_p = max_p, min_p

            filtered = [b for b in books_products if min_p <= b["price"] <= max_p]
        except ValueError:
            filtered = books_products

    resp = make_response(render_template(
        "lab3/books.html",
        books=filtered,
        min_price=min_price,
        max_price=max_price,
        min_price_all=min_price_all,
        max_price_all=max_price_all,
        count=len(filtered)
    ))

    if min_price or max_price:
        resp.set_cookie("min_price", min_price)
        resp.set_cookie("max_price", max_price)

    return resp
