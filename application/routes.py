"""
Основной модуль веб-приложения на Flask, реализующий функционал блога.

Предоставляет интерфейс для просмотра статей, аутентификации пользователей,
создания, редактирования и удаления постов. Также включает функции для регистрации
пользователей и управления сессиями входа/выхода.
"""


from datetime import datetime
from flask import redirect, render_template, request, url_for, flash
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from application import app, db
from application.models import Article, Users


@app.route('/')
def index():
    """Отображает главную страницу."""
    return render_template("index.html")


@app.route('/posts')
def posts():
    """
    Отображает страницу со списком всех статей.
    
    Возвращает страницу с постами, отсортированными по дате публикации.
    """
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/user_posts')
@login_required
def user_posts():
    """
    Отображает страницу с постами текущего пользователя.
    
    Требует аутентификации. Возвращает страницу с постами, созданными текущим пользователем.
    """
    articles = Article.query.filter_by(user_id=int(current_user.get_id())).order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
@login_required
def posts_detail(id):
    """
    Отображает детальную страницу поста по его идентификатору.
    
    Требует аутентификации. Возвращает страницу детального просмотра статьи.
    """
    article = Article.query.filter_by(id=id).join(Users).add_columns(
        Article.id,
        Article.user_id,
        Article.title,
        Article.intro,
        Article.text,
        Article.date,
        Users.name,
        Users.email,
        Users.phone_number
    ).first_or_404()
    return render_template("post_detail.html", article=article, user_id=int(current_user.get_id()))


@app.route('/posts/<int:id>/delete')
@login_required
def posts_delete(id):
    """
    Удаляет пост по его идентификатору и перенаправляет на страницу со списком постов.
    
    Требует аутентификации. В случае успеха перенаправляет на '/posts'.
    """
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении статьи произошла ошибка"


@app.route('/posts/<int:id>/update', methods=['POST'])
@login_required
def create_update(id):
    """
    Обновляет пост по его идентификатору. Поддерживает GET для загрузки формы и POST для обновления данных.
    
    Требует аутентификации. Возвращает форму для редактирования поста при GET-запросе.
    При успешном POST-запросе обновляет пост и перенаправляет на '/posts'.
    """
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text'] 

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "Ошибка при попытке сохранить пост"
    else:
        return render_template("post_update.html", article=article)


@app.route('/create-article', methods=['POST', 'GET'])
@login_required
def create_article():
    """
    Создает новый пост. Поддерживает GET для загрузки формы и POST для создания данных.
    
    Требует аутентификации. Возвращает форму для создания нового поста при GET-з
    апросе. При успешном POST-запросе создаёт пост и перенаправляет на '/posts'.
    """
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(user_id=current_user.get_id(), title=title, intro=intro, text=text, date=datetime.utcnow())

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "Ошибка при попытке сохранить пост"
    else:
        return render_template("create_article.html")


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """
    Обрабатывает вход пользователя. Поддерживает GET для загрузки формы и POST для аутентификации
    При успешном входе перенаправляет на главную страницу, иначе возвращает на страницу входа с сообщением об ошибке.
    """
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = Users.query.filter_by(login=login).first()

        if user and check_password_hash(user.encrypted_password, password):
            login_user(user)
            flash('User in')

            return redirect('/')
        else:
            flash('Неверный пароль или логин')
    else:
        flash('Заполните поля логин и пароль')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Обрабатывает регистрацию нового пользователя. Поддерживает GET для загрузки формы и POST для регистрации.
    В случае успешной регистрации перенаправляет на страницу входа, иначе возвращает на страницу регистрации с сообщением об ошибке.
    """
    login = request.form.get('login')
    password = request.form.get('password')
    rpassword = request.form.get('repeat-password')
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone-number')

    if request.method == 'POST':
        if not (login or password or rpassword):
            flash('Заполните все поля!')
        elif password != rpassword:
            flash('Пароли не одинаковые')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = Users(login=login, encrypted_password=hash_pwd, name=name, email=email, phone_number=phone)
            
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login_page'))
            except:
                flash("Такой логин уже использован")
                
    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """
    Обрабатывает выход пользователя из системы.
    После выхода перенаправляет на главную страницу.
    """
    logout_user()
    return redirect('/')


@app.after_request
def redirect_to_signin(response):
    """
    Перенаправляет неаутентифицированных пользователей на страницу входа, если доступ требует аутентификации.
    """
    if response.status_code == 401:
        return redirect(url_for('login_page'))

    return response
