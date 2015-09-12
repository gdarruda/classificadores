import mysql.connector


class BancoMySQL():

    def __init__(self, usuario, senha, host, banco, entidade):
        self.conexao = mysql.connector.connect(user=usuario, password=senha, host='127.0.0.1', database=banco, buffered=True)
        self.entidade = entidade

    def atualiza_fold_paragrafo(self, id_noticia, id_paragrafo, fold):

        cursor_noticia = self.conexao.cursor()

        update_polaridade = ('update noticias_x_paragrafo set fold = %s where id_noticia = %s and id_paragrafo = %s')
        cursor_noticia.execute(update_polaridade, (fold, id_noticia, id_paragrafo))

        self.conexao.commit()

    def seleciona_paragrafos_corpus(self):

        cursor_paragrafos = self.conexao.cursor()

        if self.entidade is not None:
            filtro_entidade = ' and entidade = \'' + self.entidade + '\''
        else:
            filtro_entidade = ''

        query_paragrafos =  ('select paragrafo, polaridade, fold, entidade, id_perfil from noticias_x_paragrafo ncp join noticias n on n.id_noticia = ncp.id_noticia where polaridade in (\'NG\',\'NE\',\'PO\') and n.ind_corpus = \'S\''
                             + filtro_entidade)
        cursor_paragrafos.execute(query_paragrafos,)

        return cursor_paragrafos

    def seleciona_ids_corpus(self):

        cursor_paragrafos = self.conexao.cursor()

        if self.entidade is not None:
            filtro_entidade = ' and entidade = \'' + self.entidade + '\''
        else:
            filtro_entidade = ''

        query_paragrafos = ('select ncp.id_noticia, ncp.id_paragrafo from noticias_x_paragrafo ncp join noticias n on n.id_noticia = ncp.id_noticia where polaridade in (\'NG\',\'NE\',\'PO\') and n.ind_corpus = \'S\''
                            + filtro_entidade)
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

    def seleciona_max_folds(self):

        cursor_folds = self.conexao.cursor()

        query_folds = ('select max(fold)from noticias_x_paragrafo ncp')
        cursor_folds.execute(query_folds,)

        return cursor_folds.fetchone()[0]
