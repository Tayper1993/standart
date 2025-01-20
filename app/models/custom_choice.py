import sqlalchemy.types as types


class ChoiceType(types.TypeDecorator):
    impl = types.String

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super().__init__(**kw)

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return [k for k, v in self.choices.items() if v == value][0]

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return self.choices.get(value)
