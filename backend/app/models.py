from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def as_dict(self) -> dict:
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def update(self, **kwargs) -> None:
        columns = inspect(self).mapper.column_attrs
        for key, value in kwargs.items():
            if key not in columns:
                raise ValidationError(f'Cannot update: {key} does not exist')
            setattr(self, key, value)


class ValidationError(BaseException):
    def __init__(self, message: str):
        self.message = message


class Post(BaseModel):
    __tablename__ = 'posts'
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String)

    def __init__(self, title: str, body: str, **kwargs):
        if kwargs:
            raise ValidationError('Unexpected arguments')

        if type(title) is not str:
            raise ValidationError('Type of title is not str')

        if type(body) is not str:
            raise ValidationError('Type of body is not str')

        if title.strip() == '':
            raise ValidationError('Title is empty')

        if body.strip() == '':
            raise ValidationError('Body is empty')

        self.title = title
        self.body = body

    def __repr__(self):
        return f'<Post (title: {self.title}, body: {self.body})>'
