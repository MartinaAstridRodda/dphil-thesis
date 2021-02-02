# dphil-thesis

This repository contains all the code for my DPhil thesis, "A corpus study of formulaic variation and linguistic productivity in early Greek epic." (I will link to an online copy of the thesis as soon as it is accessible.)

I am releasing the code for reasons of transparency and "peer-reviewability," and in the hope that scholars looking to do something similar to what I have done will be able to take advantage of it. The user should be warned that this is not necessarily *elegant* code: I was a complete beginner at Python when I started my degree, and my only goal was writing something serviceable for my work. Also, as my corpus was very small compared to most modern-language corpora, I was not terribly concerned with making my code efficient. I have listed known bugs in the comments for each script.

All code in this repository is my work apart from adjnoun.py, which is the work of Dr Alessandro Achille (https://alexachi.github.io/).

Contents of this repository:

1) adjnoun.py: a Python 3 script which extracts pairs of adjectives and nouns which agree with each other (same case, number, and gender) from .xml files in the Diorisis Ancient Greek corpus (https://www.doi.org/10.6084/m9.figshare.6187256). The script produces a list of pairs, each of which is followed by all occurrences of the pair, printed with a context window chosen by the user. The user can also set the maximum window of distance between the adjective and the noun.

2) corpusprocess_2.0.py: a Python 3 script which extracts the collocates for each word in the Diorisis corpus, that is, the words that occur together with the target word, within a window of co-occurrence defined by the user. It produces output files that can be fed into the DISSECT tool (https://www.aclweb.org/anthology/P13-4006/).

3) extract_obj_1.0.py: a Python 3 script which extracts all direct objects and the verbs they depend from in files from the treebanked Perseus DL corpus (https://perseusdl.github.io/treebank_data/), and prints them to a .csv file. NB this version extracts the inflected forms, not the lemmas.
