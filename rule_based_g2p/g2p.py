#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from rule_based_mapper import rule_based_mapper
from syllabifier import syllabifier
import codecs
import re


class G2P:
  def __init__(self):
    self.place_names = []
    self.proper_nouns=[]
    self.last_names=[]
    self.pronunce_dict = defaultdict(list)
    self.abbrevs_dict = defaultdict(list)
    self.foreigns_dict = defaultdict(list)
    self.out_of_rules = []
    self.usual_roots = []
    self.load_all_dicts()
   



  def transcript(self,word):
    if word in self.pronunce_dict:
      return self.pronunce_dict[word]
    if word in self.abbrevs_dict:
      return self.abbrevs_dict[word]
    if word in self.foreigns_dict:
      return self.foreigns_dict[word]

    if "'" in word:
      word = word.lower()
      wordw = re.sub("'", "", word)
      if wordw in self.pronunce_dict:
        return self.pronunce_dict[wordw]
      root, suffix = word.split("'")
      mb = len(root)-1
      stemmable=1
    else:
      root=word
      suffix=""
      mb = len(root)-1
      #root , suffix, stemmable , mb= morph_process(word)

    #if not stemmable:
      #return self.process_rubbish_abbrev_foreign_word(word)
    if root in self.usual_roots:
      return self.process_word(wordw,root, suffix,mb, flag="just noun")
    
    elif root in self.proper_nouns:
      return self.process_word(wordw,root, suffix,mb, flag="proper noun")

    elif root in self.place_names:
      return self.process_word(wordw,root, suffix,mb, flag="place")

    elif root in self.last_names:
      return self.process_word(wordw,root, suffix,mb, flag ="last name")
    elif root in self.abbrevs_dict:
      return self.process_abbrev(wordw, root, suffix, mb)  
      

  def load_all_dicts(self):
    G2P.load_list("dicts/proper_nouns.txt", self.proper_nouns)
    G2P.load_list("dicts/place_names.txt", self.place_names)
    G2P.load_list("dicts/last_names.txt", self.last_names)
    G2P.load_dict("dicts/pronounces.dict", self.pronunce_dict)
    G2P.load_dict("dicts/foreign_names.dict", self.foreigns_dict)
    #G2P.load_dict("dicts/abbrevs.dict", self.abbrevs_dict)
    G2P.load_list("dicts/out_of_rule.txt", self.out_of_rules)
    G2P.load_list("dicts/all_roots.txt", self.usual_roots)


  @staticmethod
  def load_list(fname, listname):
    with codecs.open(fname, "r", "utf-8") as f:
       for line in f:
         listname.append(line.strip())

  @staticmethod
  def load_dict(fname, dictname):
    with codecs.open(fname, "r", "utf-8") as f:
       for line in f:
         print line
         w, p = line.strip().split(None,1)
         w = w.strip()
         p=p.strip()
         dictname[w].append(p)

  def process_abbrev(word, root, suffix):
    soften_flag=False
    if root in self.abbrevs_dict:
      rootpro_lis = self.abbrevs_dict[root]
    else:
      rootpro_lis = [rule_based_mapper.map_abbrevs(root)]
    return [rule_based_mapper.unite_root_and_suffix_seq(word, root, mb, pro, soften_flag) for pro in rootpro_lis]    

  def process_word(self,word,root, suffix,mb, flag):
    num_of_syl = syllabifier.syllabify(root)
    soften_flag= True
    if root in self.out_of_rules:
     soften_flag=False
    elif (len(num_of_syl)==1) and  (root.endswith("rt") or root.endswith("rk") or root.endswith("nk")):
      soften_flag=False

    if root in self.pronunce_dict:
      rootpro_lis = self.pronunce_dict[root]
    else:
      l = self.lookup_substrings(root)
      if l != -1:
        rootpro_lis = l
      else:
        rootpro_lis = [rule_based_mapper.map_one_to_one(root)]

    return [rule_based_mapper.unite_root_and_suffix_seq(word, root, mb, pro, soften_flag) for pro in rootpro_lis]


  def lookup_substrings(self, word):
    n = len(word) 
    for i in range(3, n):
      first_word = word[:i]
      second_word = word[i:]
      if (first_word in self.pronunce_dict) and (second_word in self.pronunce_dict) and (len(second_word) > 2):
        fp = self.pronunce_dict[first_word]
        sp = self.pronunce_dict[second_word]
        return map(lambda l: " ".join(l), zip(fp,sp))
    return -1
        

  def process_rubbish_abbrev_foreign_word(self, word):
    if word in self.abbrevs_dict:
      return self.abbrevs_dict[word] 
    if word in self.foreigns_dict:
      return self.foreigns_dict[word]

    flag="rubbish"
    root="word"
    suff=""
    possible_suffixes = [u"lerinden", u"larından", u"sindeki", u"sındaki", u"indeki", u"indeki", u"ındaki", u"deki", u"daki", u"teki", u"taki", u"taki",u"sinden", u"sından", u"sinde",u"sında",u"sine",u"sına",u"sini", u"sını", u"inde", u"ında", u"sıyla", u"siyle", u"sine", u"sına", u"yla", u"yle", u"la", u"le", u"ta", u"te", u"da", u"de", u"tan", u"ten", u"dan", u"den", u"nin", u"nın", u"ya", u"ye", u"yi", u"yı", u"si", u"sı", u"ini", u"ını", u"in", u"ın", u"a", u"e", u"i", u"ı", u"deydim", u"daydım", u"deydi", u"daydı", u"deydik", u"daydık", u"deydiniz", u"daydınız", u"ydi", u"ydı", u"layken", u"laydı",u"larken",u"lerken",u"dı", u"di", u"tı", u"ti"]
    english_trigrams = [u"the", u"and", u"ing", u"ion", u"tio", u"ent", u"ati", u"for", u"her", u"ter", u"hat", u"tha", u"ere", u"ate", u"his", u"con", u"res", u"ver", u"all", u"ons", u"nce", u"men", u"ith", u"ted", u"ers", u"pro", u"thi", u"wit", u"are", u"ess", u"not", u"ive", u"was", u"ect", u"rea", u"com", u"eve", u"per", u"int", u"est", u"sta", u"cti", u"ica", u"ist", u"ear", u"ain", u"one", u"our", u"iti", u"rat", u"eys", u"eyz", u"buk", u"ivi", u"tır", u"eyn", u"ırs", u"kon" , u"iff", u"for", u"ation", u"ment", u"nfo", u"duc", u"uct", u"cti", u"wh", u"lic", u"ica", u"cat", u"ati", u"ope", u"era", u"org", u"str", u"ition", u"tion", u"pres", u"heir", u"able", u"ough", u"hich", u"ight", u"tive", u"some", u"ecti"]

    for suffix in possible_suffixes:
      if word.endswith(suffix):
        part = word[:-len(suffix)]
        if part in self.abbrevs_dict:
          return self.abbrevs_dict[part], suffix
        if part in self.foreigns_dict:
          return self.abbrevs_dict[part], suffix


    for suffix in possible_suffixes:
      rest = word[:-len(suffix)]
      if len(rest) ==1 or len(rest) ==2:
        root=rest
        suff=suffix
        flag="abbrev"
        break
      elif "w" in rest or "x" in rest:
        root=rest
        suff =suffix
        flag="foreign"
        break
      elif any(tri in english_trigrams for tri in rest):
        root=rest
        suff =suffix
        flag="foreign"
        break
    rootpro_lis = [rule_based_mapper.map_abbrevs(root)] if (flag=="abbrev") else [rule_based_mapper.map_foreigns(root)]
    return [rule_based_mapper.unite_root_and_suffix_seq(word, root, mb, pro, soften_flag) for pro in rootpro_lis]

   
