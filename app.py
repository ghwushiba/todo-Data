from datetime import date, datetime
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# database configuration
app.config['SQLALCHEMY_TRACT_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)


class Todo(db.Model):
    # creating a table in db
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    date = db.Column(db.DateTime, default = datetime.utcnow)

@app.route("/")
def index():
   todo_list = Todo.query.all()
   return render_template('base.html', todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get('title')
    new_todo = Todo(title=title, complete = False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    # update an item
    todo = Todo.query.filter_by(id = todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo =Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/edit', methods=['POST'])
def edit():
    #to edit an item.
    newtitle=request.form.get('newtitle')
    oldtitle=request.form.get('oldtitle')
    todo=Todo.query.filter_by(title=oldtitle).first()
    todo.title=newtitle
    db.session.commit()
    return redirect('/')












if __name__ == "__main__":
    db.create_all()


    app.run(debug=True)