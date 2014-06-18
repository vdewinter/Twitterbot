""" This script takes a filename as a command line arugment and produces
a sentence using bigrams and Markov chaining.
"""

from sys import argv
import random

def parse_text():
    scriptname, filename = argv
    keep_words = []

    with open(filename) as f:
        for line in f.readlines():
            words = line.strip().replace("\"","").split(" ")
            for word in words:
                if word != "" and word.upper() != word:
                    keep_words.append(word)
    return keep_words

def gen_dict(words):
    bigram_dict = {}

    for i in range(len(words)-2):
        bigram = (words[i], words[i+1])
        if bigram in bigram_dict:
            bigram_dict[bigram] += [words[i+2]]
        else:
            bigram_dict[bigram] = [words[i+2]]
    return bigram_dict
        
def gen_tweets(bigram_dict):
    sentence_beginnings = []
    first_bigram = []
    tweet_list = []
    tweet_max_len = 140/4 # assume 4 letters/word on avg

    # find sentence beginnings (elts in keys that follow elts ending in periods)
    for k,v in bigram_dict.iteritems():
        if k[0].endswith(".") and not k[1].endswith("."):
            sentence_beginnings.append([k[1],v])
 
    # pick a random sentence beginning (first 2 words)
    first_bigram = random.choice(sentence_beginnings)
    first_word = first_bigram[0]
    first_bigram_value = first_bigram[1][0]

    tweet_list.append(first_word + " " + first_bigram_value)
    b = (first_word, first_bigram_value)

    # generate rest of sentence with markov chain
    while bigram_dict[b] and len(tweet_list) < tweet_max_len:
        r = random.randint(0, len(bigram_dict[b])-1)
        tweet_list.append(bigram_dict[b][r]) 
        b = (b[1], bigram_dict[b][r])

    tweet_string = " ".join(tweet_list).capitalize()
    cutting_point = tweet_string.find(".", 60)
    if len(tweet_string) > 0:
        print tweet_string[:cutting_point+1]
            
def main():
    parsed_text = parse_text()
    bigram_dict = gen_dict(parsed_text)
    gen_tweets(bigram_dict)

if __name__ == "__main__":
    main()