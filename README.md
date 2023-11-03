# Casting Agency Full Stack

## About the Stack

### Backend
[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend
[View the README.md within ./frontend for more details.](./frontend/README.md)

### Deploy to Heroku
1/ Copy package.json (Edit: "build": "cd frontend && npm run build",), requirements.txt to main Folder
2/ Create Procfile file with content: "web: gunicorn backend.app:app"
3/ git init
4/ heroku create casting-agency-group
5/ heroku git:remote -a casting-agency-group
6/ heroku buildpacks:add --index 1 heroku/nodejs
7/ heroku buildpacks:add --index 2 heroku/python
8/ heroku addons:create heroku-postgresql:mini
9/ heroku config --app casting-agency-group
10/ export DATABASE_URL=“”
11/ echo $DATABASE_URL
12/ git add .
13/ git commit -am 'Ready to deploy!'
14/ git push heroku main
Note: "npm run build" if change FrontEnd