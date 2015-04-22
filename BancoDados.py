import mysql.connector

class BancoMySQL():

    def __init__(self, usuario, senha, host, banco):
        self.conexao = mysql.connector.connect(user=usuario, password=senha, host='127.0.0.1', database=banco, buffered=True)

    def seleciona_paragrafos_corpus(self):

        cursor_paragrafos = self.conexao.cursor()

        query_paragrafos =  ('select paragrafo, polaridade from noticias_x_paragrafo ncp join noticias n on n.id_noticia = ncp.id_noticia where polaridade in (\'NG\',\'NE\',\'PO\') and n.ind_corpus = \'S\'')
        cursor_paragrafos.execute(query_paragrafos,)

        return cursor_paragrafos

    def seleciona_stopwords(self):

        cursor_stopwords = self.conexao.cursor()

        query_stopwords = ('select palavra from stopwords')
        cursor_stopwords.execute(query_stopwords,)

        return cursor_stopwords

    def seleciona_tweets(self):

        cursor_tweets = self.conexao.cursor()

        query_tweets = ('select id_noticia, tweet from noticias')
        cursor_tweets.execute(query_tweets)

        return cursor_tweets

    def atualiza_polaridade_tweet(self, id_noticia, polaridade):

        cursor_noticia = self.conexao.cursor()

        update_polaridade = ('update noticias set polaridade_tweet = %s where id_noticia = %s')
        cursor_noticia.execute(update_polaridade,(polaridade, id_noticia))

        self.conexao.commit()
