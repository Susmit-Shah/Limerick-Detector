import nltk
import sys
import re
import string
from nltk.tokenize import word_tokenize

cmu_dic = nltk.corpus.cmudict.dict()

'''for eachWord in dic:
    print eachWord + " : " + str(dic[eachWord])
'''

def syllable_counter(word):

    word = word.lower().strip()
    if word in cmu_dic.keys():
        # print cmu_dic[word]

        all_pronounciations = cmu_dic[word]         # list containing all pronounciation
        #print "All Pronouce : ", all_pronounciations
        min_syllable_count = sys.maxint
        for x in all_pronounciations:
            each = str(x)
            syllable_count = each.count('0') + each.count('1') + each.count('2')
            if syllable_count < min_syllable_count:
                min_syllable_count = syllable_count
                answer = x

        print "Answer :: ", answer
        print "Syllable :: ", min_syllable_count, "\n"
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
    num_syllables_list = []
    print(lines)
    if len(lines) < 5:
        print("Less than 5 lines.")
        return False
    else:
        for each_line in lines:
            tokenized_line = apostrophe_tokenize(each_line.strip(string.punctuation))
            tokenized_lines.append(tokenized_line)
        print("Hi", tokenized_lines)

        for each_line in tokenized_lines:
            count = 0
            for each_word in each_line:
                if each_word not in string.punctuation:
                    count += syllable_counter(each_word)
            num_syllables_list.append(count)
        print("Syllables List :: ", num_syllables_list)

        # Additionally, the following syllable constraints should be observed:
        # * No line should have fewer than 4 syllables
        if min(num_syllables_list) < 4:
            return False

        # * No two A lines should differ in their number of syllables by more than two.
        if abs(num_syllables_list[0] - num_syllables_list[1]) > 2 or abs(num_syllables_list[0] - num_syllables_list[4]) > 2 or abs(num_syllables_list[1] - num_syllables_list[4]) > 2:
            return False

        # * The B lines should differ in their number of syllables by no more than two.
        if abs(num_syllables_list[2] - num_syllables_list[3]) > 2:
            return False

        # * Each of the B lines should have fewer syllables than each of the A lines.
        min_of_A = min(num_syllables_list[0], num_syllables_list[1], num_syllables_list[4])
        print("Min of A :: ",  min_of_A)
        if num_syllables_list[2] > min_of_A or num_syllables_list[3] > min_of_A:
            return False

        if is_rhyme(tokenized_lines[0][-1], tokenized_lines[1][-1]) and \
                is_rhyme(tokenized_lines[2][-1], tokenized_lines[3][-1]) and \
                is_rhyme(tokenized_lines[1][-1], tokenized_lines[4][-1]) and not \
                is_rhyme(tokenized_lines[0][-1], tokenized_lines[2][-1]):
            print("It is a limerick")
            return True
        else:
            print("It is not a limerick")
            return False


def apostrophe_tokenize(text_line):

    r = re.compile("[^\w\s']")
    new_text = r.sub("", text_line)
    tokenized_text = new_text.split(" ")
    return tokenized_text

#print(syllable_counter("thrive  "))
#syllable_counter("impair")
#print(syllable_counter("fire"))

#print("Removed Consonent :: ", remove_consonent(cmu_dic["expire"][0]))
#is_rhyme("chime", "rhyme")
fh = open("tp.txt","r")
print(is_limerick(fh.read()))
#print(string.punctuation)