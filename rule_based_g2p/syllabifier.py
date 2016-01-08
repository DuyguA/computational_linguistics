vowels = [u"a", u"e", u"i", u"\u0131", u"\xfc", u"u", u"o", u"\xf6"]

def is_a_vowel(letter): 
  return letter in vowels

class syllabifier:
  def __init__(self):
    pass

  @staticmethod
  def find_first_vowel(word):
    for index,letter in enumerate(word):
      if letter in vowels:
        return index
    return -1

  @staticmethod 
  def syllabify(word):
    syl_list=[]
    while(word):
      n = len(word)
      pos = syllabifier.find_first_vowel(word)
      if pos==-1:
        return -1
      else:
        if pos==n-1:
          syl_list.append(word)
          return syl_list
        else:
          next_letter=word[pos+1]
          if is_a_vowel(next_letter):
            syl_list.append(word[:pos+1])
            word = word[pos+1:]
          else:
            if pos+1==n-1:
              syl_list.append(word)
              return syl_list
            else:
              two_next_vowel= word[pos+2]
              if is_a_vowel(two_next_vowel):
                syl_list.append(word[:pos+1])
                word  = word[pos+1:]
              else:
                if pos+2==n-1:
                  syl_list.append(word)
                  return syl_list
                else:
                  three_next_vowel = word[pos+3]
                  if is_a_vowel(three_next_vowel):
                    syl_list.append(word[:pos+2])
                    word = word[pos+2:]  
                  else:
                    if (word[pos+1:pos+4] == u"str") or  (word[pos+1:pos+4] == u"ktr") or (word[pos+1:pos+4] == u"ntr"):
                      syl_list.append(word[:pos+3] )
                      word = word[pos+3:]
                    else:
                      syl_list.append(word[:pos+4] )
                      word = word[pos+4:]
    return syl_list
              
                  
