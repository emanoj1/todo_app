from flask import Blueprint

from controllers import get_todos, get_todo, create_todo, update_todo, delete_todo

todo_blueprint = Blueprint('todo', __name__, url_prefix='/api')

todo_blueprint.add_url_rule('/todos', methods=['GET'], view_func=get_todos)
todo_blueprint.add_url_rule('/todos/<int:todo_id>', methods=['GET'], view_func=get_todo)
todo_blueprint.add_url_rule('/todos', methods=['POST'], view_func=create_todo)
todo_blueprint.add_url_rule('/todos/<int:todo_id>', methods=['PUT'], view_func=update_todo)
todo_blueprint.add_url_rule('/todos/<int:todo_id>', methods=['DELETE'], view_func=delete_todo)