import docx2txt
def isAllCaps(line):
	for ch in line:
		if(ch.islower()):
			return False
	return True
my_text = docx2txt.process("Boyhood-screenplay-11-14-FINAL.docx")
lines = my_text.split('\n')
out = open("out.txt","w")
discovery = 1
for i,line in enumerate(lines):
	if('(' in line):
		if("CONT'D" not in line and "O.S." not in line and "V.O" not in line and "MORE" not in line):
			pre_emotion_empty_count = 0
			pre_step = 0
			pre_name_count = 0
#			while(pre_emotion_empty_count < 5):
#				if(lines[i-pre_step] == ""):
#					pre_emotion_empty_count+=1
#				pre_step+=1

			while(pre_name_count < 2 or len(lines[i - pre_step]) < 3 or  not  isAllCaps(lines[i-pre_step])):
				if isAllCaps(lines[i-pre_step]):
					pre_name_count += 1
				pre_step += 1

			post_emotion_empty_count = 0
			post_step = 0
			while(post_emotion_empty_count < 7):
				if(lines[i+post_step] == ""):
					post_emotion_empty_count+=1
				post_step+=1	

			data = []
			for line_in_range in lines[i-pre_step:i+post_step+1]:
				if(line_in_range!="" and not line_in_range[:-1].isnumeric()):
					if(line_in_range!="(O.S.)"):
						line_in_range = line_in_range.replace("\t"," ")
						data.append(line_in_range)
				# do something in scene starter?
				#if(line_in_range[0:4] == "INT."):
				#	data = []
			print(lines[i-pre_step:i+post_step+1])
			out.write("\t".join(data)+"\n")
			print(discovery,i)
			if(i == 3226):
				print(data)
			discovery+=1
			if(discovery>3):
				break
	elif(line.count("(")>2):
		print("Line {0} has more than one (",i)