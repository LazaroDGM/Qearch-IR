from nltk import WordNetLemmatizer
import regex as re

# Definición del lenguaje de consultas
# Asociativo a la derecha
# E -> TX
# X -> &E | |E | epsilon
# T -> t | (E) | ~T
 
# Clase para parsear expresiones booleanas y evaluarlas
class ParserBoolean:
    def __init__(self, terms: dict, universe= set(), lemmatizer = WordNetLemmatizer()) -> None:
        if len(universe) == 0:
            for set in terms.values():
                universe = universe.union(set)
        # Diccionario de términos con conjunto de documentos en los que se encuentra
        self.terms = terms
        # Conjunto de todos los documentos (solo índices)
        self.universe = universe
        # Para normalizar las palabras
        self.lemmatizer = lemmatizer
    
    # Elimina el diccionario de términos y el universo de la memoria
    def DestroyDataset(self):
        del self.terms
        del self.universe
        self.terms = None
        self.universe = None

    # Cambia el diccionario de términos y el universo
    # Recomendado primero ejecutar un DestroyDataset primero para vaciar memoria antes
    def ModDataset(self, terms: dict, universe= set()):
        if len(universe) == 0:
            for set in terms.values():
                universe = universe.union(set)
        self.terms = terms
        self.universe = universe

    def E(self, tokens, i):
        value, i = self.T(tokens, i)
        value, i = self.X(tokens, i, value)
        return value, i

    def X(self, tokens, i, value: set):
        if i < len(tokens):
            if tokens[i] == '|':
                new_value, i = self.E(tokens, i+1)
                value = value.union(new_value)        
            elif tokens[i] == '&':
                new_value, i = self.E(tokens, i+1)
                value = value.intersection(new_value)
        return value, i

    def T(self, tokens, i):
        if i < len(tokens):
            if tokens[i] == '~':
                value, i = self.T(tokens, i+1)
                value = self.universe.difference(value)
            elif tokens[i] == '(':
                value, i = self.E(tokens, i+1)
                if tokens[i] != ')':
                    raise Exception('Falta parentesis de cierre')
                i += 1
            else:
                value = tokens[i]
                i += 1
        return value, i
    
    # Tokenizador de las expresiones booleanas
    def tokenize(self, str: str):
        tokens = []   
        str = str.lower()     
        for item in re.findall('([\(\)&~|]|[\w]+)', str):
            if item in ['~', '&', '|', '(', ')']:
                tokens.append(item)                
            else:
                if re.match('\w+', item) == None:
                    raise Exception('Bad Expression')
                item
                item = self.lemmatizer.lemmatize(item)                
                if item in self.terms.keys():
                    tokens.append(self.terms[item])
                else:
                    tokens.append(set())
        return tokens

    # Evaluador de la expresión booleana
    def eval(self, exp: str):
        tokens = self.tokenize(exp)
        value, i = self.E(tokens, 0)
        if i != len(tokens):
            raise Exception('Parser Malo')
        return value