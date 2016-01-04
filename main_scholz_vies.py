from BancoDados import BancoMySQL
from ClassificadorScholz import ClassificadorScholz

bd = BancoMySQL('garruda', 'garruda', '127.0.0.1', 'noticias', None)


def validacao_cruzada():

    folds = bd.seleciona_max_folds()

    for i in range(1, folds + 1):
        for stemming in {False, True}:
            C = ClassificadorScholz(bd, True)
            C.monta_conjunto(stemming, i)
            C.treina_valida()

validacao_cruzada()
