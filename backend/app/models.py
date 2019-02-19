from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

db = SQLAlchemy()


class ValidationError(BaseException):
    def __init__(self, message: str):
        self.message = message


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __init__(self, *args, **kwargs):
        self._validate_data(*args, **kwargs)

    def _validate_data(self, *args, **kwargs):
        raise NotImplementedError

    def as_dict(self) -> dict:
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def update(self, *args, **kwargs) -> None:
        self._validate_data(*args, **kwargs)
        columns = inspect(self).mapper.column_attrs
        for key, value in kwargs.items():
            if key not in columns:
                raise TypeError(
                    f'Cannot update: {key} does not exist, check your '
                    f'_validate_data() method')
            setattr(self, key, value)


class Post(BaseModel):
    __tablename__ = 'posts'
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = kwargs['title']
        self.body = kwargs['body']

    def __repr__(self):
        return f'<Post (title: {self.title}, body: {self.body})>'

    def _validate_data(self, *args, **kwargs):
        if len(kwargs) != 2 or 'title' not in kwargs or 'body' not in kwargs:
            raise ValidationError('Wrong data')

        title = kwargs['title']
        body = kwargs['body']

        if type(title) is not str:
            raise ValidationError('Type of title is not str')

        if type(body) is not str:
            raise ValidationError('Type of body is not str')

        if title.strip() == '':
            raise ValidationError('Title is empty')

        if body.strip() == '':
            raise ValidationError('Body is empty')
