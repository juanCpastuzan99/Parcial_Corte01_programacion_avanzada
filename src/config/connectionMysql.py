import pymysql
import pymysql.cursors

def get_connection_mysql():
    return pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='',
        db='acortador_enlaces',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor  # ← esta línea reemplaza dictionary=True
    )