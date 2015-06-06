import time
import random
import string
import nltk
nltk.download("cmudict")
from nltk.corpus import cmudict

class Markov(object):
    def __init__(self, words):
        self.stress = cmudict.dict()
        self.words = words
        self.limit = 255
        self.vowels = "aeiou"
        self.alphanum = string.digits + string.letters + " " + "'"

    def syllable_count(self, word):
        """
        accepts string
        returns count of stressed syllables via cmudict
        if string not in cmu corpora, falls back to swag
        """
        word = word.lower()
        try:
            val = self.stress[word]
            return len([i for i in val[0] if i[-1] in string.digits])
        except KeyError:
            return self.swag(word)

    def swag(self, word):
        """
        Scientific wild ass guess
        count number of vowels in a word one by one
        if vowell is preceeded by another vowel don't count it
        this is "close enough". One could do better with nltk and the
        cmudict, but the idea is to make a cut-up, yo.

        accepts a string
        returns a count of stressed syllables
        """

        # nothing with a number is real, man.
        for i in word:
            if i in string.digits:
                return 0

        word = word.lower()
        cnt = 0
        # begone bossy, silent e
        # this misses "theatre" of course . . .
        if not len(word):
            return 0

        if word[-1] == "e":
            cnt -= 1

        if word[-1] == "y":
            cnt += 1

        # is preceding letter a consonant?
        precon = True

        for i in word:
            if i in string.lowercase:
                if i in self.vowels:
                    if precon:
                        cnt += 1
                        precon = False
                else:
                    precon = True
        return cnt

    def chain(self, seed=None):

        lines = []

        if not seed:
            chain = [self.seed()]
        else:
            chain = [seed]

        for i in range(self.limit):
            k = chain[-1]
            word = random.choice(self.words[k])
            chain.append(random.choice(self.words[k]))

        syllables = 0
        line = []
        for word in chain:
            syllables += self.syllable_count(word)
            line.append(word)
            if syllables >= 10:
                lines.append(line)
                line = []
                syllables = 0

        return  lines

    def seed(self):
        while True:
            seed = random.choice(self.words.keys())
            if seed:
                return seed

