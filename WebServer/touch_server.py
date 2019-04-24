# import the nessecary pieces from Flask
from flask import Flask,render_template, request,jsonify,Response

#Create the app object that will route our calls
app = Flask(__name__)

@app.route('/')
def home():
	return render_template('touch_home.html')

@app.route('/', methods=['GET','POST']) 
def contact():
	print(request.method)
	if request.method == 'POST':
		if request.form['submit'] == 'submit':
			print("hello it's working") # do something

	elif request.method == 'GET':
		return render_template('touch_home.html', form=form)

"""def home():
    return render_template('touch_home.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text"""
# Add a single endpoint that we can use for testing
"""@app.route('/', methods = ['GET', 'POST'])
def home():
    #return '<h1> Hello World </h1><p>My name is Mani</p>'
    return render_template('touch_home.html')

@app.route('/parse_data', methods=['GET', 'POST'])
def parse_data(data):
    if request.method == "POST":
         #perform action here
         var value = $('.textbox').val();
		$.ajax({
  		type: 'POST',
  		url: "{{ url_for('parse_data') }}",
  		data: JSON.stringify(value),
  		contentType: 'application/json',
  		success: function(data){
  	  // do something with the received data
  }
});"""

#When run from command line, start the server
if __name__ == '__main__':
    app.run(host ='0.0.0.0', port = 3333, debug = True)
