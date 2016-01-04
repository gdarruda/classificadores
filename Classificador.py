from nltk.tokenize import RegexpTokenizer
from nltk.stem import RSLPStemmer
from sklearn import svm
from sklearn import naive_bayes
from sklearn import cross_validation
from sklearn import metrics
from sklearn.decomposition import PCA
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.grid_search import GridSearchCV
import sklearn.feature_extraction.text
import matplotlib.pyplot as plt
import numpy as np


class Classificador():

    depara_polaridade = {'PO': 0, 'NE': 1, 'NG': 2}

    def __init__(self, bd):
        self.bd = bd
        self.matriz_caracteristicas = None
        self.rotulos = []

        self.treino_caracteristicas = []
        self.treino_rotulos = []
        self.validacao_caracteristicas = []
        self.validacao_rotulos = []

    def lista_stopwords(self, stop_words):

        if not stop_words:
            return list()

        cursor_stopwords = self.bd.seleciona_stopwords()
        lista_stopwords = set()

        for palavra in cursor_stopwords:
            lista_stopwords.add(palavra)

        return lista_stopwords

    def monta_conjunto(self, stemming, stop_words, tipo_caracteristicas, binario, fold):

        print ("Stemming:" + str(stemming))
        print ("Stop Words:" + str(stop_words))
        print ("Representacao:" + tipo_caracteristicas)
        print ("Binario:" + str(binario))

        cursor_paragrafos = self.bd.seleciona_paragrafos_corpus()

        tokenizer = RegexpTokenizer(r'\w+')  # Tokenizer que considera apenas alfa-numerico

        stemmer = RSLPStemmer()

        vocabulario = {}

        lista_stopwords = self.lista_stopwords(stop_words)

        if fold == 0:
            paragrafos = []
        else:
            treino_paragrafos = []
            validacao_paragrafos = []

        for (paragrafo, polaridade, fold_paragrafo, entidade, id_perfil) in cursor_paragrafos:

            paragrafo_concatenado = ''

            tokens_paragrafo = tokenizer.tokenize(paragrafo)

            for (i, palavra) in enumerate(tokens_paragrafo):

                palavra = palavra.lower()

                if palavra in lista_stopwords:
                    continue

                if stemming:
                    tokens_paragrafo[i] = stemmer.stem(palavra)
                else:
                    tokens_paragrafo[i] = palavra

                if tokens_paragrafo[i] not in vocabulario:
                    vocabulario[tokens_paragrafo[i]] = (len(vocabulario) - 1) + 1

                paragrafo_concatenado = ' '.join(tokens_paragrafo)

            if fold == 0:
                paragrafos.append(paragrafo_concatenado)
                self.rotulos.append(Classificador.depara_polaridade[polaridade])
            elif fold_paragrafo == fold:
                validacao_paragrafos.append(paragrafo_concatenado)
                self.validacao_rotulos.append(Classificador.depara_polaridade[polaridade])
            else:
                treino_paragrafos.append(paragrafo_concatenado)
                self.treino_rotulos.append(Classificador.depara_polaridade[polaridade])

        # Cria dinamicamente o vetor dependendo do tipo de contagem
        vectorizer = getattr(sklearn.feature_extraction.text, tipo_caracteristicas)(
            binary=binario, vocabulary=vocabulario)

        if fold == 0:
            self.matriz_caracteristicas = vectorizer.fit_transform(paragrafos)
        else:
            self.treino_caracteristicas = vectorizer.fit_transform(treino_paragrafos)
            self.validacao_caracteristicas = vectorizer.fit_transform(validacao_paragrafos)

    def gera_pca(self):

        pca = PCA(n_components=2)

        X = pca.fit(self.matriz_caracteristicas).transform(self.matriz_caracteristicas)
        y = np.array(self.rotulos)

        target_names = np.array(['Positivo', 'Neutro', 'Negativo'])

        plt.figure()
        for c, i, target_name in zip("rgb", [0, 1, 2], target_names):
            plt.scatter(X[y == i, 0], X[y == i, 1], c=c, label=target_name)
        plt.legend()
        plt.title('Polaridade')

        plt.show()

    def treina_valida(self):

        self.classificador.fit(self.treino_caracteristicas, self.treino_rotulos)
        predicoes = self.classificador.predict(self.validacao_caracteristicas)

        acuracia = metrics.accuracy_score(self.validacao_rotulos, predicoes)
        precisao = metrics.precision_score(self.validacao_rotulos, predicoes, average='macro')
        recall = metrics.recall_score(self.validacao_rotulos, predicoes, average='macro')

        print (acuracia)
        print (precisao)
        print (recall)

    def treina_valida_full(self):
        self.classificador.fit(self.matriz_caracteristicas, self.rotulos)
        return self.classificador.score(self.matriz_caracteristicas, self.rotulos)

    def classifica(self, caracteristicas):
        return self.classificador.predict(caracteristicas)[0]

    def gera_folds(self, quantidade):

        lista_paragrafos = []

        for chave in self.bd.seleciona_ids_corpus():
            lista_paragrafos.append(chave)

        kfolds = cross_validation.KFold(n=len(lista_paragrafos), n_folds=quantidade, shuffle=True, random_state=None)

        for (i, (indice_treino, indice_teste)) in enumerate(kfolds):

            for indice in indice_teste:
                id_noticia, id_paragrafo = lista_paragrafos[indice]
                self.bd.atualiza_fold_paragrafo(id_noticia, id_paragrafo, i + 1)


class ClassificadorSVM(Classificador):

    def __init__(self, bd, c):
        Classificador.__init__(self, bd)
        self.classificador = svm.LinearSVC(C=c)

    def validacao_cruzada(self):

        # classificador_svm = svm.LinearSVC()
        # scores = cross_validation.cross_val_score(classificador_svm, self.matriz_caracteristicas, self.rotulos, cv=10)

        C_range = np.logspace(-2, 10, 13)
        gamma_range = np.logspace(-9, 3, 13)
        param_grid = dict(gamma=gamma_range, C=C_range)
        cv = StratifiedShuffleSplit(self.rotulos, n_iter=5, test_size=0.2, random_state=42)
        grid = GridSearchCV(svm.SVC(), param_grid=param_grid, cv=cv)
        grid.fit(self.matriz_caracteristicas, self.rotulos)

        # print ('SVM: ' + str(scores.mean()))

        print("The best parameters are %s with a score of %0.2f"
      % (grid.best_params_, grid.best_score_))


    def gera_pca(self):

        self.matriz_caracteristicas = self.matriz_caracteristicas.toarray()

        Classificador.gera_pca(self)


class ClassificadorBayesiano(Classificador):

    def __init__(self, bd):
        Classificador.__init__(self, bd)
        self.classificador = naive_bayes.MultinomialNB(fit_prior=False)

    def validacao_cruzada(self):

        classificador_nb = naive_bayes.MultinomialNB(fit_prior=False)
        scores = cross_validation.cross_val_score(classificador_nb, self.matriz_caracteristicas, self.rotulos, cv=10)
        print ('Bayes: ' + str(scores.mean()))

    def gera_pca(self):

        self.matriz_caracteristicas = self.matriz_caracteristicas.toarray()

        Classificador.gera_pca(self)
