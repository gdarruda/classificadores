from BancoDados import BancoMySQL
from Classificador import Classificador

bd = BancoMySQL('garruda', 'garruda', '127.0.0.1', 'noticias')

def monta_classificador():

    C = Classificador(bd)
    C.monta_conjunto()

monta_classificador()
