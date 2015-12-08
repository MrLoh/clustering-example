# -*- coding: utf-8 -*-
import os
from hashlib import md5

PARZU_EXE = './ParZu/parzu'
CACHE = 'cache'
EXIT_STATUS_SUCCESS = 0

def stem(string):
    '''extract list of stems from a string'''
    cache_file = CACHE + '/' + md5(string.strip()).hexdigest() + '.txt'
    # see whether stemming for string is cached
    try:
        stems_file = open(cache_file)
    except IOError:
        # write input string into temp file
        temp_file = CACHE + '/' + 'temp.txt'
        with open(temp_file, 'w') as f:
            f.write(string)
        # create stemming file from temp with ParZu save result in cache
        command = '{0} < {1} > {2}'.format(PARZU_EXE, temp_file, cache_file)
        if os.system(command) != EXIT_STATUS_SUCCESS:
            raise Exception('$' + command + ' failed')
        stems_file = open(cache_file)
    # extract stems from stemming_file
    stems = []
    for line in stems_file:
        # add stem unless line is empty or about punctuation
        if line != '\n' and line.split('\t')[3][0] != '$' :
            stems += [line.split('\t')[2].lower()]
    # return list of stems
    return stems


def find_fitting_cluster(string, clusters):
    '''find a fitting clusternumber for a given string and an array of cluster tags'''
    stems = stem(string)
    ratings = [0,0,0,0]
    for c in range(len(clusters)):
        # a check that ignores compound nouns could simply use the follwing line instead of the 4 lines after it
        ratings[c] = sum([1 if stems[i] in clusters[c] else 0 for i in range(len(stems))])
        # for tag in clusters[c]:
        #     for stm in stems:
        #         if tag in stm:
        #             ratings[c] += 1
    if sum(ratings) == 0:
        cluster = 5
    else:
        cluster = ratings.index(max(ratings))+1
    return cluster

def find_in_cluster_files(line):
    for i in range(1,6):
        with open('Testdaten/cluster_' + str(i) + '.txt') as f:
            if line in f.read().splitlines():
                return i



cluster_1_tags = ['versenden','email','verschicken','outlook','thunderbird']
cluster_2_tags = ['installation','admin','admin-rechte','setup','installieren']
cluster_3_tags = ['maus','mauszeiger','zeiger','cursor','trackpad','mousepad']
cluster_4_tags = ['installation','excel','powerpoint','formattierung','computer','abstürzen']

# # we might want to remove endings, if we check for compound words, that captures things like Versendeladebalken
# cluster_1_tags[0] = 'versend'
# cluster_1_tags[2] = 'verschick'
# cluster_2_tags[4] = 'installier'
# cluster_4_tags[5] = 'abstürz'
# # adding the verb click to cluster 3 seems to make sense
# cluster_3_tags += ['klick']

cluster_tags = [cluster_1_tags, cluster_2_tags, cluster_3_tags, cluster_4_tags]

inputs = open("Testdaten/unclustered_input.txt").read().splitlines()

for line in inputs:
    fit = find_fitting_cluster(line, cluster_tags)
    truth = find_in_cluster_files(line)
    if fit != truth:
        print('mistake in: \'%s\'' % line)
        print('is: %i | fitted: %i' % (truth, fit))

for i in range(1,6):
    print('\nCluster %i:' % i)
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    for line in inputs:
        fit = find_fitting_cluster(line, cluster_tags)
        truth = find_in_cluster_files(line)
        if fit == i:
            if truth == i:
                true_positives += 1
            else:
                false_positives += 1
        else:
            if truth == i:
                false_negatives += 1
    precision = float(true_positives)/(true_positives + false_positives)*100
    recall = float(true_positives)/(true_positives + false_negatives)*100
    print('precision: \t%.0f%%' % precision)
    print('recall: \t%.0f%%' % recall)
