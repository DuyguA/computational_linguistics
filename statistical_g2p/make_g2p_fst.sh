#!/bin/bash

phonetisaurus-align --input=turkish.lexicon --ofile=turkish.corpus

ngramsymbols < turkish.corpus > turkish.syms
farcompilestrings --symbols=turkish.syms --keep_symbols=1    turkish.corpus > turkish.far
ngramcount --order=7 turkish.far > turkish.cnts
ngrammake  --method=kneser_ney turkish.cnts > turkish.mod
ngramprint --ARPA turkish.mod > turkish.arpa

phonetisaurus-arpa2fst --input=turkish.arpa  --prefix=turkish

#small test of turkish.fst

phonetisaurus-g2p --model=turkish.fst --input=ali --nbest=4 --words
