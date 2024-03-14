from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__) # app is an object inheriting the functionalities from Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/todo_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure secret key
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('todo_items', lazy=True))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('todo_items', lazy=True))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    todo_id = db.Column(db.Integer, db.ForeignKey('todo_item.id'), nullable=False)
    todo_item = db.relationship('TodoItem', backref=db.backref('tags', lazy=True))

# Routes for CRUD operations
@app.route('/todos', methods=['GET'])
def get_todos():
    todos = TodoItem.query.all()
    todo_list = [{'id': todo.id, 'title': todo.title, 'description': todo.description,
                  'due_date': todo.due_date.isoformat() if todo.due_date else None,
                  'completed': todo.completed, 'user_id': todo.user_id, 'category_id': todo.category_id}
                 for todo in todos]
    return jsonify({'todos': todo_list})

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = TodoItem.query.get(todo_id)
    if todo:
        todo_data = {
            'id': todo.id,
            'title': todo.title,
            'description': todo.description,
            'due_date': todo.due_date.isoformat() if todo.due_date else None,
            'completed': todo.completed,
            'user_id': todo.user_id,
            'category_id': todo.category_id
        }
        return jsonify({'todo': todo_data})
    else:
        return jsonify({'error': 'Todo not found'}), 404

@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.json
    if 'title' not in data or 'user_id' not in data:
        return jsonify({'error': 'Title and user_id are required'}), 400

    new_todo = TodoItem(title=data['title'],
                        description=data.get('description'),
                        due_date=data.get('due_date'),
                        completed=data.get('completed', False),
                        user_id=data['user_id'],
                        category_id=data.get('category_id'))
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({'todo': {'id': new_todo.id, 'title': new_todo.title,
                             'description': new_todo.description,
                             'due_date': new_todo.due_date.isoformat() if new_todo.due_date else None,
                             'completed': new_todo.completed,
                             'user_id': new_todo.user_id,
                             'category_id': new_todo.category_id}}), 201

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = TodoItem.query.get(todo_id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    data = request.json
    if 'title' in data:
        todo.title = data['title']
    if 'description' in data:
        todo.description = data['description']
    if 'due_date' in data:
        todo.due_date = data['due_date']
    if 'completed' in data:
        todo.completed = data['completed']
    if 'category_id' in data:
        todo.category_id = data['category_id']

    db.session.commit()

    todo_data = {
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'due_date': todo.due_date.isoformat() if todo.due_date else None,
        'completed': todo.completed,
        'user_id': todo.user_id,
        'category_id': todo.category_id
    }

    return jsonify({'todo': todo_data})

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = TodoItem.query.get(todo_id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    db.session.delete(todo)
    db.session.commit()

    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
