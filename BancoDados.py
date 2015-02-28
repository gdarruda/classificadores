import pymysql

class BancoMySQL():

    def __init__(self, usuario, senha, host, banco):
        self.conexao = pymysql.connect(host=host, unix_socket='/tmp/mysql.sock', user=usuario, passwd=senha, db=banco)

    def seleciona_paragrafos_corpus(self):

        cursor_paragrafos = self.conexao.cursor()

        query_paragrafos =  ('select paragrafo, polaridade from noticias_x_paragrafo where polaridade in (\'NG\',\'NE\',\'PO\')')
        cursor_paragrafos.execute(query_paragrafos,)

        return cursor_paragrafos

    def seleciona_stopwords(self):

        cursor_stopwords = self.conexao.cursor()

        query_stopwords = ('select palavra from stopwords')
        cursor_stopwords.execute(query_stopwords,)

        return cursor_stopwords
