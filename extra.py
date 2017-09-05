import string
import re

def ap(text_line):

    # tp = "".join(c for c in lines[4] if c not in string.punctuation)
    # tp = lines[4].translate(None, string.punctuation)
    # new_text = r.sub(r"[^\w\s']", "", text_line)
    r = re.compile("[^\w\s']")
    new_text = r.sub("", text_line)
    tokenized_text = new_text.split(" ")
    # print tokenized_text
    return tokenized_text


fh = open("tp.txt","r")
lines = fh.read().split("\n")
print lines
for x in lines:
    print ap(x), "\n"
