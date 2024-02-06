import Q
class Model2:
    def __init__(self, allQ=set([]), finalStates=[]):
        self.allQ = allQ
        self.q0 = Q({}, 0)
        self.finalStates = finalStates
        self.number = 5
        self.q_verb = Q({}, 1)
        self.q_noun = Q({}, 2)
        self.q_adj = Q({}, 3)
        self.q_prefix = Q({}, 4)

    def readList(self, path):
        file = open(path, 'r')
        return set([word.replace('\n', '') for word in file.readlines()])

    def createState(self, currentState, word, number):
        q = Q({}, number)
        currentState.li[word] = (number, q)
        self.allQ.add(q)
        return q

    def loadData(self):
        self.prefixes = set(['un', 're'])
        # suffixes
        self.verb_suffixes = set(['s', 'ed', 'ing'])
        self.noun_suffixes = set(['s'])
        self.adv_suffixes = set(['s'])
        self.adjectives_suffixes = set(['er', 'est'])

        self.noun_adj_suffixes = set(['al', 'ial', 'ic', 'y', 'ful', 'less', 'ive'])  # substantiv -> adjectiv
        self.noun_ver_suffixes = set(['ate', 'ise', 'ify'])  # substantiv ->verb
        self.noun_adv_suffixes = set(['aly', 'ialy', 'icly', 'fuly', 'lessly', 'ively'])  # substantiv ->adverb

        self.adj_noun_suffixes = set(['ness', 'ity', 'ism'])  # adjectiv -> substantiv
        self.adj_ver_suffixes = set(['ate', 'ise', 'ify'])  # adjectiv ->verb
        self.adj_adv_suffixes = set(['ly'])  # adjectiv ->adverb
        self.adj_noun_suffixes = set(['ness', 'ity'])  # adjectiv ->substantiv

        self.verb_adj_suffixes = set(['able', 'ably'])  # verb ->adjectiv
        self.verb_adv_suffixes = set(['ly'])
        self.verb_noun_suffixes = set(['ance', 'ence', 'ment', 'tion'])

        self.verbs = self.readList('/kaggle/input/dataset-nlp/verbs.txt')
        self.nouns = self.readList('/kaggle/input/dataset-nlp/nouns.txt')
        self.adjectives = self.readList('/kaggle/input/dataset-nlp/adjectives.txt')
        self.pronouns = self.readList('/kaggle/input/dataset-nlp/pronouns.txt')
        self.adverbs = self.readList('/kaggle/input/dataset-nlp/adverbs.txt')
        self.prepositions = self.readList('/kaggle/input/dataset-nlp/prep.txt')
        self.conjunctions = set(['and', 'but', 'for', 'nor', 'or', 'yet', 'so'])
        self.articles = set(['a', 'the', 'an'])

        self.verbsE = self.readList('/kaggle/input/dataset-nlp/Everbs.txt')
        self.verbs = self.verbs.union(self.verbsE)

    def addVariantsVerb(self):
        for word in self.verb_suffixes:
            self.createState(self.q_verb, word, self.number)
            self.number = self.number + 1

        for word in self.verb_adj_suffixes:
            q = self.createState(self.q_verb, word, self.number)
            self.number = self.number + 1
            self.createState(q, 's', self.number)
            self.number = self.number + 1

        for word in self.verb_adv_suffixes:
            q = self.createState(self.q_verb, word, self.number)
            self.number = self.number + 1

        for word in self.verb_noun_suffixes:
            q = self.createState(self.q_verb, word, self.number)
            self.number = self.number + 1

    def addVariantsNoun(self):
        for word in self.noun_suffixes:
            self.createState(self.q_noun, word, self.number)
            self.number = self.number + 1

        for word in self.noun_adj_suffixes:
            self.createState(self.q_noun, word, self.number)
            self.number = self.number + 1

        for word in self.noun_ver_suffixes:
            self.createState(self.q_noun, word, self.number)
            self.number = self.number + 1

        for word in self.noun_adv_suffixes:
            self.createState(self.q_noun, word, self.number)
            self.number = self.number + 1

    def addVariantsAdj(self):
        for word in self.adjectives_suffixes:
            self.createState(self.q_adj, word, self.number)
            self.number = self.number + 1

        for word in self.adj_noun_suffixes:
            self.createState(self.q_adj, word, self.number)
            self.number = self.number + 1

        for word in self.adj_ver_suffixes:
            self.createState(self.q_adj, word, self.number)
            self.number = self.number + 1

        for word in self.adj_adv_suffixes:
            self.createState(self.q_adj, word, self.number)
            self.number = self.number + 1

        for word in self.adj_noun_suffixes:
            self.createState(self.q_adj, word, self.number)
            self.number = self.number + 1

    def loadVerb(self):
        self.addVariantsVerb()
        for word in self.verbs:
            currentState = self.q0
            if word not in currentState.li.keys():  # daca se poate merge din starea actuala altundeva
                currentState.li[word] = (self.number, self.q_verb)
                self.number = self.number + 1

    def loadNoun(self):
        self.addVariantsNoun()
        for word in self.nouns:
            currentState = self.q0
            if word not in currentState.li.keys():  # daca se poate merge din starea actuala altundeva
                currentState.li[word] = (self.number, self.q_noun)
                self.number = self.number + 1

    def loadAdj(self):
        self.addVariantsAdj()
        for word in self.adjectives:
            currentState = self.q0
            if word not in currentState.li.keys():  # daca se poate merge din starea actuala altundeva
                currentState.li[word] = (self.number, self.q_adj)
                self.number = self.number + 1

    def loadPrefix(self):
        for word in self.prefixes:
            currentState = self.q0
            if word not in currentState.li.keys():  # daca se poate merge din starea actuala altundeva
                currentState.li[word] = (self.number, self.q_prefix)
                self.number = self.number + 1

                for state in self.q0.li.items():
                    if state[0] in self.verbs:
                        self.q_adj.li[state[0]] = (state[1][0], state[1][1])

    def loadPronoun(self):
        for word in self.pronouns:
            currentState = self.q0
            if word not in currentState.li.keys():  # daca se poate merge din starea actuala altundeva
                self.createState(currentState, word, self.number)
                self.number = self.number + 1

    def loadAdv(self):
        for word in self.adverbs:
            currentState = self.q0
            if word not in currentState.li.keys():  # daca se poate merge din starea actuala altundeva
                self.createState(currentState, word, self.number)
                self.number = self.number + 1

    def loadPrep(self):
        for word in self.prepositions:
            currentState = self.q0
            if word not in currentState.li.keys():  # daca se poate merge din starea actuala altundeva
                self.createState(currentState, word, self.number)
                self.number = self.number + 1

    def loadConj(self):
        for word in self.conjunctions:
            currentState = self.q0
            if word not in currentState.li.keys():  # daca se poate merge din starea actuala altundeva
                self.createState(currentState, word, self.number)
                self.number = self.number + 1

    def loadArticle(self):
        for word in self.articles:
            currentState = self.q0
            if word not in currentState.li.keys():  # daca se poate merge din starea actuala altundeva
                self.createState(currentState, word, self.number)
                self.number = self.number + 1

    def build(self):
        self.loadData()
        self.loadVerb()
        self.loadNoun()
        self.loadPrefix()
        self.loadAdj()
        self.loadPronoun()
        self.loadAdv()
        self.loadPrep()
        self.loadConj()
        self.loadArticle()

    def search(self, word):
        if self.check_word(self.q0, word) == True:
            return "Cuvant bun"

    def check_word(self, currentState, word):
        if len(word) == 0:
            return True

        ret = False
        for i, ch in enumerate(word):

            # e-deletion natural
            if word[:i + 1] + 'e' in currentState.li.keys() and len(word[i + 1:]) > 2:  # putem avea see/ feel
                if word[i + 1] != 'e' and word[i + 1:] in ['ing', 'ed', 'al', 'ial', 'ic', 'ive', 'ate', 'ise', 'ify',
                                                           'ity', 'ism', 'able', 'ably', 'ance', 'ence']:
                    ret = ret | self.check_word(currentState.li[word[:i + 1] + 'e'][1], word[i + 1:])  # driving
                elif word[i + 1] == 'e' and word[i + 1:] in ['ing', 'ed', 'al', 'ial', 'ic', 'ive', 'ate', 'ise', 'ify',
                                                             'ity', 'ism', 'able', 'ably', 'ance', 'ence']:
                    return False

            # y-replacement
            if word[:i + 1] + 'y' in currentState.li.keys() and len(word) > i + 3:  # tried tries

                if word[i + 1] == 'y':
                    return False
                if 'ies' in word[i + 1:]:
                    ret = ret | self.check_word(currentState.li[word[:i + 1] + 'y'][1], word[i + 3:])

                if 'ied' in word[i + 1:]:
                    ret = ret | self.check_word(currentState.li[word[:i + 1] + 'y'][1], word[i + 2:])

                if 'ful' in word[i + 1:]:
                    ret = ret | self.check_word(currentState.li[word[:i + 1] + 'y'][1], word[i + 2:])


            elif word[:i + 1] in currentState.li.keys():  # daca se poate merge din starea actuala altundeva
                # consonant doubling

                if word[:i + 1] in self.verbsE and len(
                        word) > i + 4:  # daca un cuvant din verbsE contine 'able' sau 'ing' si nu e dublata consoana - False

                    if ('able' in word[i + 1:] or 'ing' in word[i + 1:]) and word[i] != word[i + 1]:

                        return False
                    else:
                        ret = ret | self.check_word(currentState.li[word[:i + 1]][1], word[i + 2:])  # begging

                # e-insertion
                if len(word) > i + 1 and (
                        word[i - 1:i + 1] == 'ch' or word[i - 1:i + 1] == 'sh' or word[i] in ['s', 'z', 'x']):
                    if word[i + 1] == 's':
                        return False
                    else:
                        ret = ret | self.check_word(currentState.li[word[:i + 1]][1], word[i + 2:])

                # k-insertion
                if len(word) > i + 1 and word[i] == 'c' and word[i - 1] in ['a', 'e', 'i', 'o', 'u']:
                    if word[i + 1] != 'k':
                        return False
                    if word[i + 2] in ['a', 'e', 'i', 'o', 'u']:
                        ret = ret | self.check_word(currentState.li[word[:i + 1]][1], word[i + 2:])
                ret = ret | self.check_word(currentState.li[word[:i + 1]][1], word[i + 1:])

        return ret