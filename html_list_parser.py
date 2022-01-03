import nltk, re, pprint
from nltk import word_tokenize
from urllib import request
from bs4 import BeautifulSoup

VERBOSE = False
PRINT_ALL_SCRIPTS = False


#verbose print
def vprint(s):
    if VERBOSE:
        print(s)


def is_char(ch):
    if ch == ' ' or ch == '\n' or ch == '\r':
        return False
    return True


def is_all_caps(line):
    try:
        if line == "":
            return False
        for c in line:
            if c.islower():
                return False
        return True
    except:
        pass


def is_speech(i):
    global lines
    if i == 0 or lines[i].strip() == "":
        return False
    if (is_all_caps(lines[i - 1].strip()) and lines[i].strip()[0].islower()):
        return True
    if is_scene_changer(lines[i]):
        return False
    return is_speech(i - 1)


def remove_directions():
    global lines
    Min = 9999
    for i in range(len(lines)):
        if len(lines[i]) > 0:
            cnt = 0
            while cnt < len(lines[i]) and lines[i][cnt] == ' ':
                cnt += 1
            Min = min(cnt, Min)
    vprint('Min indentation in every line:' + str(Min))
    for i in range(len(lines)):
        if len(lines[i]) > 0:
            lines[i] = lines[i][Min:]

    direction_list = [
        'ROOFTOP', "OMITTED", 'Omitted', '(ECU)', "Shooting Script",
        "CONTINUED", 'BACK TO', 'CLOSE ON', 'DISSOLVE TO', 'ONSCREEN', 'FADE',
        'TO CAMERA', 'CLOSEUP', 'SUPERIMPOSE', '9/27/13', 'Revised', 'REVISED',
        'Revision', 'PAGES', 'SCREENPLAY', 'OMIT', 'SHOOTING SCRIPT',
        '"IN DARKNESS" SCRIPT', ' POV', ')B('
    ]

    for i, line in enumerate(lines):
        if len(line) > 0 and is_char(
                line[0]) and not is_speech(i) and not is_name(i):
            #lines[i] = ""
            pass
        else:
            for word in direction_list:
                if word in lines[i]:
                    lines[i] = ""

    vprint('Removing these directions:')
    INDENTATION_FOR_DIRECTION = 0
    for i in range(len(lines)):
        if lines[i] == '' or is_scene_changer(lines[i]):
            continue
        for j in range(INDENTATION_FOR_DIRECTION):
            if is_char(lines[i][j]):
                vprint(lines[i])
                lines[i] = ''
                break
    #1 if its direction,-1 otherwise
    global direction_ar

    direction_ar = [0] * (len(lines) + 10)
    vprint('Unconnected lines,possible directions:')
    for i in range(len(lines)):
        if check_prev_line(i):
            pass
    Min = 9999
    cnt_ar = [0] * 1005
    for i in range(len(lines)):
        if direction_ar[i] == 1 and len(lines[i]) > 0:
            cnt = 0
            while cnt < len(lines[i]) and lines[i][cnt] == ' ':
                cnt += 1
            #print('cnt',cnt)
            if cnt > 1000:
                cnt = 1000
            cnt_ar[cnt] += 1

    for i in range(25):
        if VERBOSE:
            print(i, cnt_ar[i], end=',')

    for i in range(len(lines)):
        if direction_ar[i] == 1:
            #print(lines[i])
            lines[i] = ''


def check_prev_line(i):
    global direction_ar
    global lines
    if i == 0 or lines[i] == '':
        #direction_ar[i] = -1
        return False
    #print(i)
    #print(i,direction_ar[i])
    if direction_ar[i] != 0:
        return direction_ar[i] == 1
    try:
        if is_scene_changer(lines[i]) or is_name(
                lines[i]) or lines[i].strip()[0] == '(':
            direction_ar[i] = -1
            return False
    except:
        print('=', repr(lines[i]), '=')

    if lines[i - 1] == '':
        direction_ar[i] = 1
        return True

    val = check_prev_line(i - 1)
    if val:
        direction_ar[i] = 1
    return val


def misintented_names():
    global lines
    for i in range(len(lines)):
        if len(lines[i]) > 0 and is_all_caps(
                lines[i]) and lines[i][0].isupper():
            if not is_scene_changer(lines[i]):
                vprint(lines[i])
                #print(lines[i+1])
                lines[i] = ""


