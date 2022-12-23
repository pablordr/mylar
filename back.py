from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def show_root():
    return "this is /"

@app.route("/filewrite")
def file_write():
    f = open('file.txt','w')
    now = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    f.write(now)
    f.close()
    return "File Updated"
    
@app.route("/fileread")
def file_read():
    f = open('file.txt','r')
    s = f.readlines()[0]
    f.close()
    return s

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
