#!/usr/bin/env python
# -*- coding: utf-8 -*-

def process_rubbish_abbrev_foreign_word(word, abbrevs_list, foreigns_list, place_names, proper_nouns):
  if word in abbrevs_dict:
    return  (word, "", "abbrev")
  if word in foreigns_dict:
    return (word,"", "foreign")

  flag="rubbish"
  root=word
  suff=""
  possible_suffixes = [u"lerinden", u"larından", u"sindeki", u"sındaki", u"indeki", u"indeki", u"ındaki", u"deki", u"daki", u"teki", u"taki", u"taki",u"sinden", u"sından", u"sinde",u"sında",u"sine",u"sına",u"sini", u"sını", u"inde", u"ında", u"sıyla", u"siyle", u"sine", u"sına", u"yla", u"yle", u"la", u"le", u"ta", u"te", u"da", u"de", u"tan", u"ten", u"dan", u"den", u"nin", u"nın", u"ya", u"ye", u"yi", u"yı", u"si", u"sı", u"ini", u"ını", u"in", u"ın", u"a", u"e", u"i", u"ı", u"deydim", u"daydım", u"deydi", u"daydı", u"deydik", u"daydık", u"deydiniz", u"daydınız", u"ydi", u"ydı", u"layken", u"laydı",u"larken",u"lerken",u"dı", u"di", u"tı", u"ti"]
  english_trigrams = [u"land", u"ia",u"any",u"ania", u"the", u"and", u"ing", u"ion", u"tio", u"ent", u"ati", u"for", u"her", u"ter", u"hat", u"tha", u"ere", u"ate", u"his", u"con", u"res", u"ver", u"all", u"ons", u"nce", u"men", u"ith", u"ted", u"ers", u"pro", u"thi", u"wit", u"are", u"ess", u"not", u"ive", u"was", u"ect", u"rea", u"com", u"eve", u"per", u"int", u"est", u"sta", u"cti", u"ica", u"ist", u"ear", u"ain", u"one", u"our", u"iti", u"rat", u"eys", u"eyz", u"buk", u"ivi", u"tır", u"eyn", u"ırs", u"kon" , u"iff", u"for", u"ation", u"ment", u"nfo", u"duc", u"uct", u"cti", u"wh", u"lic", u"ica", u"cat", u"ati", u"ope", u"era", u"org", u"str", u"ition", u"tion", u"pres", u"heir", u"able", u"ough", u"hich", u"ight", u"tive", u"some", u"ecti", u"ish", u"she", u"ph"]

  if u"ğ" in word:
    part, s = word.split(u"ğ") 
    part += "k"
    if part in abbrevs_dict:
      return  part, s, "abbrev"
    elif part in foreigns_dict:
      return  part,s, "foreign"
    elif part in place_names:
      return  part,s,"place"
    elif root in proper_nouns:
      return  part,s, "proper noun"
    elif root in last_names:
      return  part,s, "proper noun"
    


  for suffix in possible_suffixes:
    if word.endswith(suffix):
      part = word[:-len(suffix)]
      s = word[len(suffix):]
      if part in abbrevs_dict:
        return  part, s, "abbrev"
      elif part in foreigns_dict:
        return  part,s, "foreign"
      elif part in place_names:
        return  part,s,"place"
      elif root in proper_nouns:
        return  part,s, "proper noun"
      elif root in last_names:
        return  part,s, "proper noun"


  for suffix in possible_suffixes:
    if word.endswith(suffix):
      rest = word[:-len(suffix)]
      s = word[len(suffix):]
      if len(rest) ==2 or len(rest) ==3:
        root=rest
        flag="abbrev"
        suff=s
        break
      elif any(tri in english_trigrams for tri in rest):
        root=rest
        suff=s
        flag="foreign"
        break


  return  root,suff,flag
