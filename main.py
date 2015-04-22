from BancoDados import BancoMySQL
from Classificador import ClassificadorSVM, ClassificadorBayesiano
from ClassificadorScholz import ClassificadorScholz

bd = BancoMySQL('garruda', 'garruda', '127.0.0.1', 'noticias')

def monta_classificador():

    # for stemming in {True, False}:

    #     for stop_words in {True, False}:

    #         for representacao in {'CountVectorizer', 'TfidfVectorizer'}:

    #             if representacao == 'CountVectorizer':

    #                 for contagem in {True,False}:

    #                     C = ClassificadorSVM(bd)
    #                     C.monta_conjunto(stemming,stop_words,representacao,contagem)
    #                     C.validacao_cruzada()

    #                     C = ClassificadorBayesiano(bd)
    #                     C.monta_conjunto(stemming,stop_words,representacao,contagem)
    #                     C.validacao_cruzada()
    #             else:
    #                 C = ClassificadorSVM(bd)
    #                 C.monta_conjunto(stemming,stop_words,representacao,False)
    #                 C.validacao_cruzada()

    #                 C = ClassificadorBayesiano(bd)
    #                 C.monta_conjunto(stemming,stop_words,representacao,False)
    #                 C.validacao_cruzada()

    # for stemming in {True, False}:
    #     C = ClassificadorScholz(bd)
    #     C.monta_conjunto(stemming)
    #     C.validacao_cruzada()

    C = ClassificadorScholz(bd)
    C.monta_conjunto(False)
    # C.validacao_cruzada()
    C.classifica_tweets()
    # C.treina()
    # C.gera_pca()
    # C.gera_csv()

monta_classificador()
