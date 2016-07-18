files = [28,29,30,34,35,36]
for i in files:
	with open(str(i) + ".txt", 'r', encoding='utf-8') as f:
		for line in f:
			content = line.replace(":", ": ")			
			# content = tmp[1:]

			wf = open("./output/" + str(i) + ".txt", "ab")
			# for item in content:
				# wf.write(item.encode('utf-8'))
			wf.write(content.encode('utf-8'))
			wf.closed
	f.closed 