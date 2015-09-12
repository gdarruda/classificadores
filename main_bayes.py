from BancoDados import BancoMySQL
from Classificador import ClassificadorBayesiano

bd = BancoMySQL('garruda', 'garruda', '127.0.0.1', 'noticias', 'DILMA')

def validacao_cruzada():

    folds = bd.seleciona_max_folds()

    for stemming in {True, False}:

        for stop_words in {False}:

            for representacao in {'CountVectorizer'}:

                if representacao == 'CountVectorizer':

                    for contagem in {True, False}:

                        for i in range(1, folds + 1):
                            C = ClassificadorBayesiano(bd)
                            C.monta_conjunto(stemming, stop_words, representacao, contagem, i)
                            C.treina_valida()


def ve_tamanho():
    C = ClassificadorBayesiano(bd)
    C.monta_conjunto(False, False, 'CountVectorizer', True, 0)
    C.monta_conjunto(True, False, 'CountVectorizer', True, 0)

# validacao_cruzada()
ve_tamanho()
