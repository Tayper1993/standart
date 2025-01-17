from datetime import datetime

from flask import render_template

from app import app, db
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

    return render_template(
        'dashboard.html',
        total_users=total_users,
        total_transactions=total_transactions,
        total_amount_today=total_amount_today,
        recent_transactions=recent_transactions,
    )
