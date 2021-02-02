#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Martina Astrid Rodda
#script extracts all direct objects and the verbs they depend from in the treebanked Perseus DL corpus,
    #and prints them to a .csv file.
#this version extracts the inflected forms, not the lemmas.
#known bugs: (1) it also extracts vocatives as verbs (these won't of course have objects)
#            (2) it also extracts adjectives (a) that are objects of verbs, independently of their case.
#            (3) it also extracts object verbs in the active form (a), but not passive ones.
#            (4) the .csv printer is suboptimal -- adds spaces between each character and puts characters
                    #on different rows

#import libraries
from lxml import etree
import argparse
from collections import defaultdict
import os
from os import listdir
from os.path import isfile, join
import csv

#define input path
path = "C:/Users/Martina Astrid Rodda/Desktop/semantic analysis wip/infiles"

#define output path
path_out = "C:/Users/Martina Astrid Rodda/Desktop/semantic analysis wip/outfiles"

#intialise file list
files = [f for f in listdir(path) if isfile(join(path, f))]

#open xml files with ElementTree
import xml.etree.ElementTree as ET
for file in files:
    print(file)
    tree = ET.parse(join(path,file))
    root = tree.getroot()

    #define output file
    out_file = 'obj_dependencies_'+str(file)+'.csv'

    #open output file
    if not os.path.exists(path_out):
        os.makedirs(path_out)
    with open(join(path_out, out_file), 'w', encoding = 'UTF-8') as output:
        outwriter = csv.writer(output, delimiter = '\t', quotechar = '|', quoting = csv.QUOTE_MINIMAL)

        #initialise list of object forms per sentence:
        for child in root:
            dependency_list = []
            head_list = []
            sentence_dependencies = defaultdict(list)
            if child.tag == "sentence":
                #find verb nodes and extract node number:
                for word in child:
                    postag = word.get('postag')
                    if 'v' in postag:
                        head = word.get('id')
                        verb_form = word.get('form')
                        head_list.append(head)
                        dependency_list.append((head, verb_form))
                #find all nodes where relation="OBJ" and head="$node number"
                for word in child:
                    relation = word.get('relation')
                    head = word.get('head')
                    postag = word.get('postag')
                    if relation == 'OBJ' and head in head_list and 'a' in postag:
                        obj_form = word.get('form')
                        dependency_list.append((head, obj_form))
            for k, v in dependency_list:
                sentence_dependencies[k].append(v)
            #print(sentence_dependencies)
            
            #write output to file:
            for k in sentence_dependencies:
                outwriter.writerow(str(k))
                for v in sentence_dependencies[k]:
                    outwriter.writerow(v)