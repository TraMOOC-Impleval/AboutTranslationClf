# import spacy voor de tokenizer
import spacy
import math
import sys

nlp = spacy.load('en')


# load the wordlist with filename <filename>
# wordlist should have one word (or multiword phrase) per line
def load_wordlist(filename='automatic_translation_wordlist.txt'):
    f = open(filename, 'rt')
    wordlist = f.readlines()
    f.close()

    wordlist = [x.lower().strip() for x in wordlist]

    return wordlist


def naive_nlp(text):
    text = text.lower()
    for char in ".,;:!?":
        text = text.replace(char, '')
    text = text.strip()
    text = text.split()
    return text

# preprocess the text. No NLP-pipeline (yet)
# only tonkenisation lowering en strippen van newlines
# returns a string with the cleaned text
def preproc_text(text, do_nlp = 'naive'):  # basic preprocessing. NLP Pipeline via andere functie
    text = text.lower()
    text = text.strip()

    if do_nlp == 'spacey':
        doc1 = nlp(text)
    elif do_nlp == 'naive':
        doc1 = naive_nlp(text)
    else:
        doc1 = text.split()

    newtext = ''

    for token in doc1:
        newtext = newtext + ' ' + str(token)

    return newtext.strip()


# determines whether text is about translation
# text = the text to be classified
# wordlist: either a filename of the word list (type = string) or a list with words (type = list)
# threshold: what threshold must be met in order to 'be about translation'
# return score: is True when you want to return the score instead of a Boolean
# TODO: (maybe less naive scoring system.
def is_about_translation(text, wordlist='automatic_translation_wordlist.txt', threshold=.005, return_score=False, do_nlp = 'spacy'):
    if type(wordlist) == str:
        wordlist = load_wordlist(wordlist)

    text = preproc_text(text, do_nlp=do_nlp)

    score = 0
    for word in wordlist:
        score += text.count(word)

    score = score / (len(text.split()))

    if return_score:
        return score
    else:
        if score >= threshold:
            return True
        else:
            return False


# index = index
# max_iterator = the length of the thing youre iterating over
# max_nr_of_bars determines the size and precision of the progress-bar
import math
import sys


def fancy_progress_bar(index, max_iterator, max_nr_bars=30):
    percentage = (index + 1) * 100 / max_iterator
    num_bars = math.floor(percentage / (100 / max_nr_bars))
    num_whites = max_nr_bars - num_bars
    bar = "|{}{}|".format('-' * num_bars, ' ' * num_whites)
    sys.stdout.write("\r%d%% " % (percentage) + bar)
    sys.stdout.flush()
