#!/usr/bin/env python3

from operator import itemgetter

def sorter(word):
    return ''.join(sorted(word))

def build_dictionary():
    ordered = {}
    with open('brit-a-z.txt', 'r') as f:
        for line in f:
            word = line[:-1]
            key = sorter(word)
            if key in ordered:
                ordered[key].append(word)
            else:
                ordered[key] = [word]
        return ordered

ANAGRAM_DICTIONARY = build_dictionary()

def anagram(string):
    try:
       words = ANAGRAM_DICTIONARY[sorter(string)]
    except KeyError:
        return 'No_Anagrams'
    return words

def substring(string):
    substrings = []
    n = len(string)
    power = 2**n
    for i in range(1, power):
        spec = "0" + str(n) + "b"
        bin = format(i, spec)
        substring = ""
        compstring = ""
        for j in range(n):
            if bin[j] == "1":
                substring += string[j]
            else:
                compstring += string[j]
        substrings.append([substring, compstring])
    return substrings

def substrings(string):
    chars = list(string)
    substrings = set()
    result = []
    n = len(string)
    power = 2**n
    for i in range(1, power):
        spec = "0" + str(n) + "b"
        bin = format(i, spec)
        substring = ""
        compstring = ""
        for j in range(n):
            if bin[j] == "1":
                substring += string[j]
        substrings.add(substring)
    for substring in substrings:
        cha = list(string)
        for letter in list(substring):
            cha.remove(letter)
        result.append([substring, ''.join(cha)])
    return result

def evaluate(entry):
    if entry.string == '':
        return [entry]
    solutions = []
    for sub in entry.substrings:
        evalue = anagram(sub[0])
        if evalue != 'No_Anagrams':
            new_good_words = entry.good_words + [evalue]
            new_string = sub[1]
            new_solution = Anagram(new_string, new_good_words)
            solutions.append(new_solution)
    return solutions

def expander(anagrams):
    result = []
    for anagram in anagrams:
        new_anagrams = evaluate(anagram)
        result += new_anagrams
    return result

def forsorting(solution):
    result = ''
    for word in solution:
        result += word[0] + str(1)
    return result

def solve(string):
    anagram = [Anagram(string)]
    while True:
        previous = anagram
        anagram = expander(anagram)
        if previous == anagram:
            break
    solutions = []
    for ana in anagram:
        if ana.string == '':
            ana.good_words.sort(key=forsorting)
            solutions.append(ana.good_words)
    solutions.sort(key=forsorting)
    previous = []
    for solution in solutions[:]:
        if solution == previous:
            solutions.remove(solution)
        previous = solution
    solutions.sort(key=len, reverse=True)
    for solution in solutions:
        print(solution)
    print(len(solutions))
    return solutions

class Anagram():
    def __init__(self, string, good_words=[]):
        self.good_words = good_words
        self.string = string
        self.substrings = substrings(string)

while True:
    new_anagram = input('Enter an anagram or STOP: ')
    if new_anagram == 'STOP':
        break
    solve(new_anagram)
