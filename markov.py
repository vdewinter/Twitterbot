""" This script takes a filename as a command line arugment and produces
a sentence using bigrams and Markov chaining.
"""

from sys import argv
import random

def parse_text():
    scriptname, filename = argv
    keep_lines = []
    keep_words = []

    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            if line.upper() != line:
                keep_lines.append(line)
            elif line.startswith("               "):
                keep_lines.append(line)
            # elif "(" in line and ")" in line:
            #     for char in line:
            #         while char == "(" and char != ")":
            #             char.replace(char, "")

    for i in keep_lines:
        split_words = i.split(" ")
        for word in split_words:
            word = word.replace(" ", "")
            if word != "":
                keep_words.append(word)

    return keep_words
    f.close()

def gen_dict(keep_words):
    bigram_dict = {}
    i = 0
    
    for i in range(len(keep_words)-2):
        bigram = (keep_words[i], keep_words[i+1])
        if bigram in bigram_dict:
            bigram_dict[bigram] += [keep_words[i+2]]
        else:
            bigram_dict[bigram] = [keep_words[i+2]]
    return bigram_dict
        
def gen_tweets(bigram_dict):
    len_tweet = 140

    sentence_beginnings = []

    for k,v in bigram_dict.iteritems():
        # find sentence beginnings
        if k[0].endswith(".") and "." not in k[1]:
            sentence_beginnings.append(k[1])
            break

    sentence_beginning = random.choice(sentence_beginnings)
    print sentence_beginning
    r = random.randint(0, len(v)-1)
    word = (k[1], v[r])
    print v[r]

    # pick a random sentence beginning

    while bigram_dict[word] and not bigram_dict[word][r].endswith("."):
        if word in bigram_dict:
            print bigram_dict[word][r], word
            r = random.randint(0, len(bigram_dict[word])-1)
            word = (word[1], bigram_dict[word][r])
        else:
            break

def main():
    gen_tweets(gen_dict(parse_text()))

if __name__ == "__main__":
    main()