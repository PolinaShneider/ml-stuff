from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords, wordnet as wn
from string import punctuation
import pymorphy2
import pandas as pd

# import ssl
#
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
#
# nltk.download()

raw_data = pd.read_table('./data/descriptions.tsv')
raw_data.columns = ['id', 'description']

data = raw_data.dropna()
data = data.drop(['id', 'description'], axis=1)

russian_stopwords = stopwords.words("russian")

result = []
morph = pymorphy2.MorphAnalyzer()

areas = {
    17: 'Информационные технологии',
    50: 'Программирование',
    21: 'Биотехнологии',
    180: 'Информационная безопасность'
}


def normalize(word):
    return morph.parse(word)[0].normal_form


def tokenize_text():
    for text in raw_data.description:
        # do the nlp stuff https://nlpub.ru/NLTK
        tokens = word_tokenize(text.lower())
        normalized = map(normalize, tokens)
        without_sw = []
        for token in normalized:
            if token not in russian_stopwords and token not in punctuation:
                without_sw.append(token)

        nouns = []
        for token, pos in pos_tag(without_sw):
            if pos.startswith('N'):
                nouns.append(token)

        print('-------')
        print(nouns)
        compare_each(nouns)


raw_data2 = pd.read_table('./data/entities_by_domain.tsv')
raw_data2.columns = ['domain_id', 'entities']

data2 = raw_data2.dropna()
data2 = data2.drop(['domain_id', 'entities'], axis=1)


def toLower(x):
    return normalize(x.lower())


domain_entities = {}

for val in raw_data2.iterrows():
    domain_id = val[1].domain_id
    line = val[1].entities
    el = line[1:-1]
    arr = el.split(',')
    lower_arr = map(toLower, arr)
    domain_entities[domain_id] = list(lower_arr)


def isSimilar(entity, string):
    if (string == '' or entity == ''):
        return False
    return string in entity


scoresMap = {}


def compare_each(arr):
    scoresMap = {}
    for description_word in arr:
        for domain in domain_entities:
            for domain_word in domain_entities[domain]:
                if (isSimilar(description_word, domain_word)):
                    val = 1
                    if (scoresMap.get(domain) is not None):
                        val = scoresMap.get(domain) + 1

                    scoresMap[domain] = val

    for key in scoresMap:
        print(areas[key], ':', scoresMap[key])


tokenize_text()
