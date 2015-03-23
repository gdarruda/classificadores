import pymysql

class BancoMySQL():

    def __init__(self, usuario, senha, host, banco):
        self.conexao = pymysql.connect(host=host, unix_socket='/tmp/mysql.sock', user=usuario, passwd=senha, db=banco, init_command="set names utf8")

    def seleciona_paragrafos_corpus(self):

        cursor_paragrafos = self.conexao.cursor()

        query_paragrafos =  ('select paragrafo, polaridade from noticias_x_paragrafo where polaridade in (\'NG\',\'NE\',\'PO\')')
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
