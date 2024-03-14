from flask import jsonify, request
from models import db, User, TodoItem, Category, Tag

# Controller logic to fetch all todos
def get_todos():
    todos = TodoItem.query.all()
    todo_list = [{'id': todo.id, 'title': todo.title, 'description': todo.description,
                  'due_date': todo.due_date.isoformat() if todo.due_date else None,
                  'completed': todo.completed, 'user_id': todo.user_id, 'category_id': todo.category_id}
                 for todo in todos]
    return jsonify({'todos': todo_list})

# Controller logic to fetch a specific todo
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

    # Controller logic to create a new todo
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

    # Controller logic to update an existing todo
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

# Controller logic to delete an existing todo
def delete_todo(todo_id):
    todo = TodoItem.query.get(todo_id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    db.session.delete(todo)
    db.session.commit()

    return jsonify({'result': True})
