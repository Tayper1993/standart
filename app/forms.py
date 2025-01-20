from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import FloatField
from wtforms.validators import DataRequired, Length


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=64)])
    password = PasswordField('Password', validators=[Length(min=6)])
    webhook_url = StringField('Webhook URL', validators=[DataRequired()])
    submit = SubmitField('Submit')


class TransactionForm(FlaskForm):
    amount = FloatField('Сумма', validators=[DataRequired()])
    commission = FloatField('Комиссия', validators=[DataRequired()])
    status = SelectField(
        'Статус',
        choices=[('Wait', 'Wait'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled'), ('Expired', 'Expired')],
        validators=[DataRequired()],
    )
    submit = SubmitField('Создать транзакцию')
