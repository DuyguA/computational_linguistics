#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from word_to_sampa import word_to_sampa
from syllabifier import syllabifier
from singleton import Singleton
import exceptionary_phonetics
import codecs
import re
import foma
import os




fsm = foma.read_binary("trmorph.fst")

def capital(word):
  return u"İ" + word[1:] if word[0]=="i" else word.capitalize()

def morph_analyze(word):
  morfos = []
  for result in fsm.apply_up(word):
    root, rest = result.split("<", 1)
    root = root.replace(u"â", "a")
    root = root.replace(u"\xee", "i")
    root = root.replace(u"û", "u")
    root = root.replace(u"ê", "e")
    if word.startswith(root):
      suff = word[len(root):]
    else:
      k = os.path.commonprefix([word, root])
      if not k: return []
      suff = word[len(k)+1:]
    morfos.append((root,suff))
  return morfos



class G2P:
  __metaclass__ = Singleton
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
      return exceptionary_phonetics.process_exceptional_phono(word,self.pronunce_dict[word])
    if word in self.abbrevs_dict:
      return exceptionary_phonetics.process_exceptional_phono(word,self.abbrevs_dict[word])
    if word in self.foreigns_dict:
      return exceptionary_phonetics.process_exceptional_phono(word,self.foreigns_dict[word])

    if "'" in word:
      word = word.lower()
      wordw = re.sub("'", "", word)
      if wordw in self.pronunce_dict:
        return self.pronunce_dict[wordw]
      root, suffix = word.split("'")
      analiz = [(root, suffix, "")]
      mb = len(root)-1
      stemmable=True
      analiz=[]
    else:
      root=word
      wordw=word
      suffix=""
      analiz = morph_analyze(word) or morph_analyze(capital(word))
      if analiz:
        stemmable=True
        root, suffix =  analiz[0]
        root = root.lower()
      else:
        stemmable=False
      mb = len(root)-1
      


    if stemmable:
      if root in self.usual_roots:
        return exceptionary_phonetics.process_exceptional_phono(wordw, self.process_word(wordw,root, mb, flag="just noun"))
      elif root in self.proper_nouns:
        return exceptionary_phonetics.process_exceptional_phono(wordw, self.process_word(wordw,root,mb, flag="proper noun"))
      elif root in self.place_names:
        return exceptionary_phonetics.process_exceptional_phono(wordw, self.process_word(wordw,root,mb, flag="place"))
      elif root in self.last_names:
        return exceptionary_phonetics.process_exceptional_phono(wordw, self.process_word(wordw,root,mb, flag ="last name"))
      elif root in self.abbrevs_dict:
        return exceptionary_phonetics.process_exceptional_phono(wordw, self.process_abbrev(wordw, root,mb))  
      elif root in self.foreigns_dict:
        return exceptionary_phonetics.process_exceptional_phono(wordw,self.process_foreigns(wordw, root,mb))  
      else:
        return exceptionary_phonetics.process_exceptional_phono(wordw, self.process_word(wordw, root, mb, flag="just noun"))
    else:
      return exceptionary_phonetics.process_exceptional_phono(wordw, self.process_rubbish_abbrev_foreign_word(wordw))
      

  def load_all_dicts(self):
    G2P.load_list("dicts/proper_nouns.txt", self.proper_nouns)
    G2P.load_list("dicts/place_names.txt", self.place_names)
    G2P.load_list("dicts/last_names.txt", self.last_names)
    G2P.load_dict("dicts/pronounces.dict", self.pronunce_dict)
    G2P.load_dict("dicts/foreign_names.dict", self.foreigns_dict)
    G2P.load_dict("dicts/abbrevs.dict", self.abbrevs_dict)
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
         w, p = line.strip().split(None,1)
         w = w.strip()
         p=p.strip()
         dictname[w].append(p)

  def process_abbrev(self,word, root,mb):
    soften_flag=False
    if root in self.abbrevs_dict:
      rootpro_lis = self.abbrevs_dict[root]
    else:
      rootpro_lis = [word_to_sampa.map_abbrevs(root)]
    return [word_to_sampa.unite_root_and_suffix_seq(word, root, mb, pro, soften_flag) for pro in rootpro_lis]    

  def process_foreigns(self,word, root, mb):
    soften_flag=False
    if root in self.foreigns_dict:
      rootpro_lis = self.foreigns_dict[root]
    else:
      rootpro_lis = [word_to_sampa.map_foreigns(root)]
    return [word_to_sampa.unite_root_and_suffix_seq(word, root, mb, pro, soften_flag) for pro in rootpro_lis]    

  def process_word(self,word,root, mb, flag):
    num_of_syl = syllabifier.syllabify(root)
    soften_flag= True
    if root in self.out_of_rules:
     soften_flag=False
    elif root.endswith(u"lç") or root.endswith(u"lk") or root.endswith(u"lp") or root.endswith(u"lt") or root.endswith(u"nç") or root.endswith(u"nt") or root.endswith(u"rç") or root.endswith(u"rk") or root.endswith(u"rp") or root.endswith(u"rs") or root.endswith(u"st") or root.endswith("rt") or root.endswith("rk") or root.endswith("nk"):
      soften_flag=False

    if root in self.pronunce_dict:
      rootpro_lis = self.pronunce_dict[root]
    else:
      l = self.lookup_substrings(root)
      if l != -1:
        rootpro_lis = l
      else:
        rootpro_lis = [word_to_sampa.map_one_to_one(root)]
        if  rootpro_lis ==[[]] : rootpro_lis = [word_to_sampa.map_garbage(root)]
    return [word_to_sampa.unite_root_and_suffix_seq(word, root, mb, pro, soften_flag) for pro in rootpro_lis]


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
    root=word
    soften_flag = True
    possible_suffixes = [u"lerinden", u"larından", u"sindeki", u"sındaki", u"indeki", u"indeki", u"ındaki", u"lardan",u"lerden", u"deki", u"daki", u"teki", u"taki", u"taki",u"sinden", u"sından", u"sinde",u"sında",u"sine",u"sına",u"sini", u"sını", u"inde", u"ında", u"sıyla", u"siyle", u"sine", u"sına", u"yla", u"yle", u"la", u"le", u"ta", u"te", u"da", u"de", u"tan", u"ten", u"dan", u"den", u"nin", u"nın", u"ya", u"ye", u"yi", u"yı", u"si", u"sı", u"ini", u"ını", u"in", u"ın", u"a", u"e", u"i", u"ı", u"deydim", u"daydım", u"deydi", u"daydı", u"deydik", u"daydık", u"deydiniz", u"daydınız", u"ydi", u"ydı", u"layken", u"laydı",u"larken",u"lerken",u"dı", u"di", u"tı", u"ti"]
    english_trigrams = [u"land", u"ia",u"any",u"ania", u"the", u"and", u"ing", u"ion", u"tio", u"ent", u"ati", u"for", u"her", u"ter", u"hat", u"tha", u"ere", u"ate", u"his", u"con", u"res", u"ver", u"all", u"ons", u"nce", u"men", u"ith", u"ted", u"ers", u"pro", u"thi", u"wit", u"are", u"ess", u"not", u"ive", u"was", u"ect", u"rea", u"com", u"eve", u"per", u"int", u"est", u"sta", u"cti", u"ica", u"ist", u"ear", u"ain", u"one", u"our", u"iti", u"rat", u"eys", u"eyz", u"buk", u"ivi", u"tır", u"eyn", u"ırs", u"kon" , u"iff", u"for", u"ation", u"ment", u"nfo", u"duc", u"uct", u"cti", u"wh", u"lic", u"ica", u"cat", u"ati", u"ope", u"era", u"org", u"str", u"ition", u"tion", u"pres", u"heir", u"able", u"ough", u"hich", u"ight", u"tive", u"some", u"ecti", u"ish", u"she", u"ph"]
 

    for suffix in possible_suffixes:
      if word.endswith(suffix):
        part = word[:-len(suffix)]
        if part in self.abbrevs_dict:
          return self.process_abbrev(word, part,len(part)-1)
        elif part in self.foreigns_dict:
          return self.process_foreigns(word, part,len(part)-1)
        elif part in self.place_names:
          return self.process_word(word,part, len(part)-1, flag="place")
        elif root in self.proper_nouns:
          return self.process_word(word,part, len(part)-1, flag="proper noun")
        elif root in self.last_names:
          return self.process_word(word,part, len(part)-1, flag="proper noun")


    if u"ğ" in word:
      part, s = word.rsplit(u"ğ", 1)
      part += "k"
      if part in self.abbrevs_dict:
        return self.process_abbrev(word, part,len(part)-1)
      elif part in self.foreigns_dict:
        return self.process_foreigns(word, part,len(part)-1)
      elif part in self.place_names:
        return self.process_word(word,part, len(part)-1, flag="place")
      elif root in self.proper_nouns:
        return self.process_word(word,part, len(part)-1, flag="proper noun")
      elif root in self.last_names:
        return self.process_word(word,part, len(part)-1, flag="proper noun")


    for suffix in possible_suffixes:
      if word.endswith(suffix):
        rest = word[:-len(suffix)]
        if len(rest) ==2 or len(rest) ==3:
          root=rest
          flag="abbrev"
          soften_flag=False
          break
        elif any(tri in english_trigrams for tri in rest):
          root=rest
          soften_flag=False
          flag="foreign"
          break

    if flag=="rubbish": 
      x =  word_to_sampa.map_one_to_one(word)
      return [x] if x else [word_to_sampa.map_garbage(word)]
 
    rootpro_lis = [word_to_sampa.map_abbrevs(root)] if (flag=="abbrev") else [word_to_sampa.map_foreigns(root)]
    return [word_to_sampa.unite_root_and_suffix_seq(word, root, len(root)-1, pro, soften_flag) for pro in rootpro_lis]
