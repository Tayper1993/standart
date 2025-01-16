from datetime import datetime, timezone

import sqlalchemy as sa
import sqlalchemy.orm as so

from app import db

STATUSES = {
    'Ожидание': 'Ожидание',
    'Подтверждена': 'Подтверждена',
    'Отменена': 'Отменена',
    'Истекла': 'Истекла',
}


class Transaction(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True, comment='Идентификатор')
    amount: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False, comment='Сумма')
    commission: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False, comment='Комиссия')
    status: so.Mapped[str] = so.mapped_column(
        sa.String(12), default='Ожидание', server_default='Ожидание', comment='Статус')
    created_at: so.Mapped[datetime] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc), comment='Дата и время создания')

    def __repr__(self):
        return f'<Transaction: {self.id}, Amount: {self.amount}, Status: {self.status}, Created At: {self.created_at}>'
