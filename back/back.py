from flask import Flask, request
from helpers import *
import json

app = Flask(__name__)

@app.route('/entry', methods=['GET'])
def get_entry():
    entry_id = request.args.get('id')
    res  = query_db_entry(entry_id)
    json_res = json.dumps(res)
    return json_res

@app.route('/list', methods=['GET'])
def get_entry_list():
    # Different list options as url parameters
    # Ie: Order, filter, etc.
    res = query_db_all()
    json_res = json.dumps(res)
    return json_res

@app.route('/add', methods=['POST'])
def add_entry():
    form_data = request.form
    entry_id = form_data['entry_id']
    entry_title = form_data['entry_title']
    db_data = {
        'entry_id': entry_id,
        'entry_title': entry_title
    }
    update_db(db_data, action='add')
    msg = 'Entry with id %s successfully added' % (entry_id)
    return msg

@app.route('/edit', methods=['POST'])
def edit_entry():
    form_data = request.form
    entry_id = form_data['entry_id']
    entry_title = form_data['entry_title']
    db_data = {
        'entry_id': entry_id,
        'entry_title': entry_title
    }
    update_db(db_data, action='edit')
    msg = 'Entry with id %s successfully updated' % (entry_id)
    return msg

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
