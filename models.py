from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user" #The table name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class TodoItem(db.Model):
    __tablename__="todo_items"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('todo_items', lazy=True))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('todo_items', lazy=True))
    tags = db.relationship('Tag', secondary='todo_tags', backref=db.backref('todos', lazy=True))

todo_tags = db.Table('todo_tags',
db.Column('todo_id', db.Integer, db.ForeignKey('todo_items.id'), primary_key=True),
db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)


class Category(db.Model):
    __tablename__="category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class Tag(db.Model):
    __tablename__="tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    todo_id = db.Column(db.Integer, db.ForeignKey('todo_items.id'), nullable=False)
    todo_item = db.relationship('TodoItem', backref=db.backref('tagged_items', lazy=True))