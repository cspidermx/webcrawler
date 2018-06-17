import json
import certifi
import urllib3
import math
# from cps import cdmx
import sqlite3
from datetime import datetime
import os


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


daba = os.path.join(os.getcwd(), "databases\\gasolineras.sqlite")
dbcon = dbopen(daba)

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
# https://datos.gob.mx/desarrolladores
url = 'https://api.datos.gob.mx/v1/precio.gasolina.publico'
response = http.request('GET', url)
data = response.data.decode("utf-8-sig")
jsondata = json.loads(data.replace('\ufeff', ''))
pages = math.ceil(float(jsondata['pagination']['total']) / float(jsondata['pagination']['pageSize']))

# _id | calle | rfc | date_insert | regular | colonia | numeropermiso | fechaaplicacion | permisoid |
# longitude | latitude | premium | razonsocial | codigopostal | dieasel

gasdb = ('_id', 'calle', 'rfc', 'date_insert', 'regular', 'colonia', 'numeropermiso', 'fechaaplicacion', 'permisoid',
         'longitude', 'latitude', 'premium', 'razonsocial', 'codigopostal', 'dieasel')
floatitems = {'regular', 'premium', 'dieasel'}
timestampitems = {'date_insert', 'fechaaplicacion'}

cur = dbcon.cursor()
for x in range(2, int(pages) + 2):
    for dt in jsondata['results']:
        detallegas = dict.fromkeys(gasdb)
        detallegas = {**detallegas, **dt}  # Merge 2 dictionaries, keep data from second one
        for item in detallegas:
            if detallegas[item] == '':
                detallegas[item] = None
            if item in floatitems:
                if detallegas[item] is not None:
                    detallegas[item] = float(detallegas[item])
            if item in timestampitems:
                if detallegas[item] is not None:
                    try:
                        detallegas[item] = datetime.strptime(detallegas[item], '%Y-%m-%dT%H:%M:%S.%fZ')
                    except ValueError:
                        try:
                            detallegas[item] = datetime.strptime(
                                str(detallegas[item]).replace(' a. m.', '').replace(' p. m.', ''), '%d/%m/%Y %H:%M:%S')
                        except ValueError:
                            print(x, detallegas)
                            raise SystemExit(0)
        reg = (detallegas['_id'], detallegas['calle'], detallegas['rfc'], detallegas['date_insert'],
               detallegas['regular'], detallegas['colonia'], detallegas['numeropermiso'], detallegas['fechaaplicacion'],
               detallegas['permisoid'], detallegas['longitude'], detallegas['latitude'], detallegas['premium'],
               detallegas['razonsocial'], detallegas['codigopostal'], detallegas['dieasel'])
        cur.execute("INSERT INTO gasolineras VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", reg)
        '''if dt['codigopostal'] in cdmx:
            print(detallegas)'''
        print(x, ' - ', detallegas['_id'], detallegas['razonsocial'])
    if x <= pages:
        url = 'https://api.datos.gob.mx/v1/precio.gasolina.publico?page={}'.format(x)
        response = http.request('GET', url)
        data = response.data.decode("utf-8-sig")
        jsondata = json.loads(data.replace('\ufeff', ''))

dbcon.commit()
cur.close()
dbclose(dbcon)
