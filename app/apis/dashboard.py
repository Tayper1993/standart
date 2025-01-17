from datetime import datetime

from flask import render_template, jsonify

from app import app, db
from app.models.transaction import Transaction
from app.models.user import User


@app.route('/')
@app.route('/dashboard')
def dashboard():
    """
    Получает информацию для панели управления.

    ---
    responses:
      200:
        description: Успешный ответ с данными для панели управления.
        schema:
          type: object
          properties:
            total_users:
              type: integer
              description: Общее количество пользователей.
            total_transactions:
              type: integer
              description: Общее количество транзакций.
            total_amount_today:
              type: number
              description: Общая сумма транзакций за сегодня.
            recent_transactions:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: Идентификатор транзакции.
                  amount:
                    type: number
                    description: Сумма транзакции.
                  commission:
                    type: number
                    description: Комиссия в процентах.
                  status:
                    type: string
                    description: Статус транзакции.
                  created_at:
                    type: string
                    format: date-time
                    description: Дата и время создания транзакции.
    """
    total_users = User.query.count()
    total_transactions = Transaction.query.count()
    total_amount_today = db.session.query(db.func.sum(Transaction.amount)).filter(
        db.func.date(Transaction.created_at) == datetime.today().date()
    ).scalar() or 0
    recent_transactions = Transaction.query.order_by(Transaction.created_at.desc()).limit(5).all()

    return render_template(
        'dashboard.html',
        total_users=total_users,
        total_transactions=total_transactions,
        total_amount_today=total_amount_today,
        recent_transactions=recent_transactions,
    )

@app.route('/dashboard/data')
def dashboard_data():
    total_users = User.query.count()
    total_transactions = Transaction.query.count()
    total_amount_today = db.session.query(db.func.sum(Transaction.amount)).filter(
        db.func.date(Transaction.created_at) == datetime.today().date()
    ).scalar() or 0
    recent_transactions = Transaction.query.order_by(Transaction.created_at.desc()).limit(5).all()

    transactions_data = [
        {
            'id': transaction.id,
            'amount': transaction.amount,
            'status': transaction.status,
            'commission': transaction.commission,
            'created_at': transaction.created_at.isoformat(),
        }
        for transaction in recent_transactions
    ]

    return jsonify({
        'total_users': total_users,
        'total_transactions': total_transactions,
        'total_amount_today': total_amount_today,
        'recent_transactions': transactions_data,
    })

