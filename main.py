from BancoDados import BancoMySQL
from Classificador import ClassificadorSVM, ClassificadorBayesiano

bd = BancoMySQL('garruda', 'garruda', '127.0.0.1', 'noticias')

def monta_classificador():

    # C = ClassificadorSVM(bd)
    # C.monta_conjunto(True,False,'CountVectorizer')
    # C.validacao_cruzada()

    # C = ClassificadorSVM(bd)
    # C.monta_conjunto(True,False,'TfidfVectorizer')
    # C.validacao_cruzada()

    C = ClassificadorBayesiano(bd)
    C.monta_conjunto(True,True,'CountVectorizer')
    C.validacao_cruzada()

    C = ClassificadorBayesiano(bd)
    C.monta_conjunto(True,False,'TfidfVectorizer')
    C.validacao_cruzada()

monta_classificador()
