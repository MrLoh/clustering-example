# -*- coding: utf-8 -*-

from cluster import *

# cluster tags as specified in Testdaten/overview.xls
cluster_1_tags = ['versenden','email','verschicken','outlook','thunderbird']
cluster_2_tags = ['installation','admin','admin-rechte','setup','installieren']
cluster_3_tags = ['maus','mauszeiger','zeiger','cursor','trackpad','mousepad']
cluster_4_tags = ['installation','excel','powerpoint','formattierung','computer','abstürzen']

# we might want to remove endings, to find compound nouns from verbs like Versendeladebalken
cluster_1_tags[0] = 'versend'
cluster_1_tags[2] = 'verschick'
cluster_2_tags[4] = 'installier'
cluster_4_tags[5] = 'abstürz'
# adding the verb click to cluster 3 seems to make sense
cluster_3_tags += ['klick']

# bind clusters to array
cluster_tags = [cluster_1_tags, cluster_2_tags, cluster_3_tags, cluster_4_tags]

# read unclustered testset into list
test_set = open("Testdaten/unclustered_input.txt").read().splitlines()

# print those lines that were not fitted correctly
for line in test_set:
    fit = find_fitting_cluster(line, cluster_tags)
    truth = find_in_cluster_files(line)
    if fit != truth:
        print('mistake in: \'%s\'' % line)
        print('is: %i | fitted: %i' % (truth, fit))

# calculate and print precision and recall for all clusters
for i in range(1,6):
    print('\nCluster %i:' % i)
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    for line in test_set:
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
