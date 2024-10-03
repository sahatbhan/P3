from sqlite3.dbapi2 import Error
from flask import Flask , render_template, request
import sqlite3
from flask import g
app=Flask(__name__)

DATABASE='/.users.db'

def get_db():
    db=getattr(g,'_database', None)
    if db is None:
        db=g._database=sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db=getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur=get_db().execute(query,args)
    rv=cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def valid_login(username,password):
    user=query_db('SELECT * FROM USER where Username=? anad password=?', (username,password))
    if user is None:
        return False
    else:
        return True

def log_the_user_in(username):
    return render_template('profile.html', username=username)
     

@app.route("/")
@app.route('/login' ,methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error='Invalid username/password'

    return render_template('login.html')

if __name__ =="__main__":
    app.run(debug=True)