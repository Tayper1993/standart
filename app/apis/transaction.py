from flask import render_template, redirect, url_for, flash, request, jsonify

from app import app, db
from app.forms import TransactionForm
from app.models.transaction import Transaction


@app.route('/transactions')
def transactions():
    """
    Получает список всех транзакций.

    ---
    responses:
      200:
        description: Успешный ответ html-шаблон со списком всех транзакций.
    """
    all_transactions = Transaction.query.all()
    return render_template('transactions.html', transactions=all_transactions)


@app.route('/transaction/view/<int:transaction_id>', methods=['GET', 'POST'])
def view_transaction(transaction_id):
    """
    Просматривает детали транзакции и обновляет её статус.

    ---
    parameters:
      - name: transaction_id
        in: path
        type: integer
        required: true
        description: Идентификатор транзакции, которую нужно просмотреть.
      - name: status
        in: formData
        type: string
        required: false
        description: Новый статус транзакции (только если транзакция в состоянии "Ожидание").
    responses:
      200:
        description: Успешный ответ с деталями транзакции.
        schema:
          type: object
          properties:
            id:
              type: integer
              description: Идентификатор транзакции.
            status:
              type: string
              description: Текущий статус транзакции.
      302:
        description: Успешное обновление статуса транзакции. Перенаправление на страницу транзакций.
      404:
        description: Транзакция не найдена. Перенаправление на список транзакций.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Сообщение об ошибке.
    """
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        flash('Транзакция не найдена')
        return redirect(url_for('list_transactions'))

    if request.method == 'POST':
        new_status = request.form.get('status')
        if transaction.status == 'Wait':
            transaction.status = new_status
            db.session.commit()
            flash('Статус транзакции успешно обновлен')
            return redirect(url_for('transactions'))
        else:
            flash('Транзакция не может быть обновлена, поскольку она не находится в состоянии "Ожидание"')

    return render_template('view_transaction.html', transaction=transaction)


@app.route('/transaction/create', methods=['GET', 'POST'])
def create_transaction():
    """
    Создает новую транзакцию.

    ---
    parameters:
      - name: amount
        in: formData
        type: number
        required: true
        description: Сумма транзакции.
      - name: commission
        in: formData
        type: number
        required: true
        description: Комиссия в процентах.
      - name: status
        in: formData
        type: string
        required: true
        description: Статус транзакции.
    responses:
      302:
        description: Успешное создание транзакции. Перенаправление на страницу транзакций.
      400:
        description: Ошибка валидации формы. Возвращает сообщение об ошибке.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Сообщение об ошибке.
    """
    form = TransactionForm()
    if form.validate_on_submit():
        new_transaction = Transaction(
            amount=round(form.amount.data * (1 + form.commission.data / 100), 2),
            commission=form.commission.data,
            status=form.status.data,
        )
        db.session.add(new_transaction)
        db.session.commit()
        flash('Транзакция создана')
        return redirect(url_for('transactions'))
    return render_template('transaction_create.html', form=form)


@app.route('/transaction/cancel/<int:transaction_id>', methods=['POST'])
def cancel_transaction(transaction_id):
    """
    Отменяет транзакцию по её идентификатору.

    ---
    parameters:
      - name: transaction_id
        in: path
        type: integer
        required: true
        description: Идентификатор транзакции, которую нужно отменить.
    responses:
      302:
        description: Успешное обновление статуса транзакции. Перенаправление на страницу транзакций.
      404:
        description: Транзакция не найдена. Перенаправление на список транзакций.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Сообщение об ошибке.
    """
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        flash('Транзакция не найдена')
        return redirect(url_for('list_transactions'))

    transaction.status = 'Cancelled'
    db.session.commit()
    flash('Статус транзакции успешно обновлен на "Отменена"')

    return redirect(url_for('transactions'))


@app.route('/transaction/status/<int:transaction_id>', methods=['GET'])
def check_transaction_status(transaction_id):
    """
    Проверяет статус транзакции по её идентификатору.

    ---
    parameters:
      - name: transaction_id
        in: path
        type: integer
        required: true
        description: Идентификатор транзакции, статус которой нужно проверить.
    responses:
      200:
        description: Успешный ответ с информацией о транзакции.
        schema:
          type: object
          properties:
            id:
              type: integer
              description: Идентификатор транзакции.
            status:
              type: string
              description: Статус транзакции.
      404:
        description: Транзакция не найдена.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Сообщение об ошибке.
    """
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        return jsonify({'error': 'Транзакция не найдена'}), 404

    return jsonify({'id': transaction.id, 'status': transaction.status}), 200
