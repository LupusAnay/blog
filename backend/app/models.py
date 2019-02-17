from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def as_dict(self) -> dict:
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def update(self, data: dict) -> None:
        self.__dict__.update(data)


class Post(BaseModel):
    __tablename__ = 'posts'
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String)
