from flask import Flask, request, send_file
from app import Project
api = Flask(__name__)

project = Project()

@api.route('/head')
def hello_world():
    print (request.args.get('dbname'))
    return str(project.head())

@api.route('/plot')
def get_plot():
    bytes_obj = project.plot()
    return send_file(bytes_obj,
                     attachment_filename='plot.png',
                     mimetype='image/png')