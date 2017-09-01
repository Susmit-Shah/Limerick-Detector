import nltk
import sys
#from nltk.corpus.reader import cmudict

cmu_dic = nltk.corpus.cmudict.dict()

'''for eachWord in dic:
    print eachWord + " : " + str(dic[eachWord])
'''

def syllable_counter(word):

    word = word.lower()
    value=1
    if word in cmu_dic:
        # print cmu_dic[word]
        min_count_syllables = sys.maxint

        all_pronounciations = cmu_dic[word]         # list containing
        print "All Pronouce : ", all_pronounciations
        countmin=sys.maxint
        for x in all_pronounciations:
            count=len(x)
            if(countmin>count):
                countmin=count
                ans=str(x)
        value=ans.count('0')+ans.count('1')+ans.count('2')
    print value
    return value
        #for each_pronounciation in all_pronounciations:
        #     print(type(each_pronounciation))
        #     #count = 0
        #     #each_pronounciation_string = str(each_pronounciation)
        #     #count = each_pronounciation_string.count('0') + each_pronounciation_string.count('1') + each_pronounciation_string.count('2')
        #     #if count < min_count_syllables:
        #     #    min_count_syllables = count
        #
        #
        # """for each_pronounciation in all_pronounciations:
        #     count = 0
        #     each_pronounciation_string = str(each_pronounciation)
        #     count = each_pronounciation_string.count('0') + each_pronounciation_string.count('1') + each_pronounciation_string.count('2')
        #     if count < min_count_syllables:
        #         min_count_syllables = count"""
        #
        # print min_count_syllables

        #else:
        # Not found in dictionary
        #print("Not found in dictionary")


        #phonemes = str(data[0])
        #print phonemes

#syllable_counter("ice")
syllable_counter("Australia")
syllable_counter("Failure")