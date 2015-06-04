from BancoDados import BancoMySQL
from ClassificadorScholz import ClassificadorScholz

bd = BancoMySQL('garruda', 'garruda', '127.0.0.1', 'noticias')


def validacao_cruzada():

    folds = bd.seleciona_max_folds()

    for i in range(1, folds):
        for stemming in {False}:
            C = ClassificadorScholz(bd, True)
            C.monta_conjunto(stemming, i)
            print(C.treina_valida())

validacao_cruzada()
