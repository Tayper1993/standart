from flask import Blueprint
from sqlalchemy import true


usersbp = Blueprint('users', __name__)


@usersbp.cli.command('create-admin')
def create_admin() -> str:
    """
    Создаёт стандартного суперпользователя
    """
    from app import db
    from app.models.user import User

    admin = User(
        username='admin',
        password_hash='admin',
        balance='1000.0',
        commission_rate='0.05',
        webhook_url='https://example.com/',
        is_superuser=True,
    )

    existing_admin = User.query.filter_by(username='admin', is_superuser=true()).first()
    if existing_admin:
        return 'Стандартный администратор уже существует!'

    db.session.add(admin)
    db.session.commit()
    print('Стандартный администратор создан.')
