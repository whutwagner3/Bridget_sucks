# import the nessecary pieces from Flask
from flask import Flask, render_template, request, jsonify, Response, url_for
import subprocess
import re
import webbrowser

# Create the app object that will route our calls
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('touch_home.html')


@app.route('/', methods=['GET', 'POST'])
def contact1():
    if request.method == 'POST':
        if request.form.get('submit') == 'submit':
            subprocess.call(['rm', '-f', '/graph_json_vars.json'])
            input_gene = re.sub(r"\s+", "", request.form.get('gene'))
            input_organism = request.form.get('organism')
            subprocess.call(['python3', 'gene_clumper.py', input_gene, input_organism])
            subprocess.call(['cp', './graph_json_vars.json', './WebServer/static/'])
            return render_template('results.html')


    elif request.method == 'GET':
        subprocess.call(['rm', '-f', './WebServer/static/graph_json_vars.json'])
        return render_template('touch_home.html')


@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        # print("hello")
        if request.form.get('home') == 'home':
            return render_template('touch_home.html')


# When run from command line, start the server
if __name__ == '__main__':
    webbrowser.open_new('http://0.0.0.0:3333/')
    app.run(host='0.0.0.0', port=3333, debug=True)
