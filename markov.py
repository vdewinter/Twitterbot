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
                if word != "":
                    keep_words.append(word)
    return keep_words
    f.close()

def gen_dict(keep_words):
    bigram_dict = {}

    for i in range(len(keep_words)-2):
        bigram = (keep_words[i], keep_words[i+1])
        if bigram in bigram_dict:
            bigram_dict[bigram] += [keep_words[i+2]]
        else:
            bigram_dict[bigram] = [keep_words[i+2]]
    return bigram_dict
        
def gen_tweets(bigram_dict):
    sentence_beginnings = []
    tweet_list = []
    tweet_max_len = 140/5 # assume 5 letters/word on avg

    # find sentence beginnings (elts in keys that follow elts ending in periods)
    for k,v in bigram_dict.iteritems():
        if k[0].endswith(".") and "." not in k[1]:
            sentence_beginnings.append(k[1])

    # pick a random sentence beginning
    sentence_beginning = random.choice(sentence_beginnings)
    tweet_list.append(sentence_beginning)

    # pick random value following sentence_beginning
    r = random.randint(0, len(v)-1)
    word = (k[1], v[r])

    # generate rest of sentence with markov chain
    while bigram_dict[word] and len(tweet_list) < tweet_max_len:
        r = random.randint(0, len(bigram_dict[word])-1)
        tweet_list.append(bigram_dict[word][r]) 
        word = (word[1], bigram_dict[word][r])

    tweet_string = " ".join(tweet_list)
    cutting_point = tweet_string.find(".", 100)
    print tweet_string[:cutting_point+1]
            
def main():
    parsed_text = parse_text()
    gened_dict = gen_dict(parsed_text)
    gen_tweets(gened_dict)

if __name__ == "__main__":
    main()