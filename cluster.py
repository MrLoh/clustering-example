# -*- coding: utf-8 -*-

import os
from hashlib import md5


PARZU_EXE = './ParZu/parzu' # path to ParZu executable
CACHE_DIR = 'cache' # cache directory
CLUSTERS_DIR = 'Testdaten' # directory with clustered lines
EXIT_STATUS_SUCCESS = 0 # system exit status on success



def stem(string):
    '''extract list of stems from a string'''
    # create cache file name from string
    cache_file = '%s/%s.txt' % (CACHE_DIR, md5(string.strip()).hexdigest())
    # see whether stemming for string is cached
    try:
        stems_file = open(cache_file)
    # otherwise run ParZu to get stems
    except IOError:
        # write input string into temp file
        temp_file = '%s/temp.txt' % CACHE_DIR
        with open(temp_file, 'w') as f:
            f.write(string)
        # create stemming file from temp with ParZu save result in cache
        command = '%s < %s > %s' % (PARZU_EXE, temp_file, cache_file)
        if os.system(command) != EXIT_STATUS_SUCCESS:
            raise Exception('$ %s failed' % command)
        # open generated stems file
        stems_file = open(cache_file)

    # extract stems from stemming_file
    stems = []
    for line in stems_file:
        # add stem unless line is empty or punctuation
        if line != '\n' and line.split('\t')[3][0] != '$' :
            stems += [line.split('\t')[2].lower()]
    # return list of stems
    return stems



def find_fitting_cluster(string, clusters):
    '''find a fitting clusternumber for a given string and an array of cluster tags'''
    # get stems of word
    stems = stem(string)
    ratings = [0 for i in range(len(clusters))]
    for c in range(len(clusters)):
        # a check that ignores compound nouns could simply use the
        # follwing line instead of the 4 lines after it
        # ratings[c] = sum([1 if stems[i] in clusters[c] else 0 for i in range(len(stems))])
        # loop over cluster tags
        for tag in clusters[c]:
            # loop over stems in line
            for stm in stems:
                # increase rating if cluster tag is in stem
                if tag in stm:
                    ratings[c] += 1
    # if no tags have been found return post last cluster
    if sum(ratings) == 0:
        cluster = len(clusters)
    # otherwise return number of cluster with maximum frequency of hits
    else:
        cluster = ratings.index(max(ratings))
    # return number of cluster, start counting at 1
    return cluster + 1



def find_in_cluster_files(line):
    '''find in which cluster file the line is contained'''
    # loop over cluster files
    for i in range(1,6):
        with open('%s/cluster_%i.txt' % (CLUSTERS_DIR, i)) as f:
            # return cluster number if line is found in cluster
            if line in f.read().splitlines():
                return i
