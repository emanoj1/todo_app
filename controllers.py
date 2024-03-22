from flask import jsonify, request
from models import db, User, TodoItem, Category, Tag

# Controller logic to fetch ALL todos
def get_todos():
    todos = TodoItem.query.all()
    todo_list = []
    for todo in todos:
        todo_data = {
            'id': todo.id,
            'title': todo.title,
            'description': todo.description,
            'due_date': todo.due_date.isoformat() if todo.due_date else None,
            'completed': todo.completed,
            'user_id': todo.user_id,
            'category_id': todo.category_id,
            'tags': [tag.name for tag in todo.tags]  # Include tags information
        }
        todo_list.append(todo_data)
    return jsonify({'todos': todo_list})

# Controller logic to fetch a SPECIFIC todo
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
            'category_id': todo.category_id,
            'tags': [tag.name for tag in todo.tags]  # Include tags information
        }
        return jsonify({'todo': todo_data})
    else:
        return jsonify({'error': 'Todo not found'}), 404

# Controller to Retrieve Todo Items by Tag
def get_todos_by_tag(tag_name):
    # Query the database to find the tag
    tag = Tag.query.filter_by(name=tag_name).all()
    if not tag:
        return jsonify({'error': 'Tag not found'}), 404

    # Managing multiple todos for a single tag
    for i in range(0, len(tag)):
        todo_id = tag[i].todo_id
        todo_details = TodoItem.query.filter_by(id=todo_id).all()
        print("todo_details", todo_details)

    # Serialize todo items
        todo_list = []
        for todo in todo_details:
            todo_data = {
            'id': todo.id,
            'title': todo.title,
            'description': todo.description,
            'due_date': todo.due_date.isoformat() if todo.due_date else None,
            'completed': todo.completed,
            'user_id': todo.user_id,
            'category_id': todo.category_id
        }
            todo_list.append(todo_data)

    return jsonify({'todos': todo_list})


# Controller logic to create a new todo
def create_todo():
    data = request.json
    if 'title' not in data or 'user_id' not in data:
        return jsonify({'error': 'Title and user_id are required'}), 400

    # Extract tags from data
    tags = data.get('tags', [])

    # Create a new ToDoItem object
    new_todo = TodoItem(title=data['title'],
                        description=data.get('description'),
                        due_date=data.get('due_date'),
                        completed=data.get('completed', False),
                        user_id=data['user_id'],
                        category_id=data.get('category_id'))

    # Add the new todo item to the database session
    db.session.add(new_todo)

    # Associate tags with the new todo item
    for tag_name in tags:
        # Check if the tag already exists in the database
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            # If the tag does not exist, create a new tag and associate it with the todo item
            tag = Tag(name=tag_name)
            db.session.add(tag)
            new_todo.tags.append(tag)
        else:
            # If the tag exists, associate it with the todo item
            new_todo.tags.append(tag)

    # Commit changes to the database
    db.session.commit()

    # Return the response with the created todo item and associated tags
    return jsonify({'todo': {'id': new_todo.id,
                             'title': new_todo.title,
                             'description': new_todo.description,
                             'due_date': new_todo.due_date.isoformat() if new_todo.due_date else None,
                             'completed': new_todo.completed,
                             'user_id': new_todo.user_id,
                             'category_id': new_todo.category_id,
                             'tags': [tag.name for tag in new_todo.tags]}}), 201


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
    if 'tags' in data:
        todo.tags = [] # Create an empty list
        for tag_name in data["tags"]:
            tag = Tag.query.filter_by(name = tag_name).first()
            if not tag:
                tag = Tag(name = tag_name)
                db.session.add(tag)
            tag.todo_id = todo.id
            todo.tags.append(tag)


    db.session.commit()

    todo_data = {
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'due_date': todo.due_date.isoformat() if todo.due_date else None,
        'completed': todo.completed,
        'user_id': todo.user_id,
        'category_id': todo.category_id,
        'tags': [tag.name for tag in todo.tags] 
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
