#!/usr/bin/env python
import argparse
import sys
import codecs
if sys.version_info[0] == 2:
  from itertools import izip
else:
  izip = zip
from collections import defaultdict as dd
import re
import string
import os.path
import gzip
import tempfile
import shutil
import atexit

# Use word_tokenize to split raw text into words
from string import punctuation

import nltk
from nltk.tokenize import word_tokenize

scriptdir = os.path.dirname(os.path.abspath(__file__))

reader = codecs.getreader('utf8')
writer = codecs.getwriter('utf8')


def prepfile(fh, code):
  if type(fh) is str:
    fh = open(fh, code)
  ret = gzip.open(fh.name, code if code.endswith("t") else code+"t") if fh.name.endswith(".gz") else fh
  if sys.version_info[0] == 2:
    if code.startswith('r'):
      ret = reader(fh)
    elif code.startswith('w'):
      ret = writer(fh)
    else:
      sys.stderr.write("I didn't understand code "+code+"\n")
      sys.exit(1)
  return ret


def addonoffarg(parser, arg, dest=None, default=True, help="TODO"):
  ''' add the switches --arg and --no-arg that set parser.arg to true/false, respectively'''
  group = parser.add_mutually_exclusive_group()
  dest = arg if dest is None else dest
  group.add_argument('--%s' % arg, dest=dest, action='store_true', default=default, help=help)
  group.add_argument('--no-%s' % arg, dest=dest, action='store_false', default=default, help="See --%s" % arg)



