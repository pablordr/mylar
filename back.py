from flask import Flask, request, render_template, redirect, url_for, make_response
from datetime import datetime
import sqlite3
import os
import socket

app = Flask(__name__)

# ** HELPER FUNCTIONS **

def update_db(db_data,action):
    """ Updates DG either an INSERT or an UPDATE
        depends on 'action' parameter. Values:
        - add: it will insert db_data into the db.
        - edit: it will update db_data.
    """
    con = sqlite3.connect('mylar.db')
    cur = con.cursor()
    # TODO: Remove this to make less calls in the future. Add to init script.
    q = 'CREATE TABLE IF NOT EXISTS entries (id INT, title TEXT)'
    cur.execute(q)
    con.commit()
    if action == 'add':
        q = 'INSERT INTO entries (id, title) VALUES (%s,"%s")' % (db_data['entry_id'], db_data['entry_title'])
    elif action == 'edit':
        q = 'UPDATE entries SET id=%s, title="%s" WHERE id=%s' % (db_data['entry_id'], db_data['entry_title'], db_data['entry_id'])
    cur.execute(q)
    con.commit()
    con.close()

def query_db_entry(entry_id):
    con = sqlite3.connect('mylar.db')
    cur = con.cursor()
    q = 'select * from entries where id=%s' % (entry_id)
    cur.execute(q)
    res = cur.fetchall()
    con.close()
    return res

def query_db_all():
    con = sqlite3.connect('mylar.db')
    cur = con.cursor()
    q = 'select * from entries order by id ASC'
    cur.execute(q)
    res = cur.fetchall()
    con.close()
    return res

def get_telemetry():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return (local_ip,hostname)

# ** ROUTES ** 

@app.route('/')
def show_root():
    user = request.cookies.get('user_name') 
    return render_template('index.html', user=user, telemetry=get_telemetry())

@app.route('/login', methods=['GET','POST'])
def login():
    user = request.cookies.get('user_name')
    if request.method == 'POST':
        form_data = request.form
        user = form_data['tb_user']
        resp = make_response(redirect(url_for('show_root')))
        resp.set_cookie('user_name',user)
        return resp
    elif request.method == 'GET':
        cookie_val = request.cookies.get('user_name')
        return render_template('login.html', user=user, telemetry=get_telemetry())

@app.route('/entries')
def show_entries():
    user = request.cookies.get('user_name') 
    res = query_db_all()
    return render_template('entries_view.html', user=user, res=res, telemetry=get_telemetry())

@app.route('/add', methods=['GET','POST'])
def add_title():
    user = request.cookies.get('user_name')
    if request.method == 'GET':
        return render_template('add.html', user=user, telemetry=get_telemetry())
    elif request.method == 'POST':
        form_data = request.form
        entry_id =  form_data['entry_id']
        entry_title = form_data['entry_title']
        db_data = {
            'entry_id': entry_id,
            'entry_title': entry_title
        }
        update_db(db_data, action='add')
        return render_template('add.html', user=user, msg='Data added successfully')

@app.route('/entry', methods=['GET'])
def show_entry():  
    user = request.cookies.get('user_name') 
    entry_id = request.args.get('id')
    if entry_id is None: 
        msg = 'Error: No ID specified. Enter something like /entry?id=<ID>.'
        return render_template('error.html', msg=msg, user=user, telemetry=get_telemetry())
    else:
        res = query_db_entry(entry_id)
        if len(res) == 0:
            msg = 'Error, no entry with that ID'
            return render_template('error.html', msg=msg, user=user)
        else:
            return render_template('entry_view.html', entry_id = res[0][0], entry_title = res[0][1], user=user, telemetry=get_telemetry())

@app.route('/edit', methods=['GET','POST'])
def edit_entry():
    user = request.cookies.get('user_name') 
    if request.method == 'GET':
        entry_id = request.args.get('id')
        if entry_id is None:
            msg = 'Error: No ID specified. Enter something like /edit?id=<ID>.'
            return render_template('error.html', msg=msg, user=user, telemetry=get_telemetry())
        else:
            res = query_db_entry(entry_id)
            if len(res) == 0:
                msg = 'Error, no entry with that ID.'
                return render_template('error.html', msg=msg, user=user)
            else:
                return render_template('edit.html', entry_id = res[0][0], entry_title = res[0][1], user=user, telemetry=get_telemetry())
    elif request.method == 'POST':
        form_data = request.form
        entry_id =  form_data['entry_id']
        entry_title = form_data['entry_title']
        db_data = {
            'entry_id': entry_id,
            'entry_title': entry_title
        }
        update_db(db_data, action='edit')
        return render_template('entry_view.html', msg='Data updated successfully', entry_id=entry_id, entry_title=entry_title)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
