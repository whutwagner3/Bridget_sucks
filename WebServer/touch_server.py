# import the nessecary pieces from Flask
from flask import Flask,render_template, request,jsonify,Response
import subprocess
import re
import webbrowser

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
			#subprocess.call(['python3', 'gene_clumper.py', input_organism, input_gene])
			
			return render_template('results.html')
			

	elif request.method == 'GET':
		return render_template('touch_home.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
	if request.method == 'POST':
		#print("hello")
		if request.form.get('home') == 'home':
			return render_template('touch_home.html')
			


#When run from command line, start the server
if __name__ == '__main__':
    webbrowser.open_new('http://0.0.0.0:3333/')
    app.run(host ='0.0.0.0', port = 3333, debug = True)
