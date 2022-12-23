from flask import Flask, request, render_template, redirect, url_for, make_response
from datetime import datetime
import sqlite3

app = Flask(__name__)

def update_db(db_data,action): 
    con = sqlite3.connect('mylar.db')
    cur = con.cursor()
    # TODO: Remove this to make less calls in the future. Add to init script.
    q = "CREATE TABLE IF NOT EXISTS entries (id INT, title TEXT)"
    cur.execute(q)
    con.commit()
    if action == 'add':
        q = "INSERT INTO entries (id, title) VALUES (%s,'%s')" % (db_data['entry_id'], db_data['entry_title'])
    elif action == 'edit':
        q = "UPDATE entries SET id=%s, title='%s' WHERE id=%s" % (db_data['entry_id'], db_data['entry_title'], db_data['entry_id'])
    cur.execute(q)
    con.commit()
    con.close()

def query_db_entry(entry_id):
    con = sqlite3.connect('mylar.db')
    cur = con.cursor()
    q = "select * from entries where id=%s" % (entry_id)
    cur.execute(q)
    res = cur.fetchall()
    con.close()
    return res

def query_db_all():
    con = sqlite3.connect('mylar.db')
    cur = con.cursor()
    q = "select * from entries order by id ASC"
    cur.execute(q)
    res = cur.fetchall()
    con.close()
    return res

# ** ROUTES ** 

@app.route("/")
def show_root():
    user = request.cookies.get('user_name') 
    return render_template("index.html", user=user)

@app.route('/login', methods=['GET','POST'])
def login():
    user = request.cookies.get('user_name')
    if request.method == 'POST':
        form_data = request.form
        user = form_data['tb_user']
        res = make_response(redirect(url_for('show_root')))
        res.set_cookie('user_name',user)
        return res

    elif request.method == 'GET':
        print('En get')
        cookie_val = request.cookies.get('user_name')
        return render_template('login.html', user=user)

@app.route("/entries")
def show_entries():
    user = request.cookies.get('user_name') 
    res = query_db_all()
    return render_template('entries_view.html', user=user, res=res)

@app.route("/add", methods=["GET","POST"])
def add_title():
    user = request.cookies.get('user_name')
    if request.method == "GET":
        return render_template('add.html', user=user)
    elif request.method == "POST":
        form_data = request.form
        entry_id =  form_data['entry_id']
        entry_title = form_data['entry_title']
        db_data = {
            "entry_id": entry_id,
            "entry_title": entry_title
        }
        update_db(db_data, action="add")
        return render_template('add.html', user=user, msg="Data added successfully")

@app.route("/entry", methods=["GET"])
def show_entry():  
    user = request.cookies.get('user_name') 
    entry_id = request.args.get('id')
    if entry_id is None: 
        msg = "Error: No ID specified. Enter something like /entry?id=<ID>."
        return render_template('error.html', msg=msg, user=user)
    else:
        res = query_db_entry(entry_id)
        # Eval res
        if len(res) == 0:
            msg = "Error, no entry with that ID"
            return render_template('error.html', msg=msg, user=user)
        else:
            # return res saving this one for future api json response
            return render_template('entry_view.html', entry_id = res[0][0], entry_title = res[0][1], user=user)

@app.route("/edit", methods=["GET","POST"])
def edit_entry():
    user = request.cookies.get('user_name') 
    if request.method == "GET":
        entry_id = request.args.get('id')
        if entry_id is None:
            msg = "Error: No ID specified. Enter something like /edit?id=<ID>"
            return render_template('error.html', msg=msg, user=user)
        else:
            res = query_db_entry(entry_id)
            if len(res) == 0:
                msg = "Error, no entry with that ID"
                return render_template('error.html', msg=msg, user=user)
            else:
                return render_template('edit.html', entry_id = res[0][0], entry_title = res[0][1], user=user)
    elif request.method == "POST":
        form_data = request.form
        entry_id =  form_data['entry_id']
        entry_title = form_data['entry_title']
        db_data = {
            "entry_id": entry_id,
            "entry_title": entry_title
        }
        update_db(db_data, action="edit")
        return redirect('/entry?id=%s' % (entry_id))
        return render_template('entry_view.html', msg="Data updated successfully")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
