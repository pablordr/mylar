import sqlite3
import os
import socket

def update_db(db_data,action):
    """ Updates DG either an INSERT or an UPDATE
        depends on 'action' parameter. Values:
        - add: it will insert db_data into the db.
        - edit: it will update db_data.
    """
    con = sqlite3.connect('mylar.db')
    cur = con.cursor()
    # TODO: Remove this to make less calls in the future. Add to init script.
    q = 'CREATE TABLE IF NOT EXISTS entries (id INT PRIMARY KEY, title TEXT)'
    cur.execute(q)
    con.commit()
    if action == 'add':
        q = 'INSERT INTO entries (id, title) VALUES (%s,"%s")' % (db_data['entry_id'], db_data['entry_title'])
    elif action == 'edit':
        q = 'UPDATE entries SET title="%s" WHERE id=%s' % (db_data['entry_title'], db_data['entry_id'])
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