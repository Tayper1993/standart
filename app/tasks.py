from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from . import celery, db
from .models.transaction import Transaction


@celery.task
def check_transactions():
    with Session(db.engine) as session:
        transactions = session.query(Transaction).filter(Transaction.status == 'Wait').all()

        for transaction in transactions:
            if datetime.utcnow() - transaction.created_at > timedelta(minutes=15):
                transaction.status = 'Expired'
                session.add(transaction)
        session.commit()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, check_transactions.s(), name='Проверка транзакции каждую минуту')
