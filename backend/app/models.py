from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def as_dict(self) -> dict:
        result = self.__dict__
        result.pop('_sa_instance_state', None)
        return result

    def update(self, data: dict) -> None:
        self.__dict__.update(data)


class Post(BaseModel):
    __tablename__ = 'posts'
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String)
