from flask import Flask
from models import db
from blueprints import todo_blueprint
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/todo_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(todo_blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)