import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

database_path = "{}://{}:{}@{}:{}/{}".format(
    os.getenv("DB_CONNECTION"),
    os.getenv("DB_USERNAME"),
    os.getenv("DB_PASSWORD"),
    os.getenv("DB_HOST"),
    os.getenv("DB_PORT"),
    os.getenv("DB_DATABASE")
)

# Deploy Heroku
database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    Migrate(app, db)

class Movie(db.Model):
    __tablename__ = 'Movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime)

    casting = db.relationship('Casting', backref='movie', lazy='joined', cascade="all, delete")

    def __repr__(self):
        return f"Movie(id={self.id}, title={self.title}, release_date={self.release_date})"
    
    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime("%Y-%m-%d")
        }

class Actor(db.Model):
    __tablename__ = 'Actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(50), nullable=False)

    casting = db.relationship('Casting', backref='actor', lazy='joined', cascade="all, delete")

    def __repr__(self):
        return f"Actor(id={self.id}, name={self.name}, fullname={self.age}, gender={self.gender})"
    
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

class Casting(db.Model):
    __tablename__ = 'Casting'

    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('Movie.id'), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('Actor.id'), nullable=False)

    def __repr__(self):
        return f"Casting(id={self.id}, movie_id={self.movie_id}, actor_id={self.actor_id})"
    
    def format(self):
        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'actor_id': self.actor_id
        }
