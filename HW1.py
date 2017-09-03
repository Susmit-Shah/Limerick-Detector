import nltk
import sys
from nltk.tokenize import word_tokenize

cmu_dic = nltk.corpus.cmudict.dict()

'''for eachWord in dic:
    print eachWord + " : " + str(dic[eachWord])
'''

def syllable_counter(word):

    word = word.lower().strip()
    value=1
    if word in cmu_dic.keys():
        # print cmu_dic[word]
        min_count_syllables = sys.maxint

        all_pronounciations = cmu_dic[word]         # list containing
        print "All Pronouce : ", all_pronounciations
        min_syllable_count = sys.maxint
        for x in all_pronounciations:
            each = str(x)
            syllable_count = each.count('0') + each.count('1') + each.count('2')
            if syllable_count < min_syllable_count:
                min_syllable_count = syllable_count
                answer = x

        print "Answer :: ", answer
        print "Syllable :: ", min_syllable_count
        return min_syllable_count
    else:
        print("Not Found")
        return 1

def remove_consonent(a):

    print(a)
    while a:
        x = str(a[0])
        if x.count('0') or x.count('1') or x.count('2'):
            print("BREAK")
            break
        else:
            print(x)
            a.pop(0)
    return a


def is_rhyme(a, b):

    a = a.strip()
    b = b.strip()
    if a in cmu_dic.keys() and b in cmu_dic.keys():
        a_all_pronounciations = cmu_dic[a]
        b_all_pronounciations = cmu_dic[b]
        print(a_all_pronounciations)
        print(b_all_pronounciations)
        for each_a in a_all_pronounciations:
            for each_b in b_all_pronounciations:
                a1 = remove_consonent(each_a)
                b1 = remove_consonent(each_b)

                # get min of a, b
                small, large = list, list
                if len(a1) < len(b1):
                    small = str(a1)
                    large = str(b1)
                else:
                    small = str(b1)
                    large = str(a1)
                print("S :: ", small)
                print("L :: ", large)
                #print("Small String :: ", set(small))
                #print("Large String :: ", set(large))
                # check if min is suffix of/ends with other
                if large.endswith(small[1:]):
                    print("Rhymes\n\n")
                    return True
                else:
                    print("Doesn't rhymes\n\n")
                    return False
                    #return False

    else:
        print("Not Found")
        return False


def is_limerick(text):

    lines = text.split("\n")
    tokenized_lines = []
    print(lines)
    if len(lines) < 5:
        print("Less than 5 lines.")
        return False
    else:
        for each_line in lines:
            tokenized_lines.append(word_tokenize(each_line.strip('.,')))
        print("Hi", tokenized_lines)

        if is_rhyme(tokenized_lines[0][-1], tokenized_lines[1][-1]) and \
                is_rhyme(tokenized_lines[2][-1], tokenized_lines[3][-1]) and \
                is_rhyme(tokenized_lines[1][-1], tokenized_lines[4][-1]):
            print("It is a limerick")
            return True
        else:
            print("It is not a limerick")
            return False

        # line1 = word_tokenize(lines[0])
        # line2 = word_tokenize(lines[1])
        # line3 = word_tokenize(lines[2].strip(',.'))
        # line4 = word_tokenize(lines[3])
        # line5 = word_tokenize(lines[4])
        # print(line1, line2, line3, line4, line5)


#print(syllable_counter("thrive  "))
#syllable_counter("impair")
#print(syllable_counter("fire"))

#print("Removed Consonent :: ", remove_consonent(cmu_dic["expire"][0]))
#is_rhyme("chime", "rhyme")
fh = open("tp.txt","r")
is_limerick(fh.read())
