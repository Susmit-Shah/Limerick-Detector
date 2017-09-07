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


def guess_syllables(word):
    vowels = ['a', 'e', 'i', 'o', 'u', 'y']
    s = 0
    for i in range(0, len(word)):
        if i == 0 and word[i] in vowels:
            s += 1
        elif word[i] in vowels and word[i-1] not in vowels:
            s += 1

    if word.endswith('le') and word[-3] not in vowels:
        s += 1

    elif word.endswith('e') and word[-2] not in vowels:
        s -= 1

    print word[-2]
    print word[-3]
    print s


fh = open("tp.txt","r")
lines = fh.read().split("\n")
print lines
guess_syllables('pronunciation')
#for x in lines:
    #print ap(x), "\n"
