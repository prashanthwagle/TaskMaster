from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
#Telling the location of our db
# /// is relative path //// is absolute

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

#Initialising the database
db=SQLAlchemy(app)

#Create a Model

# Class Todo is inheriting from db.Model
class Todo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Function returns string everytime we create a new element
    def __repr__(self):
        return '<Task %r>' % self.id



@app.route('/', methods=['GET', 'POST'])
def index():
    # requests variable contains info on the requests
    if request.method == 'POST':
        # collect the content id wala from the request variable
        task_content=request.form['content']
        #Create a new ToDo object (id will be set automatically)
        new_task = Todo(content=task_content)
        try:
            #Add it to database
            db.session.add(new_task)
            db.session.commit()
            #redirect and request to be imported
            return redirect('/')
        except:
            return 'Issue adding your task'

    else: 
        # Else you query all the tasks and order by date created
        tasks=Todo.query.order_by('date_created').all()
        return render_template('index.html',tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Unable to delete the task"

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task=Todo.query.get_or_404(id)

    if request.method == 'GET':
        print(task.content)
        return render_template('update.html', task=task)
    else:
        task.content=request.form['updated_content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error in updating'
        

if __name__ == '__main__':
    app.run(debug=True)