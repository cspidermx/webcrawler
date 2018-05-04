import sqlite3


def dbopen(db):
    try:
        con = sqlite3.connect(db)
    except:
        return None
    return con


def dbclose(con):
    try:
        con.close
    except:
        return False
    return True


def dbinsert(c, data):
    cur = c.cursor()
    reg = (data['GifID'], data['GIF URL'], data['VIEWS'], data['RATING'], data['ULD'], data['ULM'], data['ULY'],
           data['ULT'], data['TRD'], data['TRM'], data['TRY'], data['TRT'], data['TAGS'])
    cur.execute("INSERT INTO GifData VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", reg)
    c.commit()
    cur.close()


def dbcleandata(c):
    cur = c.cursor()
    cur.execute('DELETE FROM GifData')
    c.commit()
    cur.close()



