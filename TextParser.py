# -*- coding: utf-8 -*- 
from LogicGroups import *

def to_syllables(w): # gets a word and returns list of syllables without special letters
    syll = [] # array with syllables
    prev = ""
    for el in spec:
        w = w.replace(el, "")
    for i in range(len(w)):
        if w[i] in vowels:
            syll.append(prev + w[i])
            prev = ""
        else:
            prev = prev + w[i]
    if len(syll) >= 1:
        syll[-1] = syll[-1] + prev
    for j in range(3):
        for i in range(len(syll) - 1):
            if len(syll[i + 1]) >= 4:
                if syll[i + 1][0] not in vowels and syll[i + 1][1] not in vowels:
                    syll[i] = syll[i] + syll[i + 1][0]
                    syll[i + 1] = syll[i + 1][1:]
    return syll

def make_lower(symbol): # function that returns lower version of letter if possible, letter if it already is low-register, empty string if it`s not a letter.
    if symbol == "ё":
        return symbol
    if symbol == "Ё":
        return "ё"
    if symbol in alpha:
        if symbol not in lower:
            return chr(ord(symbol) - ord("А") + ord("а"))
        return symbol
    return ""

def make_bigger(symbol):
    if symbol == "ё":
        return "Ё"
    if symbol == "Ё":
        return "Ё"
    if symbol in alpha:
        if symbol in lower:
            return chr(ord(symbol) + ord("А") - ord("а"))
        return symbol
    return ""

class word:
    def __init__(self, s):
        self.w = ""
        for el in s:
            self.w = self.w + make_lower(el)
        self.syll = to_syllables(self.w)
    def __str__(self):
        return self.w + " " + str(self.syll)

class text:
    def __init__(self, s):
        self.words = []
        curr = ""
        for el in s:
            if el not in alpha:
                if curr != "":
                    self.words.append(word(curr))
                    curr = ""
            else:
                curr = curr + el
        if curr != "":
            self.words.append(word(curr))
    def __str__(self):
        #return self.words.join("\n")
        z = []
        for el in self.words:
            z.append(str(el))
        return "\n".join(z)

#print(text(input()))
