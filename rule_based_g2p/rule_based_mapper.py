#!/usr/bin/env python
# coding: utf-8

import re
from syllabifier import syllabifier

class rule_based_mapper:
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
			u"z":"z",
			u"'":""}
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
		return not rule_based_mapper.is_a_rounded_vowel(vowel)

	@staticmethod
	def is_a_vowel(vowel):
		return vowel in [u"a", u"e", u"i",u"\u0131", u"\xfc", u"o", u"u", u"\xf6"]


	@staticmethod
	def  process_suffixes(suffixseq):
		resultstr=""
		endofseq = len(suffixseq)-1
		for i, currchar in enumerate(suffixseq):
			if currchar == u"k":
				if i== endofseq:
					prevchar = suffixseq[i-1]
					if rule_based_mapper.is_a_front_vowel(prevchar) : resultstr += "c"
					else: resultstr += "k"
					
				elif i==0:
					nextchar = suffixseq[1]
					if rule_based_mapper.is_a_front_vowel(nextchar) : resultstr += "c "
					else: resultstr += "k "
				else:
					nextchar = suffixseq[i+1]
					if rule_based_mapper.is_a_vowel(nextchar):
						if rule_based_mapper.is_a_front_vowel(nextchar) : resultstr += "c "
						else: resultstr += "k "
					else:
						prevchar = suffixseq[i-1]
						if rule_based_mapper.is_a_front_vowel(prevchar) : resultstr += "c "
						else: resultstr += "k "
			
			elif currchar == u"g":
				if i== endofseq:
					prevchar = suffixseq[i-1]
					if rule_based_mapper.is_a_front_vowel(prevchar) : resultstr+= "gj"
					else: resultstr+= "g"
					
				elif i==0:
					nextchar = suffixseq[1]
					if rule_based_mapper.is_a_front_vowel(nextchar) : resultstr+= "gj "
					else: resultstr+= "g "
				else:
					nextchar = suffixseq[i+1]
					if rule_based_mapper.is_a_vowel(nextchar):
						if rule_based_mapper.is_a_front_vowel(nextchar) : resultstr += "gj "
						else: resultstr+= "g "
					else:
						prevchar = suffixseq[i-1]
						if rule_based_mapper.is_a_front_vowel(prevchar) : resultstr+= "gj "
						else: resultstr+= "g "
							
			elif currchar == u"l":
				if i== endofseq:
					prevchar = suffixseq[i-1]
					if rule_based_mapper.is_a_front_vowel(prevchar) : resultstr+= "l"
					else: resultstr+= "5"
					
				elif i==0:
					nextchar = suffixseq[1]
					if rule_based_mapper.is_a_front_vowel(nextchar) : resultstr+= "l "
					else: resultstr+= "5 "
				else:
					nextchar = suffixseq[i+1]
					if rule_based_mapper.is_a_vowel(nextchar):
						if rule_based_mapper.is_a_front_vowel(nextchar) : resultstr+= "l "
						else: resultstr+= "5 "
					else:
						prevchar = suffixseq[i-1]
						if rule_based_mapper.is_a_front_vowel(prevchar) : resultstr+= "l "
						else: resultstr+= "5 "
		  	else:
				resultstr +=  rule_based_mapper.phonemap[currchar]					
				if i!= endofseq: resultstr +=" "
							
		return resultstr		



	@staticmethod
	def unite_root_and_suffix_seq(word, root, mb, pro, soften_flag=True):
		suffixseq = word[(mb+1):]
		suff_pro = rule_based_mapper.process_suffixes(suffixseq)
                suff_pro = suff_pro.strip()

		rootpro = pro.split()
		if word[mb] != root[mb]:
			rootpro[mb] = rule_based_mapper.phonemap[word[mb]] 
		elif  mb != len(word) and  rule_based_mapper.is_a_hard_consonant(word[mb]) and rule_based_mapper.is_a_vowel(word[mb+1]) and soften_flag: 
			rootpro[mb] = rule_based_mapper.phonemap[rule_based_mapper.soften(word[mb])]

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
				syl_vow = re.search(ur"[ae\u0131io\xf6u\xfc]", syl)
				is_front = rule_based_mapper.is_a_front_vowel(syl_vow)
				if len(syl)>1 and not rule_based_mapper.is_a_vowel(syl[0]) and not rule_based_mapper.is_a_vowel(syl[1]):
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
                                                        resultstr +=  rule_based_mapper.phonemap[currchar]
                                                        resultstr +=" "
						if i==0 : 
							if is_front : resultstr += "i "
							else: resultstr += "1"
                                         resultstr = resulstr[:-1]
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
							resultstr +=  rule_based_mapper.phonemap[currchar] 
							resultstr +=" "
					resultstr = resultstr[:-1]
					resultlis.append(resultstr)
							
		
		return " ".join(resultlis)



	def map_garbage(word):
		resultstr =""
		for currchar in word:
			resultstr += rule_based_mapper.phonemap[currchar]
		return resultstr
				
