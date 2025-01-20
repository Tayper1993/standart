"""init

Revision ID: 799a723453bb
Revises:
Create Date: 2025-01-17 13:27:22.252621

"""
import sqlalchemy as sa
from alembic import op

from app.models import custom_choice


# revision identifiers, used by Alembic.
revision = '799a723453bb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'transaction',
        sa.Column('id', sa.Integer(), nullable=False, comment='Идентификатор'),
        sa.Column('amount', sa.Float(), nullable=False, comment='Сумма'),
        sa.Column('commission', sa.Float(), nullable=False, comment='Комиссия'),
        sa.Column(
            'status',
            custom_choice.ChoiceType(
                {'Wait': 'Wait', 'Confirmed': 'Confirmed', 'Cancelled': 'Cancelled', 'Expired': 'Expired'}
            ),
            nullable=False,
            comment='Статус',
        ),
        sa.Column('created_at', sa.DateTime(), nullable=True, comment='Время создания'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False, comment='Идентификатор'),
        sa.Column('username', sa.String(length=64), nullable=False, comment='Логин'),
        sa.Column('password_hash', sa.String(length=256), nullable=False, comment='Хэш пароля'),
        sa.Column('balance', sa.Float(), nullable=True, comment='Баланс'),
        sa.Column('commission_rate', sa.Float(), nullable=True, comment='Ставка комиссии'),
        sa.Column('webhook_url', sa.String(length=256), nullable=True, comment='URL webhook'),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, comment='Суперпользователь'),
        sa.PrimaryKeyConstraint('id'),
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))

    op.drop_table('user')
    op.drop_table('transaction')
    # ### end Alembic commands ###
