from nltk.tokenize import RegexpTokenizer
from nltk.stem import RSLPStemmer
from sklearn import svm
from sklearn import naive_bayes
from sklearn import cross_validation
from sklearn.decomposition import PCA
import sklearn.feature_extraction.text
import matplotlib.pyplot as plt
import numpy as np

class Classificador():

    depara_polaridade = {'PO':0, 'NE':1, 'NG':2}

    def __init__(self, bd):
        self.bd = bd
        self.matriz_caracteristicas = None
        self.rotulos = list()

    def lista_stopwords(self, stop_words):

        if not stop_words:
            return list()

        cursor_stopwords = self.bd.seleciona_stopwords()
        lista_stopwords = list()

        for palavra in cursor_stopwords:
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

    def gera_pca(self):

        pca = PCA(n_components=2)

        X = pca.fit(self.matriz_caracteristicas).transform(self.matriz_caracteristicas)
        y = np.array(self.rotulos)

        target_names = np.array(['Positivo','Neutro','Negativo'])

        plt.figure()
        for c, i, target_name in zip("rgb", [0, 1, 2], target_names):
            plt.scatter(X[y == i, 0], X[y == i, 1], c=c, label=target_name)
        plt.legend()
        plt.title('Polaridade')

        plt.show()


class ClassificadorSVM(Classificador):

    def validacao_cruzada(self):

        classificador_svm = svm.LinearSVC()
        scores = cross_validation.cross_val_score(classificador_svm, self.matriz_caracteristicas, self.rotulos, cv=10)
        print ('SVM: ' + str(scores.mean()))

    def gera_pca(self):

        self.matriz_caracteristicas =  self.matriz_caracteristicas.toarray()

        Classificador.gera_pca(self)

class ClassificadorBayesiano(Classificador):

    def validacao_cruzada(self):

        classificador_nb = naive_bayes.MultinomialNB(fit_prior=False)
        scores = cross_validation.cross_val_score(classificador_nb, self.matriz_caracteristicas, self.rotulos, cv=10)
        print ('Bayes: ' + str(scores.mean()))

    def gera_pca(self):

        self.matriz_caracteristicas =  self.matriz_caracteristicas.toarray()

        Classificador.gera_pca(self)
