# -*- coding: utf-8 -*-
from db_utils import conn_init, conn_close
import uuid
from datetime import datetime

### Variables à changer ###
env = "esus_dev"
object_types = ["prestations_catalog"]
filtres = [
    {"label": "Product Title", "name": "product_title"},
]
sort_order = '99'
val = '0'
### FIN Variables ###

conn, tunnel = conn_init(env)
cur = conn.cursor()
i = 0
filtres_r = []
print ("***** Debut esus/column-gen.py *****")

# Case 1 : For columns generation
i = 1
for object_type in object_types:
    cur.execute("SELECT Distinct user_id FROM filtres WHERE (deleted_at is NULL OR deleted_at = '') AND type = %s", object_type)
    conn.commit()
    users = cur.fetchall()
    for u in users:
        print (str(i) + " - " + u["user_id"])
        f_id = str(uuid.uuid4())[:-2]
        j = 1
        for f in filtres:
            filtre_id = f_id
            if j< 10:
                filtre_id += "0"
            filtre_id += str(j)
            filtres_r.append((filtre_id, '0', u["user_id"], f["name"], f["label"], object_type, sort_order, val, '', '0', u["user_id"], u["user_id"]))
            j += 1
        i += 1

# Case 2 : For project stages generation
# is_signed = 0
# cur.execute("SELECT id FROM accounts")
# conn.commit()
# accounts = cur.fetchall()
# i = 1
# for a in accounts:
#     print (str(i) + " - " + a["id"])
#     name = str(uuid.uuid4())
#     filtre_id = str(uuid.uuid4())
#     filtres_r.append((filtre_id, a["id"], '0', name, label, object_type, 1, 1, '#000000', is_signed, '0', '0'))
#     conn.commit()
#     i = i + 1


# Excecute many
cur.executemany("INSERT INTO filtres (id, account_id, user_id, name, label, type, sort_order, val, color, is_signed, created_by, updated_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", filtres_r)
conn.commit()
conn_close(conn, tunnel)