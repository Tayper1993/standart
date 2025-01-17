from flask import render_template, redirect, url_for, flash, request

from app import app, db
from app.forms import UserForm
from app.models.user import User


@app.route('/users')
def users():
    """
    Получает список всех пользователей.

    ---
    responses:
      200:
        description: Успешный ответ html-шаблон со списком пользователей.
    """
    all_users = User.query.all()
    return render_template('users.html', users=all_users)


@app.route('/user/create', methods=['GET', 'POST'])
def create_user():
    """
    Создает нового пользователя.

    ---
    parameters:
      - name: username
        in: formData
        type: string
        required: true
        description: Имя пользователя.
      - name: password
        in: formData
        type: string
        required: true
        description: Пароль пользователя.
      - name: webhook_url
        in: formData
        type: string
        required: false
        description: URL вебхука для пользователя.
    responses:
      302:
        description: Успешное создание пользователя. Перенаправление на страницу пользователей.
      400:
        description: Ошибка валидации формы. Возвращает сообщение об ошибке.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Сообщение об ошибке.
    """
    form = UserForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            webhook_url=form.webhook_url.data,
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Пользователь создан')
        return redirect(url_for('users'))
    return render_template('create_user.html', form=form)


@app.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    """
    Редактирует данные пользователя по его идентификатору.

    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: Идентификатор пользователя, данные которого нужно редактировать.
      - name: username
        in: formData
        type: string
        required: true
        description: Новое имя пользователя.
      - name: password
        in: formData
        type: string
        required: false
        description: Новый пароль пользователя (если требуется).
      - name: webhook_url
        in: formData
        type: string
        required: false
        description: Новый URL вебхука для пользователя.
    responses:
      302:
        description: Успешное обновление данных пользователя. Перенаправление на страницу пользователей.
      404:
        description: Пользователь не найден. Перенаправление на список пользователей.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Сообщение об ошибке.
    """
    user = User.query.get(user_id)
    if not user:
        flash('Пользователь не найден')
        return redirect(url_for('users'))

    if request.method == 'POST':
        user.username = request.form['username']
        user.webhook_url = request.form['webhook_url']
        if request.form['password']:
            user.set_password(request.form['password'])
        db.session.commit()
        flash('Данные успешно обновлены')
        return redirect(url_for('users'))

    return render_template('edit_user.html', user=user)


@app.route('/user/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """
    Удаляет пользователя по его идентификатору.

    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: Идентификатор пользователя, которого нужно удалить.
    responses:
      302:
        description: Успешное удаление пользователя. Перенаправление на страницу пользователей.
      404:
        description: Пользователь не найден. Перенаправление на список пользователей.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Сообщение об ошибке.
    """
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('Пользователь успешно удалён.')
    else:
        flash('Пользователь не найден')
    return redirect(url_for('users'))
