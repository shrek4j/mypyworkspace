from textteaser import TextTeaser
# article source: https://blogs.dropbox.com/developers/2015/03/limitations-of-the-get-method-in-http/
title = "the old man and the sea"
file = open("C:\\Users\\Administrator\\Desktop\\myfolder\\sea-and-adventures\\the-old-man-and-the-sea-3.txt")
text = file.read()

tt = TextTeaser()

sentences = tt.summarize(title, text,count=20)

for sentence in sentences:
  print sentence