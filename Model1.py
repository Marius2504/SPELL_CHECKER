import json
import re
import Q

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data



class Model1:
    def __init__(self, allQ=set([]), finalStates=[]):
        self.allQ = allQ
        self.q0 = Q({}, 0)
        self.finalStates = finalStates
        self.number = 1

    def loadData(self):

        train_data = read_json('/kaggle/input/train-test/train.json')
        validation_data = read_json('/kaggle/input/train-test/validation.json')
        test_data = read_json('/kaggle/input/train-test/test.json')
        train_texts = [item['sentence1'] + ' ' + item['sentence2'] for item in train_data]
        validation_texts = [item['sentence1'] + ' ' + item['sentence2'] for item in validation_data]
        test_texts = [item['sentence1'] + ' ' + item['sentence2'] for item in test_data]
        self.texts = train_texts + validation_texts + test_texts

    def preprocessData(self):
        self.texts = [text.lower() for text in self.texts]
        self.texts = [re.sub(r'[^a-zăâîșț\-\s]', '', text) for text in self.texts]
        self.texts = [re.sub(' +', ' ', text) for text in self.texts]

    def extractUnique(self):
        self.totalWords = set([])
        for sen in self.texts:
            self.totalWords.update(set([word for word in sen.split()]))

    def buildVocab(self):
        i = 0
        for word in self.totalWords:
            currentState = self.q0
            for i, ch in enumerate(word):
                if word[i] in currentState.li.keys():  # daca se poate merge din starea actuala altundeva
                    currentState = currentState.li[word[i]][1]
                else:
                    q = Q({}, self.number)
                    currentState.li[word[i]] = (self.number, q)
                    self.allQ.add(q)
                    self.number = self.number + 1
                    currentState = q
                if i + 1 == len(word):
                    self.finalStates.append(currentState)
            i = i + 1

    def wrongLetter(self, wrong):
        proposed = ""
        maxi = len(wrong)
        for word in [x for x in self.totalWords if len(x) == len(wrong)]:
            dif = 0
            for i in range(len(word)):
                if word[i] != wrong[i]:
                    dif += 1
            if dif <= maxi:
                maxi = dif
                proposed = word
        return proposed, maxi

    def inverseLetter(self, wrong):
        proposed = ""
        maxi = len(wrong)
        possible = set([x for x in self.totalWords if len(x) == len(wrong)])
        for i in range(len(wrong) - 1):
            newWord = wrong[:i] + wrong[i + 1] + wrong[i] + wrong[i + 2:]
            if newWord in possible:
                return newWord, 1

        return "", len(wrong) + 1

    def plusLetter(self, wrong):
        proposed = ""
        maxi = len(wrong)
        possible = set([x for x in self.totalWords if len(x) + 1 == len(wrong)])
        for i in range(len(wrong)):
            if wrong[:i] + wrong[i + 1:] in possible:
                return wrong[:i] + wrong[i + 1:], 1
        return "", len(wrong) + 1

    def minusLetter(self, wrong):
        proposed = ""
        maxi = len(wrong)
        for word in [x for x in self.totalWords if len(x) - 1 == len(wrong)]:
            for i in range(len(word)):
                newWord = word[:i] + word[i + 1:]
                if newWord == wrong:
                    return word, 1
        return "", len(wrong) + 1

    def printVariants(self, word, patience):
        possible = [self.wrongLetter(word), self.inverseLetter(word), self.plusLetter(word), self.minusLetter(word)]
        newWord = ""
        multiple = False

        if patience == 0:
            patience = len(word)
        for variant in sorted(possible, key=lambda x: x[1]):
            if variant[1] <= patience and multiple == True:
                newWord += "/"
            if variant[1] <= patience:
                newWord += variant[0]
                multiple = True
        return newWord

    def check_word(self, word, patience=1):
        currentState = self.q0
        goodWord = True
        for i, ch in enumerate(word):
            if word[i] in currentState.li.keys():  # daca se poate merge din starea actuala altundeva
                currentState = currentState.li[word[i]][1]
            else:
                goodWord = False
        if goodWord == True and currentState in self.finalStates:
            return "Cuvant este corect"
        else:
            new = self.printVariants(word, patience)
            return f"Cuvantul ar putea fi: {new}"

    def build(self):
        self.loadData()
        self.preprocessData()
        self.extractUnique()
        self.buildVocab()
