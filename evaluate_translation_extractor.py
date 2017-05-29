import csv
import numpy as np
import about_translation as at

GOLDENFILENAME = 'upvoted.tab'
DEBUG = True


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


def classify_texts(texts, wordlist):
    predictions = []

    for i, text in enumerate(texts):
        if at.is_about_translation(text, wordlist, threshold=.05, do_nlp='spacey'):
            predictions.append('b')
        else:
            predictions.append('a')

        at.fancy_progress_bar(i, max_iterator=len(texts), max_nr_bars=31)
    print()
    return predictions


def make_confmat(listA, listB):
    '''

    :param listA:
    :param listB:
    :return:
    '''

    all_labels = set(list(listA) + list(listB))
    all_labels = sorted(all_labels)
    labeldict = {label:i for i, label in enumerate(all_labels)}
    print(all_labels)
    nr_unique = len(set(list(listA) + list(listB)))

    #sortedlabels = sorted(list(labeldict.keys()))

    m = np.zeros((nr_unique, nr_unique))

    for true, pred in zip(listA, listB):
        m[labeldict[true]][labeldict[pred]] += 1

    return m


def get_confmatstring(m):
    confmatstr = \
        """
        predicted
            a   b
true    a   {}  {}
        b   {}  {}

        """.format(int(m[0, 0]), int(m[0, 1]), int(m[1, 0]), int(m[1, 1]))
    return confmatstr


def print_confmat(m):
    confmatstr = get_confmatstring(m)
    print(confmatstr)

def get_pr_rec_string(m):
    precision_a = m[0, 0] / (m[0, 0] + m[1, 0])
    recall_a = m[0, 0] / (m[0, 0] + m[0, 1])
    precision_b = m[1, 1] / (m[1, 1] + m[0, 1])
    recall_b = m[1, 1] / (m[1, 1] + m[1, 0])


    pr_rec_string = \
        """
precision a:\t{}
recall a:\t{}
precision b:\t{}
recall b:\t{}
        """.format(precision_a, recall_a, precision_b, recall_b)

    return pr_rec_string

def evaluate_information_extractor(m):
    precision_about = m[0, 0] / (m[0, 0] + m[1, 0])
    print('precision a:\t{}'.format(precision_about))
    recall_about = m[0, 0] / (m[0, 0] + m[0, 1])
    print('recall a:\t{}'.format(recall_about))

    precision_not_about = m[1, 1] / (m[1, 1] + m[0, 1])
    print('precision b:\t{}'.format(precision_not_about))

    recall_not_about = m[1, 1] / (m[1, 1] + m[1, 0])
    print('recall b:\t{}'.format(recall_not_about))


def print_error_analysis(Ypred, Ytrue, posts, m, logfilename = 'error_analysis.txt'):

    log = open(logfilename, 'wt')
    log.write('a: not about translation\n')
    log.write('b: about translation\n')

    log.write('{}\n'.format(get_confmatstring(m)))

    log.write('{}\n'.format(get_pr_rec_string(m)))


    log.write('---pred = a and true = b (False Negatives) --------------------------------------------\n\n')
    i = 0
    for true, pred in zip(Ytrue, Ypred):
        if pred == 'a' and true == 'b':
            #print()
            #print(posts[i])
            log.write('\n{}\n'.format(posts[i]))

        i+=1

    log.write('\n\n---pred = b and true = a (False Positives) --------------------------------------------\n\n')
    i = 0
    for true, pred in zip(Ytrue, Ypred):
        if pred == 'b' and true == 'a':
            #print()
            #print(posts[i])
            log.write('\n{}\n'.format(posts[i]))

        i+=1

    log.write('\n\n---pred = b and true = b (True Positives) --------------------------------------------\n\n')
    i = 0
    for true, pred in zip(Ytrue, Ypred):
        if pred == 'b' and true == 'b':
            #print()
            #print(posts[i])
            log.write('\n{}\n'.format(posts[i]))

        i += 1

    log.close()


golden = read_csv_file('upvoted_a.tab', DEBUG)
header_golden = golden[0]
topiclabels = golden[1:,2]

topiclabels = preprocess_topics(topiclabels)

forumposts = golden[1:,5]
wordlist = at.load_wordlist('wordlist_generated.txt')

predictions = classify_texts(forumposts, wordlist)
m = make_confmat(topiclabels, predictions)

print_confmat(m)
evaluate_information_extractor(m)

print_error_analysis(predictions, topiclabels, forumposts, m)