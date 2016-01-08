#!/bin/bash

phonetisaurus-align --input=turkish.lexicon --ofile=turkish.corpus
estimate-ngram -o 7 -t turkish.corpus -wl turkish.arpa
phonetisaurus-arpa2fst --input=turkish.arpa  --prefix=turkish

#small test of turkish.fst

phonetisaurus-g2p --model=turkish.fst --input=ali --nbest=4 --words
