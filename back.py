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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
