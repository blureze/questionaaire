from flask import Flask, render_template, Markup, request, make_response
from pymongo import MongoClient

app = Flask(__name__)

url = "doraemon.iis.sinica.edu.tw"
db_name = "emotion_push"
collection_name = "log"	# need to change

client = MongoClient(url)
db = client[db_name]
collection = db[collection_name]

dialog = []
user = {1:[1,2], 2:[2,1]}
topic = {}
content = ""

with open('templates/test.txt', 'r', encoding='UTF-8') as f:
	for line in f:
		if line == "----\n":
			dialog.append(content)
			content = ""
		else:
			content += line.split('\n')[0] + '</br>'
	dialog.append(content)	# add the last dialog content
f.closed

@app.route("/<int:userid>")
def hello(userid = None):
	if userid:
		print(user[userid])

		# get dialog topic for the user
		
		index = 0
		for item in user[userid]:
			topic[index] = Markup(dialog[item-1])
			index += 1

		return render_template('evaluate.html', number = 1, dialog = topic[0])

@app.route('/next', methods=['POST'])
def next():
	form_id = int(request.form['id'])

	q1 = request.form['q1']
	q2 = request.form['q2']
	q3 = request.form['q3']
	q4 = request.form['q4']	
	q5 = request.form['q5']
	q6 = request.form['q6']				
	q7 = request.form['q7']				
	#self.collection.insert_one(data) # insert a row.
	#self.collection.find("MongoDB Query Language") # find specific rows according the query.

	print (q1, q2, q3, q4, q5, q6, q7)
	return render_template('evaluate.html', number = form_id+1, dialog = topic[form_id])

@app.route('/submit', methods=['POST'])
def submit():
	form_id = request.form['id']
	q1 = request.form['q1']
	q2 = request.form['q2']
	q3 = request.form['q3']
	q4 = request.form['q4']	
	q5 = request.form['q5']
	q6 = request.form['q6']				
	q7 = request.form['q7']		
	#self.collection.insert_one(data) # insert a row.
	#self.collection.find("MongoDB Query Language") # find specific rows according the query.

	print (q1, q2)
	return render_template('submit.html')

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='140.114.192.9', port=8080)