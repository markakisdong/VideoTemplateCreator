from flask import Flask, request, send_from_directory
from VideoTemplateCreator.main import *
import json
import pdb
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/video', methods=['POST'])
def video():
    adsjson = request.get_json()
    run(adsjson)
    return send_from_directory(directory=app.root_path, filename='holy.avi')

if __name__ == "__main__":
    app.run()