class LimerickDetector:

    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        self._pronunciations = nltk.corpus.cmudict.dict()

    def num_syllables(self, word):
        """
        Returns the number of syllables in a word.  If there's more than one
        pronunciation, take the shorter one.  If there is no entry in the
        dictionary, return 1.
        """

        # TODO: provide an implementation!

        word = word.lower().strip()
        if word in self._pronunciations.keys():

            all_pronounciations = self._pronunciations[word]  # list containing all pronounciations
            # print "All Pronouce : ", all_pronounciations
            min_syllable_count = sys.maxint
            for each_pronounciation in all_pronounciations:
                each = str(each_pronounciation)
                syllable_count = each.count('0') + each.count('1') + each.count('2')
                if syllable_count < min_syllable_count:
                    min_syllable_count = syllable_count
                    selected_pronounciation = each_pronounciation

            #print "Selected Pronounciation :: ", selected_pronounciation
            #print "Syllable :: ", min_syllable_count, "\n"
            return min_syllable_count
        else:
            #print("Not Found")
            return 1

    def remove_consonent(self, pronounciation):

        # #print(pronounciation)
        while pronounciation:
            first_sound = str(pronounciation[0])
            if first_sound.count('0') or first_sound.count('1') or first_sound.count('2'):
                # #print("BREAK")
                break
            else:
                # #print(first_sound)
                pronounciation.pop(0)
        return pronounciation

    def rhymes(self, a, b):
        """
        Returns True if two words (represented as lower-case strings) rhyme,
        False otherwise.
        """

        # TODO: provide an implementation!

        a = a.strip()
        b = b.strip()
        if a in self._pronunciations.keys() and b in self._pronunciations.keys():
            a_all_pronounciations = self._pronunciations[a]
            b_all_pronounciations = self._pronunciations[b]
            # #print("All a pronounciations :: ", a_all_pronounciations)
            # #print("All b pronounciations :: ", b_all_pronounciations)
            for each_pronounciation_a in a_all_pronounciations:
                for each_pronounciation_b in b_all_pronounciations:
                    a1 = self.remove_consonent(each_pronounciation_a)
                    b1 = self.remove_consonent(each_pronounciation_b)

                    # get min of a, b
                    if len(a1) < len(b1):
                        small = str(a1)
                        large = str(b1)
                    else:
                        small = str(b1)
                        large = str(a1)
                    # #print("S :: ", small)
                    # #print("L :: ", large)

                    # check if min is suffix of/ends with other
                    if large.endswith(small[1:]):               # [1:] removes '[' present at start
                        # #print("Rhymes\n\n")
                        return True
                    else:
                        pass
                        # #print("Doesn't rhymes\n\n")
            # #print("Doesn't rhymes\n\n")
            return False
        else:
            # #print("Not Found")
            return False

    def is_limerick(self, text):
        """
        Takes text where lines are separated by newline characters.  Returns
        True if the text is a limerick, False otherwise.

        A limerick is defined as a poem with the form AABBA, where the A lines
        rhyme with each other, the B lines rhyme with each other, and the A lines do not
        rhyme with the B lines.


        Additionally, the following syllable constraints should be observed:
          * No two A lines should differ in their number of syllables by more than two.
          * The B lines should differ in their number of syllables by no more than two.
          * Each of the B lines should have fewer syllables than each of the A lines.
          * No line should have fewer than 4 syllables

        (English professors may disagree with this definition, but that's what
        we're using here.)


        """
        # TODO: provide an implementation!

        text = text.strip(string.punctuation + '\n ')
        lines = text.split("\n")
        tokenized_lines = []
        num_syllables_list = []
        # #print "All Lines :: ", lines
        if len(lines) < 5:
            # #print("Less than 5 lines.")
            return False
        else:
            for each_line in lines:
                #tokenized_line = apostrophe_tokenize(each_line.strip(string.punctuation+" "))
                tokenized_line = word_tokenize(each_line.strip(string.punctuation+" "))
                tokenized_lines.append(tokenized_line)
            # #print("Tokenized Lines :: ", tokenized_lines)

            for each_line in tokenized_lines:
                count = 0
                for each_word in each_line:
                    if each_word not in string.punctuation:
                        count += self.num_syllables(each_word)
                num_syllables_list.append(count)
            # #print("Syllables List :: ", num_syllables_list)

            # Additionally, the following syllable constraints should be observed:
            # * No line should have fewer than 4 syllables
            if min(num_syllables_list) < 4:
                return False

            # * No two A lines should differ in their number of syllables by more than two.
            if abs(num_syllables_list[0] - num_syllables_list[1]) > 2 or abs(
                            num_syllables_list[0] - num_syllables_list[4]) > 2 or abs(
                        num_syllables_list[1] - num_syllables_list[4]) > 2:
                return False

            # * The B lines should differ in their number of syllables by no more than two.
            if abs(num_syllables_list[2] - num_syllables_list[3]) > 2:
                return False

            # * Each of the B lines should have fewer syllables than each of the A lines.
            min_of_A = min(num_syllables_list[0], num_syllables_list[1], num_syllables_list[4])
            # #print("Min of A :: ", min_of_A)
            if num_syllables_list[2] > min_of_A or num_syllables_list[3] > min_of_A:
                return False

            if self.rhymes(tokenized_lines[0][-1], tokenized_lines[1][-1]) and \
                    self.rhymes(tokenized_lines[2][-1], tokenized_lines[3][-1]) and \
                    self.rhymes(tokenized_lines[1][-1], tokenized_lines[4][-1]) and not \
                    self.rhymes(tokenized_lines[0][-1], tokenized_lines[2][-1]):
                # #print("It is a limerick")
                return True
            else:
                # #print("It is not a limerick")
                return False

        return False

    def apostrophe_tokenize(self, text_line):
        r = re.compile("[^\w\s']")
        new_text = r.sub("", text_line)
        tokenized_text = new_text.split(" ")
        return tokenized_text

    def guess_syllables(self, word):
        vowels = ['a', 'e', 'i', 'o', 'u', 'y']
        s = 0
        for i in range(0, len(word)):
            if i == 0 and word[i] in vowels:
                s += 1
            elif word[i] in vowels and word[i - 1] not in vowels:
                s += 1

        if word.endswith('le') and word[-3] not in vowels:
            s += 1

        if word.endswith('e') and word[-2] not in vowels:
            s -= 1

        #print word[-2]
        #print word[-3]
        #print s
        return int(s)


def apostrophe_tokenize(text_line):
    r = re.compile("[^\w\s']")
    new_text = r.sub("", text_line)
    tokenized_text = new_text.split(" ")
    return tokenized_text

# The code below should not need to be modified
def main():
  parser = argparse.ArgumentParser(description="limerick detector. Given a file containing a poem, indicate whether that poem is a limerick or not",
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  addonoffarg(parser, 'debug', help="debug mode", default=False)
  parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input file")
  parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file")




  try:
    args = parser.parse_args()
  except IOError as msg:
    parser.error(str(msg))

  infile = prepfile(args.infile, 'r')
  outfile = prepfile(args.outfile, 'w')

  ld = LimerickDetector()
  lines = ''.join(infile.readlines())
  outfile.write("{}\n-----------\n{}\n".format(lines.strip(), ld.is_limerick(lines)))

if __name__ == '__main__':
  main()
