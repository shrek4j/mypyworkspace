# -*- coding: utf-8 -*
import sys
import regex as re
reload(sys)
sys.setdefaultencoding('utf8')

filename = "C:\\Users\Administrator\\Desktop\youtube\\20180925\\HOW_TO_UNDERSTAND_YOUR_CAT_BETTER_English.srt"
newfilename = "C:\\Users\Administrator\\Desktop\youtube\\20180925\\HOW_TO_UNDERSTAND_YOUR_CAT_BETTER_English_handled.srt"
file1 = open(filename)
file2 = open(newfilename,'w')
lines = file1.read()
all = lines.splitlines()
for line in all:
    if re.match("^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$",line):
        time = line.replace(" ","").split("-->")[0]
        hmsn = time.split(",")
        hms = hmsn[0].split(":")
        newtime = int(hms[0])*3600 + int(hms[1])*60 + int(hms[2]) + int(hmsn[1])*0.001

        file2.write('\n')
        file2.write(str(newtime))
        file2.write("||||")
    elif re.match("^\d+$",line):
        pass
    else:
        file2.write(line+" ")

file1.close()
file2.close()