import pymysql
import pymysql.cursors

def connection(config):
    conn = pymysql.connect(host=config.MYSQL_DATABASE_HOST,
                            user = config.MYSQL_DATABASE_USER,
                            passwd = config.MYSQL_DATABASE_PASSWORD,
                            db = config.MYSQL_DATABASE_DB,
                            cursorclass = pymysql.cursors.DictCursor,
                            charset = 'utf8')
    c = conn.cursor()
    return c, conn
