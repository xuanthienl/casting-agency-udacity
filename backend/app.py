import os
from flask import Flask, request, abort, jsonify, redirect, url_for
from sqlalchemy.orm.exc import NoResultFound
from flask_cors import CORS
from werkzeug.exceptions import NotFound
import requests
from dotenv import load_dotenv
from .database.models import setup_db, db, Movie, Actor, Casting
from .auth.auth import AuthError, requires_auth


def create_app(test_config=None):

    app = Flask(__name__, static_folder='../frontend/dist/', static_url_path='/')
    if test_config is not None:
        setup_db(app, test_config['database_path'])
    else:
        setup_db(app)
    CORS(app)

    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    API_AUDIENCE = os.getenv("API_AUDIENCE")

    #  ----------------------------------------------------------------
    #  Home
    #  ----------------------------------------------------------------

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return app.send_static_file("index.html")

    @app.errorhandler(NotFound)
    def not_found(error):
        return redirect(url_for('catch_all'))
    
    #  ----------------------------------------------------------------
    #  Log In
    #  ----------------------------------------------------------------
    
    @app.route('/login', methods=['POST'])
    def login():
        try:
            body = request.get_json()
            username = body.get('username')
            password = body.get('password')

            url = f'https://{AUTH0_DOMAIN}/oauth/token'
            payload = {
                "username":username,
                "password":password,
                "client_id":CLIENT_ID,
                "client_secret":CLIENT_SECRET,
                "audience":API_AUDIENCE,
                "grant_type":"password"
            }
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                response = response.json()
                return jsonify(
                    {
                        "success": True,
                        "data": {
                            "access_token": response.get('access_token'),
                            "expires_in": response.get('expires_in')
                        }
                    }
                )
            else:
                abort(422)
        except Exception as e:
            print(e)
            abort(500)

    #  ----------------------------------------------------------------
    #  CORS Headers
    #  ----------------------------------------------------------------

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response
    
    #  ----------------------------------------------------------------
    #  Movies
    #  ----------------------------------------------------------------

    # Read all movies
    @app.route("/movies", methods=["GET"])
    @requires_auth("get:movies")
    def readAllMovie(payload):
        try:
            movies = []
            
            results = Movie.query.all()
            for result in results:
                actors = []
                for casting in result.casting:
                    actors.append({
                        "id": casting.actor_id,
                        "name": casting.actor.name
                    })

                data = result.format()
                data["actors"] = actors

                movies.append(data)

            return jsonify(
                {
                    "success": True,
                    "data": movies
                }
            )
        except Exception as e:
            print(e)
            abort(500)

    # Add movies
    @app.route("/movies", methods=["POST"])
    @requires_auth("post:movies")
    def createMovie(payload):
        try:
            body = request.get_json()
            movie = Movie(
                title = body.get("title", None),
                release_date = body.get("release_date", None)
            )
            db.session.add(movie)
            db.session.commit()

            return jsonify({
                "success": True,
                "data": movie.format()
            })
        except Exception as e:
            db.session.rollback()
            print(e)
            abort(422)

    # Edit movies
    @app.route("/movies/<id>", methods=["PATCH"])
    @requires_auth("patch:movies")
    def updateMovie(payload, id):
        try:
            body = request.get_json()
            title = body.get("title", None)
            release_date = body.get("release_date", None)

            movie = Movie.query.filter(Movie.id == id).one()
            if title is not None:
                movie.title = title
            if release_date is not None:
                movie.release_date = release_date
            movie.verified = True
            db.session.commit()

            return jsonify({
                "success": True
            })
        except NoResultFound as e:
            print(e)
            raise NoResultFound
        except Exception as e:
            db.session.rollback()
            print(e)
            abort(422)

    # Delete movies
    @app.route("/movies/<id>", methods=["DELETE"])
    @requires_auth("delete:movies")
    def deleteMovie(payload, id):
        try:
            movie = Movie.query.filter(Movie.id == id).one()
            db.session.delete(movie)
            db.session.commit()

            return jsonify({
                "success": True
            })
        except NoResultFound as e:
            print(e)
            raise NoResultFound
        except Exception as e:
            db.session.rollback()
            print(e)
            abort(500)

    #  ----------------------------------------------------------------
    #  Actors
    #  ----------------------------------------------------------------

    # Read all actors
    @app.route("/actors", methods=["GET"])
    @requires_auth("get:actors")
    def readAllActor(payload):
        try:
            actors = []
            
            results = Actor.query.all()
            for result in results:
                movies = []
                for casting in result.casting:
                    movies.append({
                        "id": casting.movie_id,
                        "title": casting.movie.title
                    })

                data = result.format()
                data["movies"] = movies

                actors.append(data)
            
            return jsonify(
                {
                    "success": True,
                    "data": actors
                }
            )
        except Exception as e:
            print(e)
            abort(500)

    # Add actors
    @app.route("/actors", methods=["POST"])
    @requires_auth("post:actors")
    def createActor(payload):
        try:
            body = request.get_json()
            actor = Actor(
                name = body.get("name", None),
                age = body.get("age", None),
                gender = body.get("gender", None),
            )
            db.session.add(actor)
            db.session.commit()

            return jsonify({
                "success": True,
                "data": actor.format()
            })
        except Exception as e:
            db.session.rollback()
            print(e)
            abort(422)

    # Edit actors
    @app.route("/actors/<id>", methods=["PATCH"])
    @requires_auth("patch:actors")
    def updateActor(payload, id):
        try:
            body = request.get_json()
            name = body.get("name", None)
            age = body.get("age", None)
            gender = body.get("gender", None)

            actor = Actor.query.filter(Actor.id == id).one()
            if name is not None:
                actor.name = name
            if age is not None:
                actor.age = age
            if age is not None:
                actor.gender = gender
            actor.verified = True
            db.session.commit()

            return jsonify({
                "success": True
            })
        except NoResultFound as e:
            print(e)
            raise NoResultFound
        except Exception as e:
            print(e)
            db.session.rollback()
            abort(422)

    # Delete actors
    @app.route("/actors/<id>", methods=["DELETE"])
    @requires_auth("delete:actors")
    def deleteActor(payload, id):
        try:
            actor = Actor.query.filter(Actor.id == id).one()
            db.session.delete(actor)
            db.session.commit()

            return jsonify({
                "success": True
            })
        except NoResultFound as e:
            print(e)
            raise NoResultFound
        except Exception as e:
            db.session.rollback()
            print(e)
            abort(500)

    #  ----------------------------------------------------------------
    #  Casting
    #  ----------------------------------------------------------------

    # Add casting
    @app.route("/casting", methods=["POST"])
    @requires_auth("post:casting")
    def createCasting(payload):
        try:
            body = request.get_json()
            movie_id = body.get("movie", None)
            actor_id = body.get("actor", None)

            movie = Movie.query.filter(Movie.id == movie_id).one()
            actor = Actor.query.filter(Actor.id == actor_id).one()

            casting = Casting(
                movie_id = movie_id,
                actor_id = actor_id
            )
            db.session.add(casting)
            db.session.commit()

            return jsonify({
                "success": True
            })
        except NoResultFound as e:
            print(e)
            raise NoResultFound
        except Exception as e:
            db.session.rollback()
            print(e)
            abort(500)

    #  ----------------------------------------------------------------
    #  Errors
    #  ----------------------------------------------------------------

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "Bad Request"}),
            400
        )

    # @app.errorhandler(404)
    # def not_found(error):
    #     return (
    #         jsonify({"success": False, "error": 404, "message": "Not Found"}),
    #         404
    #     )

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return (
            jsonify({"success": False, "error": 422, "message": "Unprocessable Entity"}),
            422
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({"success": False, "error": 405, "message": "Method Not Allowed"}),
            405
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify({"success": False, "error": 500, "message": "Internal Server Error"}),
            500
        )
        
    @app.errorhandler(NoResultFound)
    def no_result_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "No Result Found"}),
            404
        )
    
    @app.errorhandler(AuthError)
    def auth_error(error):
        return (
            jsonify({"success": False, "error": error.status_code, "message": error.error['description']}),
            error.status_code
        )


    return app


app = create_app()

if __name__ == '__main__':
    app.run()
