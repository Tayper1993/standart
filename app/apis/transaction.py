from flask import render_template, redirect, url_for, flash, request

from app import app, db
from app.models.transaction import Transaction


@app.route('/transactions')
def transactions():
    all_transactions = Transaction.query.all()
    return render_template('transactions.html', transactions=all_transactions)


@app.route('/transaction/view/<int:transaction_id>', methods=['GET', 'POST'])
def view_transaction(transaction_id):
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
