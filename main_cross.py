from BancoDados import BancoMySQL
from Classificador import ClassificadorSVM

bd = BancoMySQL('garruda', 'garruda', '127.0.0.1', 'noticias')

C = ClassificadorSVM(bd)
C.gera_folds(10)
