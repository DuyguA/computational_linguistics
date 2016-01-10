#!/usr/bin/env python

import re
from syllabifier import syllabifier

class word_to_sampa:
  phonemap = {u"a":"a", 
      u"b":"b", 
      u"c":"dZ", 
      u"\xe7":"tS", 
      u"d":"d",  
      u"e":"e", 
      u"f":"f", 
      u"g":"gj", 
      u"\u011f":"G",
      u"h":"h", 
      u"\u0131":"1", 
      u"i":"i", 
      u"j":"Z", 
      u"k":"k", 
      u"l":"l", 
      u"m":"m", 
      u"n":"n", 
      u"o":"o" , 
      u"\xf6":"2", 
      u"p":"p" , 
      u"r":"r", 
      u"s":"s", 
      u"\u015f":"S", 
      u"t":"t", 
      u"u":"u", 
      u"\xfc":"y", 
      u"w":"v", 
      u"v":"v", 
      u"y":"j", 
      u"x": "i c s",
      u"z":"z",
      u"'":"",
      u"@":"e t"}

  def __init__(self):
    pass

  @staticmethod
  def is_a_hard_consonant(cons):
    return cons in [u"p", u"t", u"k", u"\xe7"]

  @staticmethod
  def is_a_hard_consonant_saying(phon):
    return phon in ["p", "t", "k", "c", "tS"]




  @staticmethod
  def soften(cons):
    if cons == u"p": return u"b"
    elif cons == u"\xe7": return u"c"
    elif cons == u"t": return u"d"
    elif cons == u"k" : return u"\u011f" 
    else: return cons



  @staticmethod
  def is_a_front_vowel(vowel):
    return vowel in [u"i", u"\xf6", u"e", u"\xfc"]

  
  @staticmethod
  def is_a_back_vowel(vowel):
    return vowel in [u"a", u"o", u"u", u"\u0131"]


  @staticmethod
  def is_a_rounded_vowel(vowel):
    return vowel in [u"\xfc", u"o", u"u", u"\xf6"]

  
  @staticmethod
  def is_not_a_rounded_vowel(vowel):
    return not word_to_sampa.is_a_rounded_vowel(vowel)

  @staticmethod
  def is_a_vowel(vowel):
    return vowel in [u"a", u"e", u"i",u"\u0131", u"\xfc", u"o", u"u", u"\xf6"]

  @staticmethod
  def is_a_consonant(letter):
    return not word_to_sampa.is_a_vowel(letter)

  @staticmethod
  def is_a_phonetic_vowel(phone):
    return phone in ["a", "e", "i", "1", "u", "y", "o", "2"]
  
  @staticmethod
  def is_a_phonetic_consonant(phone):
    return not word_to_sampa.is_a_phonetic_vowel(phone)

  @staticmethod
  def  process_suffixes(suffixseq):
    resultstr=""
    endofseq = len(suffixseq)-1
    for i, currchar in enumerate(suffixseq):
      if currchar == u"k":
        if i== endofseq:
          prevchar = suffixseq[i-1]
          if word_to_sampa.is_a_front_vowel(prevchar) : resultstr += "c"
          else: resultstr += "k"
          
        elif i==0:
          nextchar = suffixseq[1]
          if word_to_sampa.is_a_front_vowel(nextchar) : resultstr += "c "
          else: resultstr += "k "
        else:
          nextchar = suffixseq[i+1]
          if word_to_sampa.is_a_vowel(nextchar):
            if word_to_sampa.is_a_front_vowel(nextchar) : resultstr += "c "
            else: resultstr += "k "
          else:
            prevchar = suffixseq[i-1]
            if word_to_sampa.is_a_front_vowel(prevchar) : resultstr += "c "
            else: resultstr += "k "
      
      elif currchar == u"g":
        if i== endofseq:
          prevchar = suffixseq[i-1]
          if word_to_sampa.is_a_front_vowel(prevchar) : resultstr+= "gj"
          else: resultstr+= "g"
          
        elif i==0:
          nextchar = suffixseq[1]
          if word_to_sampa.is_a_front_vowel(nextchar) : resultstr+= "gj "
          else: resultstr+= "g "
        else:
          nextchar = suffixseq[i+1]
          if word_to_sampa.is_a_vowel(nextchar):
            if word_to_sampa.is_a_front_vowel(nextchar) : resultstr += "gj "
            else: resultstr+= "g "
          else:
            prevchar = suffixseq[i-1]
            if word_to_sampa.is_a_front_vowel(prevchar) : resultstr+= "gj "
            else: resultstr+= "g "
              
      elif currchar == u"l":
        if i== endofseq:
          prevchar = suffixseq[i-1]
          if word_to_sampa.is_a_front_vowel(prevchar) : resultstr+= "l"
          else: resultstr+= "5"
          
        elif i==0:
          nextchar = suffixseq[1]
          if word_to_sampa.is_a_front_vowel(nextchar) : resultstr+= "l "
          else: resultstr+= "5 "
        else:
          nextchar = suffixseq[i+1]
          if word_to_sampa.is_a_vowel(nextchar):
            if word_to_sampa.is_a_front_vowel(nextchar) : resultstr+= "l "
            else: resultstr+= "5 "
          else:
            prevchar = suffixseq[i-1]
            if word_to_sampa.is_a_front_vowel(prevchar) : resultstr+= "l "
            else: resultstr+= "5 "
      else:
        resultstr +=  word_to_sampa.phonemap[currchar]          
        if i!= endofseq: resultstr +=" "
              
    return resultstr    



  @staticmethod
  def unite_root_and_suffix_seq(word, root, mb, pro, soften_flag=True):
    suffixseq = word[(mb+1):]
    suff_pro = word_to_sampa.process_suffixes(suffixseq)
    suff_pro = suff_pro.strip()

    rootpro = pro.split()

    if word[mb] != root[mb]:
      if (mb>1) and  word[mb-1] != root[mb-1]:
        rootpro = rootpro[:-2] + rootpro[-1:]
        suff_pro = word_to_sampa.process_suffixes(word[mb:]).strip()
      else: 
        rootpro[-1] = word_to_sampa.phonemap[word[mb]] 
    elif  mb != len(word)-1 and  word_to_sampa.is_a_hard_consonant_saying(rootpro[-1]) and word_to_sampa.is_a_vowel(word[mb+1]) and soften_flag: 
      rootpro[-1] = word_to_sampa.phonemap[word_to_sampa.soften(word[mb])]

    if suff_pro:  return " ".join(rootpro) + " "+ suff_pro
    else: return " ".join(rootpro)

  @staticmethod
  def map_one_to_one(word):
    resultlis=[]
    sform = syllabifier.syllabify(word)
    if sform == -1: return []
    else:
      for syl in sform:
        resultstr=""
        syl_vow = filter(lambda x: word_to_sampa.is_a_vowel(x), syl)
        is_front = word_to_sampa.is_a_front_vowel(syl_vow)
        if len(syl)>1 and word_to_sampa.is_a_consonant(syl[0]) and word_to_sampa.is_a_consonant(syl[1]):
           for  i, currchar in enumerate(syl):
             if currchar == u"k":
               if is_front : resultstr += "c "
               else: resultstr += "k "
             elif currchar == u"g":
               if is_front: resultstr+= "gj "
               else: resultstr+= "g "
             elif currchar == u"l":  
               if is_front  : resultstr+= "l "
               else: resultstr+= "5 "  
             else:
               resultstr +=  word_to_sampa.phonemap[currchar]
               resultstr +=" "
             if i==0 : 
               if is_front : resultstr += "i "
               else: resultstr += "1 "
           resultstr = resultstr[:-1]
           resultlis.append(resultstr)
          

        else:
          for  currchar in syl:
            if currchar == u"k":
              if is_front : resultstr += "c "
              else: resultstr += "k "
            elif currchar == u"g":
              if is_front: resultstr+= "gj "
              else: resultstr+= "g " 
            elif currchar == u"l":
              if is_front  : resultstr+= "l "
              else: resultstr+= "5 "  
            else:
              resultstr +=  word_to_sampa.phonemap[currchar] 
              resultstr +=" "
          resultstr = resultstr[:-1]
          resultlis.append(resultstr)
              
    
    return " ".join(resultlis)


  @staticmethod
  def map_garbage(word):
    resultstr =""
    for currchar in word:
      resultstr += word_to_sampa.phonemap[currchar]
      resultstr += " "
    return resultstr[:-1]

  @staticmethod 
  def map_abbrevs(abbrev):
    if len(abbrev)==2:
      f = abbrev[0]
      s = abbrev[1]
      if word_to_sampa.is_a_vowel(f) and word_to_sampa.is_a_consonant(s):
         return  word_to_sampa.phonemap[f] +": " + word_to_sampa.phonemap[s] + (" a:" if s=="k" else " e:")
      elif word_to_sampa.is_a_consonant(f) and word_to_sampa.is_a_consonant(s):
        return  word_to_sampa.phonemap[f] +(" a: " if f=="k" else " e: " ) + word_to_sampa.phonemap[s] + (" a:" if s=="k" else " e:")
      else:
        return word_to_sampa.map_one_to_one(abbrev) 
    elif len(abbrev)==3:
      f = abbrev[0]
      s = abbrev[1]
      t = abbrev[2]
      if word_to_sampa.is_a_consonant(f) and word_to_sampa.is_a_consonant(s) and word_to_sampa.is_a_consonant(t) :
        return word_to_sampa.phonemap[f]+(" a: " if f=="k" else " e: ")+word_to_sampa.phonemap[s]+(" a: " if s=="k" else " e: ")+word_to_sampa.phonemap[t] +(" a:" if t=="k" else " e:")
      elif word_to_sampa.is_a_consonant(f) and word_to_sampa.is_a_vowel(s) and word_to_sampa.is_a_consonant(t) :
        return word_to_sampa.map_one_to_one(abbrev)
      elif word_to_sampa.is_a_consonant(f) and word_to_sampa.is_a_consonant(s) and word_to_sampa.is_a_vowel(t) :
        return word_to_sampa.phonemap[f]+(" a: " if f=="k" else " e: ")+word_to_sampa.phonemap[s]+(" a: " if s=="k" else " e: ")+word_to_sampa.phonemap[t] + ":"
      elif word_to_sampa.is_a_consonant(f) and word_to_sampa.is_a_vowel(s) and word_to_sampa.is_a_vowel(t) :
        return word_to_sampa.phonemap[f]+" "+word_to_sampa.phonemap[s]+": "+word_to_sampa.phonemap[t] + ":"
      elif word_to_sampa.is_a_vowel(f) and word_to_sampa.is_a_consonant(s) and word_to_sampa.is_a_vowel(t) :
        return word_to_sampa.map_one_to_one(abbrev)
      elif word_to_sampa.is_a_vowel(f) and word_to_sampa.is_a_vowel(s) and word_to_sampa.is_a_consonant(t) :
        return word_to_sampa.phonemap[f]+": "+word_to_sampa.phonemap[s]+": "+word_to_sampa.phonemap[t] + (" a:" if t=="k" else " e:")
      elif word_to_sampa.is_a_vowel(f) and word_to_sampa.is_a_consonant(s) and word_to_sampa.is_a_consonant(t) :
        return word_to_sampa.phonemap[f]+": "+word_to_sampa.phonemap[s]+ (" a: " if s=="k" else " e: ") +word_to_sampa.phonemap[t] + (" a:" if t=="k" else " e:")
    

  @staticmethod
  def map_foreigns(word):
    grammap={
             "tation": "t e j S 1 n",
             "ation":" e j S 1 n",
             "ction": "c S 1 n",
             "other": "a d 1 r",
             "their": "d e j r",
             "there": " d e: r",
             "ition" : "i S 1: n",
             "ement" : "e m e n t",
             "inter":  " i n t e r",
             "tional": "S 1 n 1 5",
             "ional" : " 1 n 1 5",
             "ween" : "v 1: n",
             "ment":"m 1 n t",
             "ally": "e l i",
             "over": "o v 1 r",
             "sion": "S 1 n",
             "ther": "d e r",
             "that": "d e t",
             "atio": "e j S i j o",
             "tion": "S 1 n",
             "hough" : "o:",
             "ough": "o f",
             "rati": "r e j",
             "ecti": "e c S i",
             "sher": "S e r",
             "ish": "i S",
             "aph": "a f",
             "any": "a n i",
             "she": "S i",
             "any": "1 n i",
             "ive": "a j v",
             "the": "d e",
             "whi" : "v i",
             "whe" : "v e:",
             "ish": "i S",
             "con": "k o n",
             "chr": "k 1 r",
             "com": "k o m",
             "py": "p i",
             "ia": "i j a",
             "ch": "tS",
             "ci": "s a j"}
    
    if word.startswith(u"x"):
      word = u"[ k 1 s e ]" + word[1:]

    for gr in grammap:
      if gr in word:
        word = word.replace(gr, u" ["+grammap[gr] +u"] ")
  
    #unprocessed = re.findall(ur"(?:\]|^)([^\[\]]+)(?:\[|$)", word)
    unprocessed = re.findall(ur"(?:\]|^)([\w|\s]+)(?:\[|$)", word, re.U)



    for substr in unprocessed:
     if not substr.isspace():
       a = substr.strip()
       pro  = word_to_sampa.map_garbage(a)
       word =word.replace(a, pro)

   
    word = word.replace("[", "")
    word = word.replace("] ", "")
    #word = re.sub(ur"\s+"," ", word )
    word = word.strip()
    return word
  
        
      
     
    
   
