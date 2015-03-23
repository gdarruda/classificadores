from nltk.tokenize import RegexpTokenizer
from nltk.stem import RSLPStemmer
from sklearn import svm
from sklearn import naive_bayes
from sklearn import cross_validation
import sklearn.feature_extraction.text


class Classificador():

    depara_polaridade = {'PO':1, 'NE':2, 'NG':3}

    def __init__(self, bd):
        self.bd = bd
        self.matriz_caracteristicas = None
        self.rotulos = list()

    def lista_stopwords(self, stop_words):

        if not stop_words:
            return list()

        cursor_stopwords = self.bd.seleciona_stopwords()
        lista_stopwords = list()

        for (palavra,) in cursor_stopwords:
            lista_stopwords.append(palavra)

        return lista_stopwords

    def monta_conjunto(self, stemming, stop_words, tipo_caracteristicas, binario):

        print ("Stemming:" + str(stemming))
        print ("Stop Words:" + str(stop_words))
        print ("Representacao:" + tipo_caracteristicas)
        print ("Binario:" + str(binario))

        cursor_paragrafos = self.bd.seleciona_paragrafos_corpus()

        tokenizer = RegexpTokenizer(r'\w+') #Tokenizer que considera apenas alfa-numerico

        stemmer = RSLPStemmer()

        #Cria dinamicamente o vetor dependendo do tipo de contagem
        vectorizer = getattr(sklearn.feature_extraction.text, tipo_caracteristicas)(binary=binario, stop_words=self.lista_stopwords(stop_words))

        paragrafos = list()

        for (paragrafo, polaridade) in cursor_paragrafos:

            if stemming:
                tokens_paragrafo = tokenizer.tokenize(paragrafo)

                for (i, palavra) in enumerate(tokens_paragrafo):
                    tokens_paragrafo[i] = stemmer.stem(palavra)

                paragrafos.append(' '.join(tokens_paragrafo))
            else:
                paragrafos.append(paragrafo)

            self.rotulos.append(Classificador.depara_polaridade[polaridade])

        #Matriz com os vetores de caracteristica
        self.matriz_caracteristicas = vectorizer.fit_transform(paragrafos)

class ClassificadorSVM(Classificador):

    def validacao_cruzada(self):

        classificador_svm = svm.LinearSVC()
        scores = cross_validation.cross_val_score(classificador_svm, self.matriz_caracteristicas, self.rotulos, cv=10)
        print ('SVM: ' + str(scores.mean()))

class ClassificadorBayesiano(Classificador):

    def validacao_cruzada(self):

        classificador_nb = naive_bayes.MultinomialNB(fit_prior=False)
        scores = cross_validation.cross_val_score(classificador_nb, self.matriz_caracteristicas, self.rotulos, cv=10)
        print ('Bayes: ' + str(scores.mean()))
