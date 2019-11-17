from flask import Flask
#from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import sql


app = Flask(__name__)
app.secret_key = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200))
    # set default time
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='todos')
    timestamp = db.Column(db.DateTime(timezone=True), default=sql.func.now())
    complete = db.Column(db.Boolean, default=False)

    def __repr__(self):
        # str.format() is much better than '% ()'
        return u'<ToDo , {0} , {1} , {2}, {3}>'.format(self.id, self.task, self.complete, self.user_id)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20))
    email = db.Column(db.String(20))

    def __repr__(self):
        return u'<user No:{0} , {1} , {2} , {3}>'.format(self.id, self.username, self.email, self.todos)


def test():
    ur = User(username='wtlab', password='wtlab123', email='wtlabu@nmit.ac.in')
    td = Todo(task='sos')
    print(ur)
    print(td)
    db.session.add(ur)
    db.session.add(td)
    td.user_id = 1
    print(ur)
    print(td)
    db.session.commit()
    print(ur)
    print(td)
    td.complete = True
    print(td)


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    print('rebuild database')
    test()