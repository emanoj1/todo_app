import os
from flask import Flask
from models import db
from blueprints import todo_blueprint
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)

#configs
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY']=os.environ.get("JWT_SECRET_KEY")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)  # Example expiration time for access tokens

#connect libraries with flask app
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

app.register_blueprint(todo_blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)