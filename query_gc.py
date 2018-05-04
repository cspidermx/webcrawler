import localdb


def printrecords(cur):
    i = 0
    cur.execute('SELECT * FROM GifData where (TAGS LIKE "%|your so boring|%") ')

    for registro in cur:
        i += 1
        # print(i, registro)
        print(registro[1], registro[2], registro[12])

    print(i, " - registros")


def tagnumbers(cur):
    i = 0
    tgd = {}
    cur.execute('SELECT * FROM GifData')
    for registro in cur:
        i += 1
        cant = len(registro[12].split('|'))
        avgv = registro[2] / cant
        for tag in registro[12].split('|'):
            if tag not in tgd:
                tgd[tag] = (1, avgv)
            else:
                tgd[tag] = (tgd[tag][0] + 1, tgd[tag][1] + avgv)

    prefix = 'hyperrpg'
    with open(prefix + 'Query.csv', 'wb') as csvfile:
        for wrd, val in tgd.items():
            line = wrd + ', ' + str(val[0]) + ', ' + str(val[1]) + '\n'
            lineu = line.encode('utf-8', 'ignore')
            csvfile.write(lineu)
    print(i, " - registros")


db = 'hypergifsdata.db'  # ULD(4) ULM(5) ULY(6)

ldb = localdb.dbopen(db)
cur = ldb.cursor()

# printrecords(cur)
tagnumbers(cur)

cur.close()
localdb.dbclose(ldb)
