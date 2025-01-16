import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True, comment='Идентификатор')
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True, comment='Логин')
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256), comment='Хэш пароля')
    balance: so.Mapped[float | None] = so.mapped_column(sa.Float, default=0.0, comment='Баланс')
    commission_rate: so.Mapped[float | None] = so.mapped_column(sa.Float, default=0.0, comment='Ставка комиссии')
    webhook_url: so.Mapped[str | None] = so.mapped_column(sa.String(256), comment='URL webhook')
    is_superuser: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False, comment='Суперпользователь')

    def __repr__(self) -> str:
        return f'<User {self.id}, Balance: {self.balance}, Commission Rate: {self.commission_rate}>'

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
