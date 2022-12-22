import bisect
import numpy as np

class ValueData:
    def __init__(self, value, data) -> None:
        self.value = value
        self.data = data
    
    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __ne__(self, other):
        return self.value != other.value

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self) -> str:
        return  f'({self.value}, {self.data})'

class SortedValueDataSet:

    def __init__(self) -> None:
        self._list = []

    def add(self, elem: ValueData, mod=None):        
        i = bisect.bisect_left(self._list, elem)
        if len(self._list) != i and self._list[i].value == elem.value:
            if mod != None:
                self._list[i].data = mod(self._list[i].data)
            else:
                self._list[i].data = elem.data
            return self._list[i].data
        else:
            bisect.insort_left(self._list, elem)
            return elem.data

    def add_sum(self, elem: ValueData):
        return self.add(elem, lambda exist: exist + elem.data)    

    def get_IndexByValue(self, value):
        i = bisect.bisect_left(self._list, ValueData(value, None))
        if len(self._list) != i and self._list[i].value == value:
            return i
        else:
            return -1

    def get_DataByValue(self, value, default= None):
        i = self.get_IndexByValue(value)
        if i != -1:
            return self._list[i].data
        return default

    def to_set(self):
        return set([item.value for item in self._list])

    def to_numpy(self):
        return np.array(self._list)

    def __len__(self) -> int:
        return len(self._list)

    def __repr__(self) -> str:
        return repr(self._list)

    def get_DataByIndex(self, i):
        return self._list[i]


import string
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import regex

lemmatizer  = WordNetLemmatizer()
porter = PorterStemmer()
stopwords   = set(nltk.corpus.stopwords.words('english'))
punctuation = string.punctuation
reg = regex.compile('([\w]+)')

def normalize(text):
    for token in reg.findall(text):        
        token = token.lower()
        token = lemmatizer.lemmatize(token)
        #token = porter.stem(token)
        if token not in stopwords and token not in punctuation:
            yield token

def preproc_frec(doc: str, dict_term: dict, index_doc):
    items  = nltk.FreqDist(normalize(doc)).items()    
    for key, value in items:
        s = dict_term.get(key, SortedValueDataSet())        
        s.add_sum(ValueData(index_doc, value))
        dict_term[key] = s    