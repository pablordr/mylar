from flask import Flask, request, render_template, redirect
from datetime import datetime
import sqlite3

app = Flask(__name__)

def update_db(db_data):
    con = sqlite3.connect('mylar.db')
    cur = con.cursor()
    q = "CREATE TABLE IF NOT EXISTS entries (id INT, title TEXT)"
    cur.execute(q)
    con.commit()
    q = "INSERT INTO entries (id, title) VALUES (%s,'%s')" % (db_data['entry_id'], db_data['entry_title'])
    cur.execute(q)
    con.commit()
    con.close()

def query_db(entry_id):
    con = sqlite3.connect('mylar.db')
    cur = con.cursor()
    q = "SELECT * FROM entries WHERE id=%s" % (entry_id)
    cur.execute(q)
    res = cur.fetchall()
    con.close()
    return res

@app.route("/")
def show_root():
    return "this is /"

@app.route("/add", methods=["GET","POST"])
def add_title():
    if request.method == "GET":
        return render_template('add.html')
    elif request.method == "POST":
        form_data = request.form
        entry_id =  form_data['entry_id']
        entry_title = form_data['entry_title']
        db_data = {
            "entry_id": entry_id,
            "entry_title": entry_title
        }
        update_db(db_data)
        return render_template('add.html', msg="Data added successfully")

@app.route("/entry", methods=["GET"])
def show_entry():
    entry_id = request.args.get('id')
    if entry_id is None: 
        return "No ID specified"
    else:
        res = query_db(entry_id)
        # Eval res
        if len(res) == 0:
            msg = "Error, no entry with that ID"
            return render_template('error.html', msg = msg)
        else:
            # return res saving this one for future api json response
            return render_template('entry_view.html', entry_id = res[0][0], entry_title = res[0][1])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
