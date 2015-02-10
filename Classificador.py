from nltk.tokenize import RegexpTokenizer
from nltk.stem import RSLPStemmer
from sklearn.feature_extraction.text import TfidfVectorizer


class Classificador():

    def __init__(self, bd):
        self.bd = bd

    def monta_conjunto(self):

        cursor_paragrafos = self.bd.seleciona_paragrafos_corpus()

        tokenizer = RegexpTokenizer(r'\w+') #Tokenizer que considera apenas alfanumerico

        stemmer = RSLPStemmer()

        vectorizer = TfidfVectorizer()

        paragrafos = list()

        for (paragrafo, polaridade) in cursor_paragrafos:

            tokens_paragrafo = tokenizer.tokenize(paragrafo)

            #Faz o stemming das palavras
            for (i, palavra) in enumerate(tokens_paragrafo):
                tokens_paragrafo[i] = stemmer.stem(palavra)

            paragrafos.append(tokens_paragrafo)
