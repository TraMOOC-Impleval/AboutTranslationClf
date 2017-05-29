import numpy as np
import csv
import random

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

def write_line(linelist, handle , delim = '\t'):
    outline = delim.join(linelist) + '\n'
    handle.write(outline)
    pass


outa = open('upvoted_a.tab', 'wt')
outb = open('upvoted_b.tab', 'wt')


golden = read_csv_file('upvoted.tab', DEBUG)
header = golden[0]

data = golden[1:]

write_line(header,outa)
write_line(header,outb)

for row in data:
    if random.random() < .5:
        write_line(row, outa)
    else:
        write_line(row, outb)

outa.close()
outb.close()


