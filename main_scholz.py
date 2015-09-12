from BancoDados import BancoMySQL
from ClassificadorScholz import ClassificadorScholz

bd = BancoMySQL('garruda', 'garruda', '127.0.0.1', 'noticias', None)


def validacao_cruzada():

    folds = bd.seleciona_max_folds()

    # C = ClassificadorScholz(bd, False)
    # C.monta_conjunto(False, 0)
    # C.validacao_cruzada()

    for i in range(1, folds + 1):
        for stemming in {True, False}:
            C = ClassificadorScholz(bd, False)
            C.monta_conjunto(stemming, i)
            C.treina_valida()

validacao_cruzada()
