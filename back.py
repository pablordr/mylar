from flask import Flask, request, render_template, redirect
from datetime import datetime

app = Flask(__name__)

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
        return render_template('add.html', msg="Data added successfully")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
