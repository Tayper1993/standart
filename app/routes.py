from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.forms import UserForm

from datetime import datetime
from app.models.transaction import Transaction
from app.models.user import User


@app.route('/')
@app.route('/dashboard')
def dashboard():
    total_users = User.query.count()
    total_transactions = Transaction.query.count()
    total_amount_today = db.session.query(db.func.sum(Transaction.amount)).filter(
        db.func.date(Transaction.created_at) == datetime.today().date()
    ).scalar() or 0
    recent_transactions = Transaction.query.order_by(Transaction.created_at.desc()).limit(5).all()

    return render_template('dashboard.html', total_users=total_users, total_transactions=total_transactions,
                           total_amount_today=total_amount_today, recent_transactions=recent_transactions)


@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/transactions')
def transactions():
    transactions = Transaction.query.all()
    return render_template('transactions.html', transactions=transactions)


@app.route('/user/create', methods=['GET', 'POST'])
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully.')
        return redirect(url_for('users'))
    return render_template('create_user.html', form=form)


@app.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get(user_id)
    if not user:
        flash('User not found.')
        return redirect(url_for('users'))

    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        if request.form['password']:
            user.set_password(request.form['password'])  # Обновляем пароль, если он указан
        db.session.commit()
        flash('User updated successfully.')
        return redirect(url_for('users'))

    return render_template('edit_user.html', user=user)


@app.route('/user/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully.')
    else:
        flash('User not found.')
    return redirect(url_for('users'))


@app.route('/transaction/view/<int:transaction_id>', methods=['GET', 'POST'])
def view_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        flash('Transaction not found.')
        return redirect(url_for('transactions'))

    if request.method == 'POST':
        new_status = request.form.get('status')
        if transaction.status == 'pending':
            transaction.status = new_status
            db.session.commit()
            flash('Transaction status updated successfully.')
        else:
            flash('Transaction cannot be updated.')
        return redirect(url_for('transactions'))

    return render_template('view_transaction.html', transaction=transaction)
