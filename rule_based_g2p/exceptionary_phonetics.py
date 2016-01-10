#!/usr/bin/env python
# -*- coding: utf-8 -*-


from word_to_sampa import word_to_sampa
import re

def find_all_indexes(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


def n_l_assimilation(word, utterance):
  if u"nl" in word:
    utterance = re.sub(r"n l", "n n", utterance)
    utterance = re.sub(r"n 5", "n n",utterance)
  return utterance




def n_l_assimilation_lis(word, lis):
  newlis = list(lis)
  for  utter in lis:
    new_pro = n_l_assimilation(word, utter)
    if new_pro  not in newlis:
      newlis.append(new_pro)
  return newlis




def round_r_in_yor(word,utterance):
  if "yor" in word and not word.startswith("yor") and not word[1:].startswith("yor"):
    if  word.endswith("yor"):
      newut = utterance[:-2]
      return newut
    else:
      pos = utterance.find("j o r")
      if   word_to_sampa.is_a_phonetic_consonant(utterance[pos+6]):
        newut = utterance[:pos+3] + utterance[pos+5:]
        return newut
  return  None



def round_r_in_yor_lis(word, lis):
  newlis = list(lis)
  for  utter in lis:
    new_pro = round_r_in_yor(word, utter)
    if new_pro:
      newlis.append(new_pro)
  return newlis




def soft_g(word, utterance):
  lis=[utterance]
  if u"G" in utterance:
    if utterance.endswith(u"G"):
      lis = [utterance[:-2]+":"]
    else:
      if "e G i" in utterance:
        seclis =[re.sub("e G i", "e j i", utt) for utt in lis ]
        seclis.extend([re.sub("e G i", "i:", utt) for utt in lis])
        lis = seclis
      if "i G e" in utterance:
        trilis = [re.sub("i G e", "i j e", utt) for  utt in lis]
        lis =trilis
      if "1 G a" in utterance:
        tlis = [re.sub("1 G a", "1 a", utt) for  utt in lis]
        lis =tlis
      if "a G 1" in utterance:
        tli = [re.sub("a G 1", "a 1", utt) for  utt in lis]
        tli.extend([re.sub("a G 1", "a:", utt) for utt in lis])
        lis=tli
      sli =map(lambda x: re.sub(ur"(\w) G \1", r"\1:", x), lis)
      lis= sli
      flis = map(lambda word : re.sub(ur" G", ":", word) , lis)
      lis = flis
  return lis if lis != [utterance] else []     


def softg_lis(word, lis):
  newlis = []
  for  utter in lis:
    pro_lis = soft_g(word, utter)
    newlis += pro_lis
  return   lis+newlis

def process_exceptional_phono(word, utterlis):
  return    n_l_assimilation_lis(word, round_r_in_yor_lis(word, softg_lis(word, utterlis)))
  
