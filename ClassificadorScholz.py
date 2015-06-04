from Classificador import ClassificadorSVM, Classificador
from nltk.stem import RSLPStemmer
import nlpnet
import nltk
import math


class ClassificadorScholz(ClassificadorSVM):

    depara_classes = {'V': 'VERB', 'VAUX': 'VERB',
                      'N': 'NOME', 'NPROP': 'NOME', 'PROSUB': 'NOME',
                      'ADV': 'ADV',
                      'ADJ': 'ADJ', 'PROADJ': 'ADJ', 'PCP': 'ADJ'}

    depara_rotulos = {0: 'PO', 1: 'NE', 2: 'NG'}

    def __init__(self, bd, ind_vies):
        ClassificadorSVM.__init__(self, bd)
        nlpnet.set_data_dir('pos-pt')
        self.tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')
        self.tagger = nlpnet.POSTagger()
        self.grafo = {}
        self.stemmer = RSLPStemmer()
        self.stemming = False
        self.entidades = {}
        self.dim_entidade = 0
        self.perfis = {}
        self.dim_perfil = 0
        self.seleciona_entidades_perfis()
        self.ind_vies = ind_vies

    def seleciona_entidades_perfis(self):

        for (paragrafo, polaridade, fold_paragrafo, entidade, id_perfil) in self.bd.seleciona_paragrafos_corpus():

            if entidade not in self.entidades:
                self.entidades[entidade] = len(self.entidades) + 1

            if id_perfil not in self.perfis:
                self.perfis[id_perfil] = len(self.perfis) + 1

        # Tamanho da representacao maxima
        self.dim_entidade = len(self.decimal_binario(len(self.entidades), 0))
        self.dim_perfil = len(self.decimal_binario(len(self.perfis), 0))

    def decimal_binario(self, numero, tamanho):

        if numero == 0:

            prefixo = []

            while tamanho > 0:
                prefixo.append(0)
                tamanho -= 1

            return prefixo

        resultado, digito = divmod(numero, 2)

        numero = self.decimal_binario(resultado, tamanho - 1)
        numero.append(digito)

        return numero

    def monta_chave(self, palavra, classe):

        if self.stemming:
            chave = self.stemmer.stem(palavra)
        else:
            chave = palavra

        return chave.upper() + '_' + classe

    def classe_valida(self, chave):

        classe = chave[chave.index('_') + 1:]

        if classe in ClassificadorScholz.depara_classes:
            return (True, ClassificadorScholz.depara_classes[classe])
        else:
            return (False, '')

    def adiciona_grafo(self, chave_1, chave_2, polaridade, cont_chamadas):

        if cont_chamadas > 2:
            return

        if chave_1 in self.grafo:
            arestas = self.grafo[chave_1]
        else:
            arestas = dict()

        if chave_2 in arestas:
            tripla = arestas[chave_2]
        else:
            tripla = (0, 0, 0)

        positivo, neutro, negativo = tripla

        if polaridade == 'PO':
            positivo += 1
        elif polaridade == 'NE':
            neutro += 1
        elif polaridade == 'NG':
            negativo += 1

        tripla = (positivo, neutro, negativo)

        arestas[chave_2] = tripla
        self.grafo[chave_1] = arestas

        cont_chamadas += 1
        self.adiciona_grafo(chave_2, chave_1, polaridade, cont_chamadas)

    def tag_paragrafo(self, paragrafo):

        paragrafo_taggeado = list()

        for sentenca in self.tokenizer.tokenize(paragrafo):

            palavras = self.tagger.tag(sentenca)

            paragrafo_taggeado.extend(palavras[0])

        return paragrafo_taggeado

    def monta_conjunto(self, stemming, fold):

        self.stemming = stemming
        print ("Stemming:" + str(stemming))

        for (paragrafo, polaridade, fold_paragrafo, entidade, id_perfil) in self.bd.seleciona_paragrafos_corpus():

            if fold_paragrafo == fold:
                continue

            paragrafo_taggeado = self.tag_paragrafo(paragrafo)

            for (i, (palavra_1, classe_1)) in enumerate(paragrafo_taggeado):

                chave_1 = self.monta_chave(palavra_1, classe_1)

                for (palavra_2, classe_2) in paragrafo_taggeado[i+1:]:

                    chave_2 = self.monta_chave(palavra_2, classe_2)

                    self.adiciona_grafo(chave_1, chave_2, polaridade, 1)

        if fold == 0:
            self.matriz_caracteristicas = []
            self.rotulos = []
        else:
            self.treino_caracteristicas = []
            self.treino_rotulos = []

            self.validacao_caracteristicas = []
            self.validacao_rotulos = []

        for (paragrafo, polaridade, fold_paragrafo, entidade, id_perfil) in self.bd.seleciona_paragrafos_corpus():

            lista_caracteristicas = self.extai_metricas(paragrafo, entidade, id_perfil)

            if fold == 0:
                self.matriz_caracteristicas.append(lista_caracteristicas)
                self.rotulos.append(Classificador.depara_polaridade[polaridade])
            elif fold_paragrafo == fold:
                self.validacao_caracteristicas.append(lista_caracteristicas)
                self.validacao_rotulos.append(Classificador.depara_polaridade[polaridade])
            else:
                self.treino_caracteristicas.append(lista_caracteristicas)
                self.treino_rotulos.append(Classificador.depara_polaridade[polaridade])

    def busca_grafo(self, chave_1, chave_2):

        retorno_falso = (False, (0, 0, 0))

        if chave_1 in self.grafo:
            arestas = self.grafo[chave_1]

            if chave_2 in arestas:
                return (True, arestas[chave_2])

        return retorno_falso

    def adiciona_subgrafo(self, chave_1, chave_2, subgrafo):

        encontrou, tripla = self.busca_grafo(chave_1, chave_2)

        if not encontrou:
            return

        if chave_1 in subgrafo:
            arestas = subgrafo[chave_1]
        else:
            arestas = dict()

        arestas[chave_2] = tripla
        subgrafo[chave_1] = arestas

    def atualiza_tupla(self, totalizador, nova_relacao):

        positivo_tot, neutro_tot, negativo_tot = totalizador
        positivo, neutro, negativo = nova_relacao

        positivo_tot = positivo_tot + positivo
        neutro_tot = neutro_tot + neutro
        negativo_tot = negativo_tot + negativo

        return (positivo_tot, neutro_tot, negativo_tot)

    def positividade(self, totalizador):

        positivo, neutro, negativo = totalizador

        if positivo == 0:
            return .0
        else:
            return float(positivo) / float(positivo + negativo)

    def negatividade(self, totalizador):

        positivo, neutro, negativo = totalizador

        if negativo == 0:
            return .0
        else:
            return float(negativo) / float(positivo + negativo)

    def subjetividade(self, totalizador):

        positivo, neutro, negativo = totalizador

        if positivo + negativo == 0:
            return .0
        else:
            return float(positivo + negativo) / float(positivo + neutro + negativo)

    def neutralidade(self, totalizador):

        positivo, neutro, negativo = totalizador

        if neutro == 0:
            return .0
        else:
            return float(neutro) / float(positivo + neutro + negativo)

    def entropia_polaridade(self, totalizador):

        positividade = self.positividade(totalizador)
        negatividade = self.negatividade(totalizador)

        if positividade + negatividade == 0:
            return 0
        elif positividade == 0 and negatividade > 0:
            return -1
        elif negatividade == 0 and positividade > 0:
            return 1
        elif negatividade <= positividade:
            return 1 + positividade * math.log(positividade, 2)
        else:
            return -1 - negatividade * math.log(negatividade, 2)

    def entropia_subjetividade(self, totalizador):

        subjetividade = self.subjetividade(totalizador)
        neutralidade = self.neutralidade(totalizador)

        if subjetividade + neutralidade == 0:
            return 0
        elif subjetividade == 0 and neutralidade > 0:
            return -1
        elif neutralidade == 0 and subjetividade > 0:
            return 1
        if neutralidade <= subjetividade:
            return 1 + subjetividade * math.log(subjetividade, 2)
        else:
            return -1 - neutralidade * math.log(neutralidade, 2)

    def extai_metricas(self, paragrafo, entidade, id_perfil):

        paragrafo_taggeado = self.tag_paragrafo(paragrafo)
        subgrafo = dict()
        caracteristicas = {'POL_VERB': .0, 'POL_NOME': .0, 'POL_ADV': .0, 'POL_ADJ': .0,
                           'SUB_VERB': .0, 'SUB_NOME': .0, 'SUB_ADV': .0, 'SUB_ADJ': .0}
        totalizadores = {'VERB': (0, 0, 0), 'NOME': (0, 0, 0), 'ADV': (0, 0, 0), 'ADJ': (0, 0, 0)}

        for (i, (palavra_1, classe_1)) in enumerate(paragrafo_taggeado):

            chave_1 = self.monta_chave(palavra_1, classe_1)

            for (palavra_2, classe_2) in paragrafo_taggeado[i+1:]:

                chave_2 = self.monta_chave(palavra_2, classe_2)
                self.adiciona_subgrafo(chave_1, chave_2, subgrafo)

        for chave_1 in subgrafo.keys():

            for chave_2 in subgrafo[chave_1].keys():

                classe_valida_1, classe_1 = self.classe_valida(chave_1)
                classe_valida_2, classe_2 = self.classe_valida(chave_2)

                if classe_valida_1 and classe_valida_2:

                    totalizadores[classe_1] = self.atualiza_tupla(totalizadores[classe_1], subgrafo[chave_1][chave_2])

                    if classe_1 != classe_2:

                        totalizadores[classe_2] = self.atualiza_tupla(totalizadores[classe_2], subgrafo[chave_1][chave_2])

        for classe in totalizadores.keys():

            caracteristicas['POL_' + classe] = self.entropia_polaridade(totalizadores[classe])
            caracteristicas['SUB_' + classe] = self.entropia_subjetividade(totalizadores[classe])

        lista_caracteristicas = list()
        lista_caracteristicas.append(caracteristicas['POL_VERB'])
        lista_caracteristicas.append(caracteristicas['POL_NOME'])
        lista_caracteristicas.append(caracteristicas['POL_ADV'])
        lista_caracteristicas.append(caracteristicas['POL_ADJ'])

        lista_caracteristicas.append(caracteristicas['SUB_VERB'])
        lista_caracteristicas.append(caracteristicas['SUB_NOME'])
        lista_caracteristicas.append(caracteristicas['SUB_ADV'])
        lista_caracteristicas.append(caracteristicas['SUB_ADJ'])

        if self.ind_vies:
            # lista_caracteristicas.extend(self.decimal_binario(self.entidades[entidade], self.dim_entidade))
            lista_caracteristicas.extend(self.decimal_binario(self.perfis[id_perfil], self.dim_perfil))

        return (lista_caracteristicas)

    def gera_csv(self):

        arquivo_csv = open("data_set.csv", "w")
        arquivo_csv.write('POL_VERB,POL_NOME,POL_ADV,POL_ADJ,SUB_VERB,SUB_NOME,SUB_ADV,SUB_ADJ,CLASSE\n')

        for i in range(0, len(self.rotulos)):

            rotulo = ClassificadorScholz.depara_rotulos[self.rotulos[i]]
            lista_caracteristicas = list()

            for caracteristica in self.matriz_caracteristicas[i]:
                lista_caracteristicas.append(str(caracteristica))

            lista_caracteristicas.append(rotulo)

            arquivo_csv.write(','.join(lista_caracteristicas) + '\n')

        arquivo_csv.close()

    def gera_pca(self):

        Classificador.gera_pca(self)

    def classifica_tweets(self):

        self.treina()

        for (id_noticia, tweets) in self.bd.seleciona_tweets():

            caracteristicas = self.extai_metricas(tweets)
            resultado = self.classifica(caracteristicas)

            self.bd.atualiza_polaridade_tweet(id_noticia, ClassificadorScholz.depara_rotulos[resultado])
