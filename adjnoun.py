#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division

import xml.etree.ElementTree

from collections import defaultdict

# from IPython import embed

import argparse


parser = argparse.ArgumentParser(description='Analyses Old Greek xmls')
parser.add_argument('filenames', type=str, nargs='+',
                    help='name of the xml file to load')
parser.add_argument('--window-length', '-w', default=4, type=int,
                    help='length of window for matching')
parser.add_argument('--extract-length', '-e', default=2, type=int,
                    help='length of extract to show before and after the relevant words')
parser.add_argument('--threshold', '-t', default=20, type=int,
                    help='frequency threshold for pairs')
args = parser.parse_args()

# TODO: This only covers nouns and hopefully adjectives (・_・ヾ
ONE_LETTER_CODES = {
    'masc': 'M',
    'fem': 'F',
    'neut': 'N',
    'nom': 'N',
    'gen': 'G',
    'dat': 'D',
    'acc': 'A',
    'voc': 'V',
    'sg': 'S',
    'pl': 'P',
    'dual': 'D'
}

class Word(object):

    def __init__(self, xml_entry, sentence_id, position):
        self.sentence_id = sentence_id
        self.position = position

        self.id = xml_entry.attrib['id']
        self.form = xml_entry.attrib['form']

        # FIXME: can a word have more lemmas associated? (゜-゜)
        lemma = xml_entry.find('lemma')
        self.pos = lemma.attrib.get('POS', None)
        self.entry = lemma.attrib.get('entry', None)
        self.morph = set()
        for analysis in lemma.findall('analysis'):
            # ACHIEVEMENT: My first time using |= in Python! (ﾉ´ヮ´)ﾉ*:･ﾟ✧
            self.morph |= self._morph_to_set(analysis.attrib['morph'])
        try:
            # from cltk.corpus.greek.beta_to_unicode import Replacer
            self.replacer = Replacer()
        except:
            self.replacer = None

    def _morph_to_set(self, morph):
        morphologies = {''}
        for s in morph.split(' '):
            new_morphologies = set()
            for a in s.split('/'):
                if a not in ONE_LETTER_CODES:
                    continue
                new_morphologies |= {m + ONE_LETTER_CODES[a] for m in morphologies}
            if new_morphologies:
                morphologies = new_morphologies
        return morphologies

    def is_compatible_with(self, word):
        # TODO: make this work for words that are not noun/adjective pairs (　ﾟдﾟ)
        if not (
            (self.pos == 'noun' and word.pos == 'adjective') or 
            (self.pos == 'adjective' and word.pos == 'noun')):
            return False
        # Check that words are in the same sentence
        if self.sentence_id != word.sentence_id:
            return False
        # Check that words have at least one morphology in common
        if not (self.morph & word.morph):
            return False
        return True

    def __str__(self):
        try:
            return self.replacer.beta_code(self.form)
        except:
            # return '{}[{}]'.format(self.form, ','.join(self.morph))
            return self.form

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':


    words = []

    for filename in args.filenames:
        body = xml.etree.ElementTree.parse(filename).getroot()
        body = body.find('text').find('body')

        
        for sentence in body.findall('sentence'):
            for word in sentence.findall('word'):
                words.append(Word(word, sentence.attrib['id'], position=len(words)))

    compatible_tuples = []
    unique_pairs = defaultdict(list)

    for i, w1 in enumerate(words):
        for j, w2 in enumerate(words[i+1:i+args.window_length]):
            if w1.is_compatible_with(w2):
                compatible_tuples.append( (w1, w2) )
                k = frozenset((w1.entry, w2.entry))
                unique_pairs[k].append((w1, w2))

    for (f1, f2), occurences in sorted(unique_pairs.items(), key=lambda k: len(k[1]), reverse=True):
        if len(occurences) < args.threshold:
            continue
        print(u'Pair {} {}: total {}'.format(f1, f2, len(occurences)).encode('utf-8').decode('utf-8'))
        for w1, w2 in occurences:
            i, j = w1.position, w2.position
            extract = ' '.join([str(w) if i+k-args.extract_length != i and i+k-args.extract_length != j else '_' + str(w) + '_' for k, w in enumerate(words[i-args.extract_length:j+args.extract_length+1])])
            print('\tSentence {}: {}'.format(words[i].sentence_id, extract))
        


    # for w1, w2 in compatible_tuples:
    #     i, j = w1.position, w2.position
    #     extract = ' '.join([str(w) if i+k-extract_length != i and i+k-extract_length != j else '_' + str(w) + '_' for k, w in enumerate(words[i-args.extract_length:j+args.extract_length+1])])
    #     print('Sentence {}: {}'.format(words[i].sentence_id, extract))
