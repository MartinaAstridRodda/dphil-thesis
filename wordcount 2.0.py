#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Martina Astrid Rodda
#script opens a .csv file containing a list of words, one per line,
#       and counts the frequency of each unique word.

#import libraries
import os
from os import listdir
from os.path import isfile, join
import csv

# filename parameters:
verb = input("What verb is this fillers list for?")
comp = input("Type 'comparison' or 'target' depending on the case.")

#define input path
path_in = "C:/Users/Martina Astrid Rodda/Documents/uni/dphil/project/semantic analysis wip/fillers_lists"
#define input file
in_file = str(verb) + "_fillers_" + str(comp) + ".csv"

#define output path
path_out = "C:/Users/Martina Astrid Rodda/Documents/uni/dphil/project/semantic analysis wip/fillers_lists"
#define output file
out_file = str(verb) + "_uniq_" + str(comp) + ".csv"

with open(join(path_in, in_file), 'r', encoding = 'UTF-8') as infile:
    inreader = csv.reader(infile, delimiter = '\n', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
    #initialises empty list
    wordlist =[]
    #initialises empty count dictionary
    counts = {}

    #reads text and updates count dictionary
    for row in inreader:
        wordlist.append(str(row))
    for word in wordlist:
        if word in counts:
            counts[word] = counts[word] + 1
        else:
            counts[word] = 1

#prints dictionary output as defined
if not os.path.exists(path_out):
    os.makedirs(path_out)
with open(join(path_out, out_file), 'w', encoding = 'UTF-8') as output:
    outwriter = csv.writer(output, delimiter = '\t', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
    for word in counts:
        outwriter.writerow([word,str(counts[word])])