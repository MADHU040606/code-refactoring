from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route("/")
def home():
    """
    Render the homepage and display all tasks in the to-do list.
    """
    # Fetch all tasks from the database
    todo_list = Todo.query.all()
    
    # Render the 'base.html' template and pass the list of tasks
    return render_template("base.html", todo_list=todo_list)



@app.route("/add", methods=["POST"])
def add_task():
    """
    Add a new task to the to-do list.
    """
    # Get the task title from the form input
    task_title = request.form.get("title")
    
    # Create a new Todo object with the task title
    new_task = Todo(title=task_title, complete=False)
    
    # Add the new task to the database and commit changes
    db.session.add(new_task)
    db.session.commit()
    
    # Redirect back to the homepage
    return redirect(url_for("home"))


@app.route("/update/<int:task_id>")
def toggle_task_completion(task_id):
    """
    Toggle the completion status of a task by its ID.
    """
    # Fetch the task from the database using its ID
    task = Todo.query.get(task_id)
    
    # Toggle the completion status
    task.complete = not task.complete
    
    # Commit changes to the database
    db.session.commit()
    
    # Redirect back to the homepage
    return redirect(url_for("home"))


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    """
    Delete a task from the to-do list by its ID.
    """
    # Fetch the task from the database using its ID
    task_to_delete = Todo.query.get(task_id)
    
    # Delete the task and commit changes to the database
    db.session.delete(task_to_delete)
    db.session.commit()
    
    # Redirect back to the homepage
    return redirect(url_for("home"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

