import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from app import create_app
from database.models import setup_db, Movie, Actor

load_dotenv()

class AppTestCase(unittest.TestCase):
    TOKEN = ''

    """This class represents the trivia test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        database_path = "{}://{}:{}@{}:{}/{}".format(
            os.getenv("DB_CONNECTION"),
            os.getenv("DB_USERNAME"),
            os.getenv("DB_PASSWORD"),
            os.getenv("DB_HOST"),
            os.getenv("DB_PORT"),
            os.getenv("DB_TEST_DATABASE")
        )
        # Deploy Heroku
        database_path = os.environ['DATABASE_URL']
        if database_path.startswith("postgres://"):
            database_path = database_path.replace("postgres://", "postgresql://", 1)
        
        test_config = {}
        test_config["database_path"] = database_path
        self.app = create_app(test_config)
        self.client = self.app.test_client

        if self.TOKEN == '':
            dataLogin = {
                "username": os.getenv("USERNAME"),
                "password": os.getenv("PASSWORD")
            }
            res = self.client().post("/login", json=dataLogin)
            data = json.loads(res.data)
            self.TOKEN = data["data"]["access_token"]

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_movies(self):
        headers = {'Authorization': f'Bearer {self.TOKEN}'}

        res = self.client().get("/movies", headers=headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    
    def test_add_movies(self):
        data = {
            "title":'Movies 01',
            "release_date":'2025-01-01'
        }
        headers = {'Authorization': f'Bearer {self.TOKEN}'}

        res = self.client().post("/movies", json=data, headers=headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    
    def test_422_for_add_movies(self):
        data = {
            "title":'Movies 01',
            "release_date":'2025-01-32'
        }
        headers = {'Authorization': f'Bearer {self.TOKEN}'}

        res = self.client().post("/movies", json=data, headers=headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 422)
        self.assertEqual(data["message"], "Unprocessable Entity")

    def test_update_movies(self):
        data = {
            "title":'Movies The First',
            "release_date":'2025-01-01'
        }
        headers = {'Authorization': f'Bearer {self.TOKEN}'}

        with self.app.app_context():
            movie = Movie.query.first()
        res = self.client().patch("/movies/" + str(movie.id), json=data, headers=headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_404_for_update_movies(self):
        data = {
            "title":'Movies The First',
            "release_date":'2025-01-01'
        }
        headers = {'Authorization': f'Bearer {self.TOKEN}'}

        res = self.client().patch("/movies/1000", json=data, headers=headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "No Result Found")

    def test_422_for_update_movies(self):
        data = {
            "title":'Movies The First',
            "release_date":'2025-01-32'
        }
        headers = {'Authorization': f'Bearer {self.TOKEN}'}

        with self.app.app_context():
            movie = Movie.query.first()
        res = self.client().patch("/movies/" + str(movie.id), json=data, headers=headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 422)
        self.assertEqual(data["message"], "Unprocessable Entity")

    def test_delete_movies(self):
        headers = {'Authorization': f'Bearer {self.TOKEN}'}

        with self.app.app_context():
            movie = Movie.query.first()
        res = self.client().delete("/movies/" + str(movie.id), headers=headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_404_for_delete_movies(self):
        headers = {'Authorization': f'Bearer {self.TOKEN}'}

        res = self.client().delete("/movies/1000", headers=headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "No Result Found")

    def test_get_all_actors(self):
        headers = {'Authorization': f'Bearer {self.TOKEN}'}

        res = self.client().get("/actors", headers=headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    
    def test_add_actors(self):
        data = {
            "name":"Actors 01",
            "age":"20",
            "gender":"male"
        }
        headers = {'Authorization': f'Bearer {self.TOKEN}'}

        res = self.client().post("/actors", json=data, headers=headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    
    def test_422_for_add_actors(self):
        data = {
            "name":"Actors 01",
            "age":"xxx",
            "gender":"male"
        }
        headers = {'Authorization': f'Bearer {self.TOKEN}'}

        res = self.client().post("/actors", json=data, headers=headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 422)
        self.assertEqual(data["message"], "Unprocessable Entity")

    def test_update_actors(self):
        data = {
            "name":"Actors The First",
            "age":"20",
            "gender":"male"
        }
        headers = {'Authorization': f'Bearer {self.TOKEN}'}

        with self.app.app_context():
            actors = Actor.query.first()
        res = self.client().patch("/actors/" + str(actors.id), json=data, headers=headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_404_for_update_actors(self):
        data = {
            "name":"Actors The First",
            "age":"20",
            "gender":"male"
        }
        headers = {'Authorization': f'Bearer {self.TOKEN}'}

        res = self.client().patch("/actors/1000", json=data, headers=headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "No Result Found")

    def test_422_for_update_actors(self):
        data = {
            "name":"Actors The First",
            "age":"xxx",
            "gender":"male"
        }
        headers = {'Authorization': f'Bearer {self.TOKEN}'}

        with self.app.app_context():
            actors = Actor.query.first()
        res = self.client().patch("/actors/" + str(actors.id), json=data, headers=headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 422)
        self.assertEqual(data["message"], "Unprocessable Entity")

    def test_delete_actors(self):
        headers = {'Authorization': f'Bearer {self.TOKEN}'}

        with self.app.app_context():
            actors = Actor.query.first()
        res = self.client().delete("/actors/" + str(actors.id), headers=headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_404_for_delete_movies(self):
        headers = {'Authorization': f'Bearer {self.TOKEN}'}

        res = self.client().delete("/actors/1000", headers=headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "No Result Found")

    def test_add_casting(self):
        with self.app.app_context():
            actors = Actor.query.first()
            movies = Movie.query.first()
        data = {
            "movie":movies.id,
            "actor":actors.id
        }
        headers = {'Authorization': f'Bearer {self.TOKEN}'}

        res = self.client().post("/casting", json=data, headers=headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_404_for_add_casting(self):
        data = {
            "movie":"1000",
            "actor":"1000"
        }
        headers = {'Authorization': f'Bearer {self.TOKEN}'}

        res = self.client().post("/casting", json=data, headers=headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "No Result Found")

if __name__ == "__main__":
    unittest.main()
