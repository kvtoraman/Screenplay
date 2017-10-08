import docx2txt
import string
def isAllCaps(line):
    for ch in line:
        if(ch.islower()):
            return False
    return True
def isAction(i,lines):
    #print("i-1,i-3=>",lines[i-1] , lines[i-2] , lines[i-3])
    if(lines[i] == ""):
        return False
    if(i+3>=len(lines)):
        return False
    if("--" in lines[i]):
        return False
    if lines[i][0].islower():
        return False
    if lines[i][-1] == '?':
        return False
    if(lines[i-1] == lines[i-2] == lines[i-3] == ""):
        if(lines[i+1] == lines[i+2] == lines[i+3] == ""):
            if(lines[i][1].islower()):
                if(lines[i-4] != "" and lines[i-4][0] == '('):
                    return False
                if(lines[i-4] == ""):
                    return True
                return True
    if "EXT." in lines[i-4] or "INT." in lines[i-4]:
        return True
    return False
def isName(name):
    if not isAllCaps(name):
        return False
    if "INT." in name or "EXT." in name:
        return False
    if len(name)<3:
        return False
    return True
#todo:checks whether the file has errors or not
def errorInFile(lines):
    for line in lines:
        if(bool("(" in line) != bool(")" in line)):
            pass
            #print("(" in line , ")" in line)
            #print(line)
            #return True
    return False

MOVIE_NAME = "FightBelle"
DOCX_NAME = "FightBelle"
my_text = docx2txt.process(DOCX_NAME +".docx")
lines = my_text.split('\n')
out = open(DOCX_NAME + "_out.txt","w")
txtfile = open(DOCX_NAME + "_modified.txt","w")
print("Movie:",MOVIE_NAME,"Screenplay:",DOCX_NAME)
discovery = 1
#remove tabs,(MORE),pagenumbers from text

if(errorInFile(lines)):
    print("ERROR IN FILE")
    exit(1)
print("Modifing the file...")
for i,line in enumerate(lines):
    lines[i] = lines[i].replace('\t',' ')#replace all tab characters with space
    lines[i] = lines[i].replace('(MORE)','')#replace all (MORE)
    if(2<=len(lines[i])<=5 and lines[i][-1] == '.' and  lines[i][:-1].isdigit()):#replace pagenumbers
        #print("page:",lines[i])
        lines[i] = ""
    if(lines[i] != "" and ')' in lines[i] and '(' not in lines[i]):#find parantheticals that occupy more than oneline,merge them
        open_id = i
        #print("=>",lines[i-1],lines[i])
        while('(' not in lines[open_id]):
            open_id -= 1
        new_line = lines[open_id]+" "+lines[i]
        #print(new_line)
        del lines[open_id:i+1]
        lines.insert(open_id,new_line)
        
        
test = 988
#print("%".join(lines[test-10:test+10]))
print("Remove unnecassary action(direction)s")
for i,line in enumerate(lines):
    #remove action(direction)'s and 3 '\n' after them
    if(isAction(i,lines)):
    #    print(i,line)
        del lines[i:i+4]
    #if i > 1000:
     #   break
#print modified file to check
for i,line in enumerate(lines):
    txtfile.write(line+"\n")
print("Parsing..")
for i,line in enumerate(lines):
    if('(' in line):
        if("CONT'D" not in line and "O.S." not in line and "V.O" not in line and "MORE" not in line):
            pre_emotion_empty_count = 0
            pre_step = 0
            pre_name_count = 0
            result = []
        
            while(pre_name_count < 1 or len(lines[i - pre_step]) < 3 or  not  isAllCaps(lines[i-pre_step])):
                if isAllCaps(lines[i-pre_step]) and len(lines[i-pre_step]) > 0:
                    pre_name_count += 1
                pre_step += 1
            if("INT." in lines[i-pre_step] or "EXT." in lines[i-pre_step]):
                result.append("")
                result.append("")
                result.append("")
                pre_step-=1
                while(lines[i-pre_step] == ""):
                    pre_step-=1
                
            post_emotion_empty_count = 0
            post_step = 0
            post_name_count = 0

            while(post_name_count < 2 or len(lines[i + post_step]) < 3 or  not  isAllCaps(lines[i+post_step]) ):
                if "EXT." in lines[i+post_step] or "INT." in lines[i+post_step] :
                    break
                if isAllCaps(lines[i+post_step]) and len(lines[i+post_step]) > 0:
                    post_name_count += 1
                post_step += 1
            while "EXT." in lines[i+post_step] or "INT." in lines[i+post_step]:
                post_step -=1
            
            #print(lines[i-pre_step:i+post_step])
            #print(pre_step,post_step)
            printed_lines = lines[i-pre_step:i+post_step]
            
            for line_in_range in lines[i-pre_step:i+post_step]:
                if(line_in_range!="" and not line_in_range[:-1].isnumeric()):
                    if(line_in_range!="(O.S.)"):
                        if(len(result)%3 == 1 and result[-1][0] != '(' and line_in_range[0]!='('):
                            result.append("")
                        result.append(line_in_range)
            name_utterance = []
            tmp_utterance = "%%%"
            for x in result:
                if(isName(x)):
                    if(tmp_utterance != "%%%"):
                        name_utterance.append(tmp_utterance)
                    tmp_utterance = ""
                    name_utterance.append(x)
                else:
                    tmp_utterance += x
                
            if(tmp_utterance != ""):
                name_utterance.append(tmp_utterance)
            #print("=".join(name_utterance))
            out.write("\t".join(name_utterance)+"\n")
            #print("+".join(result))
            #out.write("\t".join(result)+"\n")
            #print(discovery,i)
            discovery+=1
            #if(discovery>50):
             #   break
    elif(line.count("(")>2):
        print("Line {0} has more than one (",i)
print("Done")