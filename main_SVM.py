from BancoDados import BancoMySQL
from Classificador import ClassificadorSVM

bd = BancoMySQL('garruda', 'garruda', '127.0.0.1', 'noticias')

def validacao_cruzada():

    folds = bd.seleciona_max_folds()

    for stemming in {True, False}:

        for stop_words in {True, False}:

            for representacao in {'CountVectorizer', 'TfidfVectorizer'}:

                if representacao == 'CountVectorizer':

                    for contagem in {True, False}:

                        for i in range(1, folds + 1):
                            C = ClassificadorSVM(bd)
                            C.monta_conjunto(stemming, stop_words, representacao, contagem, i)
                            C.treina_valida()

                else:
                    for i in range(1, folds + 1):
                        C = ClassificadorSVM(bd)
                        C.monta_conjunto(stemming, stop_words, representacao, False, i)
                        C.treina_valida()

validacao_cruzada()
