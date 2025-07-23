from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": [
    "https://34.239.116.28"
]}})
# Use PostgreSQL if DATABASE_URL is provided, otherwise fall back to SQLite for local development
database_url = os.environ.get('DATABASE_URL')
if database_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'task': self.task,
            'completed': self.completed
        }

# Create tables
with app.app_context():
    db.create_all()

@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Test database connection
        db.session.execute(db.text('SELECT 1'))
        db_status = 'healthy'
    except Exception as e:
        db_status = f'unhealthy: {str(e)}'
    
    return jsonify({
        'status': 'healthy', 
        'service': 'todo-api',
        'database': db_status
    }), 200

@app.route('/api/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos]), 200

@app.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    if not data or 'task' not in data:
        return jsonify({'error': 'Task is required'}), 400
    
    todo = Todo(task=data['task'])
    db.session.add(todo)
    db.session.commit()
    
    return jsonify(todo.to_dict()), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    
    data = request.get_json()
    if 'completed' in data:
        todo.completed = data['completed']
    if 'task' in data:
        todo.task = data['task']
    
    db.session.commit()
    return jsonify(todo.to_dict())

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 