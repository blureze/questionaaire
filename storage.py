# -*- coding：utf-8 -*-
from pymongo import MongoClient

url = "doraemon.iis.sinica.edu.tw"
db_name = "emotion_push"	# name of the database
collection_name = "plan_b_conversation"	# name of the table

client = MongoClient(url)
db = client[db_name]	# database
collection = db[collection_name]	# table

def post(speaker, dialog_id, content, order):
	# create new post object
	post = {"speaker": speaker,	# the id of the user
	         "dialog_id": dialog_id,	# the id of the dialog
	         "content": content,
	         "order": order}	# the order of the sentence in the dialog
	
	# insert into collection
	#post_id = collect.insert_one(post3).inserted_id
	post_id = collection.insert_one(post) # insert a row.
	print (post_id) # if ObjectId('...') then successful!

for filename in range(1,37):
	with open("./conversation/" + str(filename) + ".txt", 'r', encoding='utf-8') as f:
		order = 0
		for line in f:
			tmp = line.split(": ")
			speaker = tmp[0]
			content = tmp[1]
			dialog_id = filename	# filename
			# emotion = "none"
			order += 1

			post(speaker, dialog_id, content, order)
	f.closed 
