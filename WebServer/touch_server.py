# import the nessecary pieces from Flask
from flask import Flask,render_template, request,jsonify,Response
import subprocess
import re

#Create the app object that will route our calls
app = Flask(__name__)

@app.route('/')
def home():
	return render_template('touch_home.html')

@app.route('/', methods=['GET','POST']) 
def contact1():
	
	if request.method == 'POST':
		if request.form.get('submit') == 'submit':
			input_organism= re.sub(r"\s+","",request.form.get('organism'))
			input_gene= request.form.get('gene')
			subprocess.call(['echo', input_organism,input_gene])
			
			return render_template('results.html')
			

	elif request.method == 'GET':
		return render_template('touch_home.html')

@app.route('/results', methods=['GET', 'POST'])
def contact2():
	if request.method == 'POST':
		if request.form.get('home') == 'home':
			return render_template('touch_home.html')
			


#When run from command line, start the server
if __name__ == '__main__':
    app.run(host ='0.0.0.0', port = 3333, debug = True)