def is_scene_changer(line):  #detect scene changer lines
    sc_list = [
        "EXT.", "INT.", "EXT ", "INT ", "INT:", "EXT:", "DECK ", "ROOM",
        "ELEVATOR", "ON THE ", "SLAM TO", "INT/EXT", "I/E.", "TITLE",
        'TRANSITION TO', 'LATER', 'NIGHT', 'THAT', 'APARTMENT', 'CUT TO',
        'INTERCUT', 'SCENE', 'SFX OVER', 'VFX:', 'DISSOLVE '
    ]
    for sc in sc_list:
        if (sc in line):
            return True

    return False


def is_name(name):
    if not is_all_caps(name):
        return False
    if is_scene_changer(name):
        return False
    if len(name) < 2:
        return False
    if name[-1] == '.':
        return False
    return True


def get_html(url):
    html = request.urlopen(url).read().decode('utf8', errors='ignore')
    if html.count('<pre>') != 1:
        print("WARNING: #of <pre>'s", html.count('<pre>'))
    html = html.split('<pre>')[-1].split('pre>')[0] + 'pre>'
    return html


def print_dialogues(movie_name, url):
    global lines
    MOVIE_NAME = movie_name
    to_be_printed = []
    discovery = 0
    vprint('# lines:' + str(len(lines)))
    for i, line in enumerate(lines):
        if (line.count("(") == 1):
            #print(line)
            if (is_all_caps(line)):
                continue
            if (line[0] == '(' and line[-1] == ')'
                    and line[1:10] == 'copyright'):
                continue
            if ("CONT'D" in line or "O.S." in line or "V.O" in line
                    or "MORE" in line):
                continue
            if is_scene_changer(line):
                continue
            #print(line)
            pre_emotion_empty_count = 0
            pre_step = 0
            pre_name_count = 0
            result = []
            while (i - pre_step >= 0
                   and (pre_name_count < 1 or len(lines[i - pre_step]) < 2
                        or not is_all_caps(lines[i - pre_step]))):
                if is_all_caps(
                        lines[i - pre_step]) and len(lines[i - pre_step]) > 0:
                    pre_name_count += 1
                pre_step += 1
            if (is_scene_changer(lines[i - pre_step])):
                result.append("")
                result.append("")
                result.append("")
                pre_step -= 1
                while (lines[i - pre_step] == ""):
                    pre_step -= 1

            post_emotion_empty_count = 0
            post_step = 0
            post_name_count = 0

            while i + post_step + 1 < len(lines) and (
                    post_name_count < 2 or len(lines[i + post_step]) < 2
                    or not is_all_caps(lines[i + post_step])):
                if len(lines) <= i + post_step or is_scene_changer(
                        lines[i + post_step]):
                    break
                if is_all_caps(lines[i + post_step]) and len(
                        lines[i + post_step]) > 0:
                    post_name_count += 1
                post_step += 1
            while is_scene_changer(lines[i + post_step]):
                post_step -= 1

            #print(lines[i-pre_step:i+post_step])
            #print(pre_step,post_step)
            printed_lines = lines[i - pre_step:i + post_step]

            for line_in_range in lines[i - pre_step:i + post_step]:
                if (line_in_range != ""
                        and not line_in_range[:-1].isnumeric()):
                    if (line_in_range != "(O.S.)"):
                        if (len(result) % 3 == 1 and result[-1][0] != '('
                                and line_in_range[0] != '('):
                            result.append("")
                        result.append(line_in_range)
            #print("=".join(result))
            name_utterance = []
            tmp_utterance = "%%%"
            for x in result:
                x = str(x)
                if (is_name(x)):
                    if (tmp_utterance != "%%%"):
                        name_utterance.append(tmp_utterance)
                    tmp_utterance = ""
                    name_utterance.append(x.strip())
                else:
                    if (x != ""):
                        tmp_utterance += " "
                    tmp_utterance += "" + x.strip()

            if (tmp_utterance != ""):
                name_utterance.append(tmp_utterance)
            #print("=".join(name_utterance))
            #out.write("\t".join(name_utterance)+"\n")
            if (len(name_utterance) <= 2 or '%%%' in name_utterance[0]):
                continue
            #print(name_utterance)
            clear_name_0 = name_utterance[0].split('(')[0].strip()
            clear_name_1 = name_utterance[2].split('(')[0].strip()
            if clear_name_0 == clear_name_1:
                #print("NOT a D:",name_utterance)
                continue

            while (len(name_utterance) < 8):
                name_utterance.append("")
            if '(' not in name_utterance[3] or ')' not in name_utterance[3]:
                continue
            label = name_utterance[3].split('(')[1].split(')')[0]
            name_utterance[3] = name_utterance[3].split(
                '(')[0] + name_utterance[3].split(')')[1]
            label = label.strip()
            if label == 'beat':
                continue
            dont_print = False
            for x in name_utterance:
                if "CONTINUED" in x or "INT." in x or "EXT." in x:
                    dont_print = True
            if not dont_print:
                to_be_printed.append(name_utterance + [MOVIE_NAME, label])
            #print("+".join(result))
            #out.write("\t".join(result)+"\n")
            #print(discovery,i)
            discovery += 1
            #if(discovery>50):
            #   break
        elif (line.count("(") > 2):
            print("Line {0} has more than one (", i)
    #check whether the movies is parsed well or not
    if len(to_be_printed) < 3:
        with open('Problem_movies.txt', 'a', encoding='utf-8') as pmovies:
            pmovies.write(movie_name + "\t" + url + '\n')
            print('PROBLEM in ', movie_name)
    else:
        with open('data/all_dialogues.txt', 'a', encoding='utf-8') as out:
            for i, l in enumerate(to_be_printed):
                if (i == len(to_be_printed) - 1
                        or not (l[0] == to_be_printed[i + 1][0]
                                and l[1] == to_be_printed[i + 1][1])):
                    out.write("\t".join(l) + "\n")
    #out.close()
    vprint(movie_name + 'DONE!')


