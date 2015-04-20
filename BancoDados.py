import mysql.connector

class BancoMySQL():

    def __init__(self, usuario, senha, host, banco):
        self.conexao = mysql.connector.connect(user=usuario, password=senha, host='127.0.0.1', database=banco, buffered=True)

    def seleciona_paragrafos_corpus(self):

        cursor_paragrafos = self.conexao.cursor()

        query_paragrafos =  ('select paragrafo, polaridade from noticias_x_paragrafo ncp join noticias n on n.id_noticia = ncp.id_noticia where polaridade in (\'NG\',\'NE\',\'PO\') and n.ind_corpus = \'S\'')
        cursor_paragrafos.execute(query_paragrafos,)

        return cursor_paragrafos
        # retorno = list()

        # retorno.append(('Isto resolve a crise.','PO'))
        # retorno.append(('Isto resolve a crise lentamente.','NE'))
        # retorno.append(('Isto intensifica a crise.','NG'))

        # return retorno

    def seleciona_stopwords(self):

        cursor_stopwords = self.conexao.cursor()

        query_stopwords = ('select palavra from stopwords')
        cursor_stopwords.execute(query_stopwords,)

        return cursor_stopwords
