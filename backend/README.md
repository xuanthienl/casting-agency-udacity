Casting Agency - BackEnd
-----

## Development Setup

First, [install Python](https://www.python.org/downloads/) and [install PostgreSQL](https://www.postgresql.org/download/) if you haven't already.

To start and run the local development server,

1. Initialize and activate a virtual environment:

  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ python3 -m venv env
  $ source env/bin/activate
  ```

2. Install the dependencies:

  ```
  $ python3 -m pip install --upgrade pip
  $ python3 -m pip install -r requirements.txt
  ```

3. Configuration Keys "SQLALCHEMY_DATABASE_URI" (YOUR_PROJECT_DIRECTORY_PATH/config.py). Reference [connection URI format](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/#connection-uri-format)

4. Flask-Migrate:

  ```
  $ createdb -U postgres casting_agency
  $ chmod +x setup.sh
  $ source setup.sh
  $ flask db init
  $ flask db migrate
  $ flask db upgrade
  ```

5. Run the development server:

  ```
  $ flask --app app run
  ```

  /

  ```
  $ set FLASK_APP=app
  $ flask run
  ```

6. Verify on the Browser

  Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) 

7. Test API

  $ cd backend
  $ source setup.sh
  $ python3 test_app.py
