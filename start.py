from flask import Flask, render_template, Markup, request, make_response
from pymongo import MongoClient
import datetime

app = Flask(__name__)

url = "doraemon.iis.sinica.edu.tw"
db_name = "emotion_push"	# name of the database
collection_name = "plan_b_evaluation"	# name of the table

client = MongoClient(url)
db = client[db_name]	# database
collection = db[collection_name]	# table

dialog = []		# store all the dialog in the list
user = {1:[2, 8, 14, 5, 17, 11], 2:[2, 9, 13, 5, 17, 11], 3:[3, 9, 15, 6, 18, 12],
        4:[3, 7, 14, 6, 18, 12], 5:[1, 8, 13, 4, 10, 16], 6:[1, 7, 15, 4, 10, 16],
        7:[19, 25, 35, 24, 30, 31], 8:[19, 25, 36, 23, 29, 31], 9:[20, 26, 22, 34, 28, 32],
        10:[20, 26, 22, 34, 28, 32], 11:[21, 27, 24, 29, 35, 33], 12:[21, 27, 23, 30, 36, 33],
        13:[1,6,9,12,13,14,18,19,21,24,25,28,30,32,33,34,35,36], 14:[1,6,9,12,13,14,18,19,21,24,25,28,30,32,33,34,35,36],
        15:[2,3,4,5,7,8,10,11,15,16,17,20,22,23,26,27,29,31], 16:[2,3,4,5,7,8,10,11,15,16,17,20,22,23,26,27,29,31]}	# record the user and the dialog they should evaluate
# user = {1: ["4","5","6","10"]}
# topic = {}	# store the dialog which the current user should evaluate
content = ""	# temperate store the dialog read from the file

def post(userid, dialog_id, answer, time):
	# create new post object
	post = {"userid": userid,	# the id of the user
	         "dialog_id": dialog_id,	# the number of the dialog
	         "answer": answer,
	         "submit_time": time}	# the answer
	
	# insert into collection
	#post_id = collect.insert_one(post3).inserted_id
	post_id = collection.insert_one(post) # insert a row.
	print (post_id) # if ObjectId('...') then successful!	

@app.route("/")
def index():	# get user id in this page
	return render_template('index.html')

@app.route("/<int:userid>")
def start(userid = None):	# render the first dialog to the user
	if userid:
		# get dialog topic for the user	
		collect = db['plan_b_conversation']	# table
		# index = 0
		'''
		for item in user[userid]:
			cursor = collect.find({'dialog_id': item}).sort("order",1)
			dialog = ""
			for document in cursor:
				speaker = document['speaker']
				dialog += speaker + ": " + document['content'].replace('\n', '</br>')
			
			# topic[index] = Markup(dialog)
			# index += 1
		'''
		cursor = collect.find({'dialog_id': user.get(userid)[0]}).sort("order",1)
		dialog = ""
		for document in cursor:
			speaker = document['speaker']
			dialog += speaker + ": " + document['content'].replace('\n', '</br>')		
		topic = Markup(dialog)
		# store the cookie
		resp = make_response(render_template('evaluate.html', number = 1, dialog = topic, userid = userid))
		resp.set_cookie('userid', str(userid))
		# resp.set_cookie('number', str(user[userid][0]))
		return resp
		# return render_template('evaluate.html', number = 1, dialog = topic[0])

@app.route('/next', methods=['POST'])
def next():
	form_id = int(request.form['id'])
	userid = int(request.cookies.get('userid'))
	dialog_id = user.get(userid)[form_id-1]
	
	next_dialog = user.get(userid)[form_id]
	collect = db['plan_b_conversation']
	cursor = collect.find({'dialog_id': next_dialog}).sort("order",1)
	dialog = ""
	for document in cursor:
		speaker = document['speaker']
		dialog += speaker + ": " + document['content'].replace('\n', '</br>')		
	topic = Markup(dialog)

	# get the answer
	q1 = request.form['q1']
	q2 = request.form['q2']
	q3 = request.form['q3']
	q4 = request.form['q4']
	q5 = request.form['q5']
	q6 = request.form['q6']
	q7 = request.form['q7']
	q8 = request.form['q8']
	q9 = request.form['q9']
	q10 = request.form['q10']	
	answer = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
	time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	post(userid, dialog_id, answer, time)
	
	return render_template('evaluate.html', number = form_id+1, dialog = topic, userid = userid)

@app.route('/submit', methods=['POST'])
def submit():
	form_id = int(request.form['id'])
	userid = int(request.cookies.get('userid'))
	dialog_id = user.get(userid)[form_id-1]
	
	q1 = request.form['q1']
	q2 = request.form['q2']
	q3 = request.form['q3']
	q4 = request.form['q4']	
	q5 = request.form['q5']
	q6 = request.form['q6']				
	q7 = request.form['q7']		
	q8 = request.form['q8']
	q9 = request.form['q9']
	q10 = request.form['q10']	
	answer = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
	time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	post(userid, dialog_id, answer, time)

	return render_template('submit.html')

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=2468)
