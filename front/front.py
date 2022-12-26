from flask import Flask, request, render_template, redirect, url_for, make_response
from helpers import * 
import requests
import json
import os

API_ENDPOINT=os.environ.get("API_ENDPOINT")

app = Flask(__name__)

@app.route('/')
def show_root():
    user = request.cookies.get('user_name') 
    return render_template('index.html', user=user, telemetry=get_telemetry())

@app.route('/entry', methods=['GET'])
def show_entry():  
    user = request.cookies.get('user_name') 
    entry_id = request.args.get('id')
    if entry_id is None: 
        msg = 'Error: No ID specified. Enter something like /entry?id=<ID>.'
        return render_template('error.html', msg=msg, user=user, telemetry=get_telemetry())
    else:
        req_url = API_ENDPOINT + '/entry?id=%s' % (entry_id)
        res = requests.get(req_url)
        res_json = json.loads(res.content)
        if len(res_json) == 0:
            msg = 'Error, no entry with that ID'
            return render_template('error.html', msg=msg, user=user, telemetry=get_telemetry())
        else:
            return render_template('entry_view.html', entry_id = res_json[0][0], entry_title = res_json[0][1], user=user, telemetry=get_telemetry())
   
@app.route('/entries')
def show_entries():
    user = request.cookies.get('user_name') 
    req_url = API_ENDPOINT + '/list'
    res = requests.get(req_url)
    res_json = json.loads(res.content)
    return render_template('entries_view.html', user=user, res=res_json, telemetry=get_telemetry())
3
@app.route('/add', methods=['GET','POST'])
def add_title():
    user = request.cookies.get('user_name')
    if request.method == 'GET':
        return render_template('add.html', user=user, telemetry=get_telemetry())
    elif request.method == 'POST':
        req_url = API_ENDPOINT + '/add'
        form_data = request.form
        entry_id =  form_data['entry_id']
        entry_title = form_data['entry_title']
        data = {
            'entry_id': entry_id,
            'entry_title': entry_title
        }
        requests.request("POST", req_url, data=data)
        return render_template('add.html', user=user, msg='Data added successfully', telemetry=get_telemetry())

@app.route('/edit', methods=['GET','POST'])
def edit_entry():
    user = request.cookies.get('user_name') 
    if request.method == 'GET':
        entry_id = request.args.get('id')
        if entry_id is None:
            msg = 'Error: No ID specified. Enter something like /edit?id=<ID>.'
            return render_template('error.html', msg=msg, user=user, telemetry=get_telemetry())
        else:
            req_url = API_ENDPOINT + '/entry?id=%s' % (entry_id)
            res = requests.get(req_url)
            res_json = json.loads(res.content)
            if len(res_json) == 0:
                msg = 'Error, no entry with that ID.'
                return render_template('error.html', msg=msg, user=user, telemetry=get_telemetry())
            else:
                return render_template('edit.html', entry_id = res_json[0][0], entry_title = res_json[0][1], user=user, telemetry=get_telemetry())
    elif request.method == 'POST':
        req_url = API_ENDPOINT + '/edit'
        form_data = request.form
        entry_id =  form_data['entry_id']
        entry_title = form_data['entry_title']
        data = {
            'entry_id': entry_id,
            'entry_title': entry_title
        }
        requests.request("POST", req_url, data=data)
        return render_template('entry_view.html', msg='Data updated successfully', entry_id=entry_id, entry_title=entry_title, telemetry=get_telemetry())

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