def print_remaining():
    global lines
    for i, line in enumerate(lines):
        vprint(line)


def parse(movie_name, url):
    global lines

    #url = "http://www.imsdb.com/scripts/Ali.html"
    if url[-5:] != '.html':
        print(repr(url), repr(url[-5:]))
        return

    MOVIE_NAME = movie_name
    #print('Movie:',MOVIE_NAME)
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    print('MOVIE:', movie_name, 'URL:', url)
    vprint("You shouldn't see anything below here:")
    html_problem = 0
    for elem in soup.find_all('b'):
        try:
            line = str(elem).split('<b>')[1]
        except:
            vprint('exception:', elem)
            line = ""
        line = line.split('</b>')[0]
        if is_scene_changer(line):
            continue
        if not is_all_caps(elem):
            vprint(line)
            html_problem += 1
    if html_problem > 100:
        return
    vprint("You shouldn't see anything above here:")

    raw = soup.get_text()
    #print(html)
    raw = raw.replace('\r\n', '\n')
    raw = raw.replace('\r', '\n')
    lines = raw.split('\n')
    if (len(lines) < 10):
        return
    vprint(lines[:10])

    vprint('printing original..')
    reserved_chars = ["<", ">", ":", '"', "/", "\\", "|", "?", "*"]
    for ch in reserved_chars:
        MOVIE_NAME = MOVIE_NAME.replace(ch, '')

    if PRINT_ALL_SCRIPTS:
        with open(MOVIE_NAME + "_original.txt", "w", encoding='utf-8') as f:
            for i, line in enumerate(lines):
                f.write(lines[i] + '\n')

    for i, line in enumerate(lines):
        lines[i] = lines[i].replace("’", "'")
        lines[i] = lines[i].replace('(MORE)', '')  #replace all (MORE)
        lines[i] = lines[i].replace('EXT:',
                                    'EXT.')  # default is 'EXT.', not 'EXT:'
        lines[i] = lines[i].replace("cont'd", "CONT'D")
        lines[i] = lines[i].replace('(Cont.)', "(CONT'D)")

    vprint('-Those will be removed---------')
    misintented_names()
    vprint('-------------------------------')

    remove_directions()

    #remove tabs,(MORE),pagenumbers from text

    vprint("Modifing the file...")
    for i, line in enumerate(lines):
        lines[i] = lines[i].strip()
        if (lines[i] == ''):
            continue
        lines[i] = lines[i].replace(
            '\t', ' ')  #replace all tab characters with space

        if ("(CONT'D)" in lines[i] and lines[i][-8:] != "(CONT'D)"):
            #print(lines[i])
            cont_splitted = lines[i].split("(CONT'D)")
            lines[i] = cont_splitted[0]
            lines.insert(i + 1, "")
            lines.insert(i + 2, cont_splitted[1][1:])
            #fix?
    print_dialogues(movie_name, url)


with open('data/all_name_script.txt') as f:
    for line in f:
        if line == '':
            break
        line = line.strip()
        vprint('==============================')
        parse(*line.split('\t'))
        vprint('==============================')
