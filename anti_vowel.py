# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 09:51:32 2017

@author: wonjo
"""

text = "Hey You!"
#%%
def anti_vowel(text_):
    output_text= ''
    for iter_text in text_:
        if iter_text.lower() == 'a' or iter_text.lower() == 'e' or iter_text.lower() == 'i' or iter_text.lower() == 'o' or iter_text.lower() == 'u':
            continue
        else:
            output_text += iter_text
    return output_text


#%%  Best Solution 

def anti_vowel_best(text):
    newtext = ''
    for c in text:
        if c.lower() not in "aeiou":
            newtext += c
    return newtext


#%%

score = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2, 
         "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3, 
         "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1, 
         "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4, 
         "x": 8, "z": 10}

#%%


def scrabble_score(word):
    total_sum = 0;
    for iter_word in word:
        if iter_word.lower() in score:
            total_sum += score[iter_word]
        else:
            continue
    return total_sum 

#%%
text= "this hack is wack hack"
word = "hack"
def censor(text, word):
  return text.replace(word, "*" * len(word))


#%%
def purify(num):
    evn = []
    for x in num:
        if x % 2 == 0:
            evn.append(x)
    return evn

#%%
sequence = [4, 5, 5, 4]
def median(sequence):
    sequence.sort()
    len_sequence = len(sequence)
    if len_sequence % 2 == 1:
        return sequence[int((len_sequence//2))]
    else:
        return (sequence[int((len_sequence//2))] + sequence[int((len_sequence//2))-1])/2.0
#%%
test = median(sequence)

