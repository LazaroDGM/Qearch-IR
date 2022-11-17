import regex as re
from nltk import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# Preprocesado de un documento en lenguaje natural
# para extraer todos los términos que contiene
def preproc_ocurrence(doc: str):
    # Todo lo convierte a minúsculas
    lower_case = doc.lower()
    # Crear conjunto de Términos
    terms = set()
    for word in re.findall('([\w]+)', lower_case):
        lem_word = lemmatizer.lemmatize(word)
        terms.add(lem_word)
    return terms

# Preprocesado de un documento en lenguaje natural
# para extraer la frecuencia de los términos que contiene
def preproc02(doc: str):
    # minusculas
    lower_case = doc.lower()
    # Crear conjunto de Términos
    terms = dict()
    for word in re.findall('([\w]+)', lower_case):
        lem_word = lemmatizer.lemmatize(word)
        if lem_word not in terms:
            terms[lem_word] = 0
        terms[lem_word]+=1
    return terms