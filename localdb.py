import sqlite3


def open(db):
    try:
        con = sqlite3.connect(db)
    except:
        return None
    return con


def close(con):
    try:
        con.close
    except:
        return False
    return True


def insert(c, data):
    cur = c.cursor()
    reg = (data['ID'], data['GIF URL'], data['VIEWS'], data['RATING'], data['ULD'], data['ULM'], data['ULY'],
           data['ULT'], data['TRD'], data['TRM'], data['TRY'], data['TRT'], data['TAGS'])
    cur.execute("INSERT INTO GifData VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", reg)
    c.commit()
    cur.close()


def cleandata(c):
    cur = c.cursor()
    cur.execute('DELETE FROM GifData')
    c.commit()
    cur.close()


db = 'hypergifsdata.db'

ldb = open(db)
cur = ldb.cursor()
i = 0
cur.execute('SELECT * FROM GifData where (TAGS not like "%hyperrpg%") ')
for registro in cur:
    i += 1
    # print(i, registro)
    print(registro[1], registro[2], registro[12])
cur.close()
close(ldb)
