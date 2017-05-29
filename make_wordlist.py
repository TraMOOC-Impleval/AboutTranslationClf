import numpy as np
import csv
from collections import Counter
import re

def read_csv_file(filename, debug = False):
    '''

    :param filename:
    :param debug:
    :return:
    '''
    with open(filename) as f:
        reader = csv.reader(f, dialect="excel-tab")
        data = [row for row in reader]

    data = np.array(data)

    if debug:
        print('Data loaded. Shape: {}'.format(data.shape))

    return data


def preprocess_topics(topiclabels):
    newtopiclabels = []
    for label in topiclabels:
        if label == 'b':
            newtopiclabels.append('b')
        else:
            newtopiclabels.append('a')
    topiclabels = newtopiclabels
    return topiclabels

def make_wordcount(listoftexts):
    allwordlist = []
    for text in listoftexts:
        text = text.lower()
        text = re.sub('[\W]', ' ', text)
        textlist = text.split()
        allwordlist += textlist

    wordcount = Counter(allwordlist)

    return dict(wordcount)

def make_wordlist(count_of_interest, backgroundcount, threshold = 20):
    wordlist = []
    for word in count_of_interest.keys():
        if word in backgroundcount.keys():
            likelihoodratio = count_of_interest[word]/backgroundcount[word]
            if likelihoodratio > threshold:
                wordlist.append((word, likelihoodratio))

        else:
            print(word, count_of_interest[word])
            pass #todo: figure out what to do when word not in backgroundcount

    return wordlist

def write_wordlist(wordlist, filename = 'wordlist.txt'):
    with open(filename, 'wt') as f:
        for word, _ in wordlist:
            word = word + '\n'
            f.write(word)

data = read_csv_file('upvoted_b.tab', debug=True)

header_golden = data[0]
topiclabels = data[1:,2]

topiclabels = preprocess_topics(topiclabels)

forumposts = data[1:,5]

a_posts = []
b_posts = []

for label, post in zip(topiclabels, forumposts):
    if label == 'a':
        a_posts.append(post)
    elif label == 'b':
        b_posts.append(post)

wordcount_a = make_wordcount(a_posts)
wordcount_b = make_wordcount(b_posts)

relwordcount_a = {word:wordcount_a[word]/sum(list(wordcount_a.values())) for word in wordcount_a.keys()}
relwordcount_b = {word:wordcount_b[word]/sum(list(wordcount_b.values())) for word in wordcount_b.keys()}
print(relwordcount_a)
print(relwordcount_b)

wordlist = make_wordlist(relwordcount_b, relwordcount_a, threshold=15)

print(wordlist)
print(len(wordlist))

write_wordlist(wordlist, 'wordlist_generated.txt')
