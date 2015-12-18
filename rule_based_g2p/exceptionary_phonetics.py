def n_l_assimilation(word, lis):
  if u"nl" in word:
    secondlis = map (lambda w : re.sub(r"n l", "n n",w) , lis)
    secondlis = map (lambda w : re.sub(r"n 5", "n n",w) , lis)
    lis += secondlis





def round_r_in_yor(word, tagset, surface, utterance):
  if "Prog1" in tagset:
    newut = utterance
    if tagset[-1] == "Prog1":
      del newut[-1]
      return (word, tagset, surface, [utterance, newut])
    else:
      pos = word.find("yor")
      if  not rule_based_mapper.is_a_vowel(word[pos+3]):
      del newut[pos+2]
      return (word, tagset, surface, [utterance, newut])

  return (word, tagset, surface, [utterance, newut])

