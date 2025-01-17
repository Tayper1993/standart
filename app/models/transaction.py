from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy import DateTime

from app import db
from app.models.custom_choice import ChoiceType


class Transaction(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True, comment='Идентификатор')
    amount: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False, comment='Сумма')
    commission: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False, comment='Комиссия')
    status: so.Mapped[str] = so.mapped_column(
        ChoiceType({"Wait": "Ожидание", "Confirmed": "Подтверждено", "Cancelled": "Отменена", "Expired": "Истекла"}),
        comment='Статус'
    )

    created_at = db.Column(DateTime, default=datetime.utcnow, comment='Время создания')

    def __repr__(self):
        return f'<Transaction: {self.id}, Amount: {self.amount}, Status: {self.status}>'
