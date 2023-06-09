# -*- coding: utf-8 -*-
from db_utils import conn_init, conn_close
import uuid
from datetime import datetime

### Variables à changer ###
env = "esus_dev"
object_types = ["supplier_prestations"]
filtres = [
    {"label": "Title", "name": "product_title", 'default':'1'},
    {"label": "Quantity", "name": "quantity",'default':'1'},
    {"label": "Purchase price TTC", "name": "purchase_price_ttc", 'default': '1'},
    {"label": "Purchase price HT", "name": "purchase_price_ht", 'default': '0'},
    {"label": "Sales Price TTC", "name": "sales_price_ttc", 'default': '1'},
    {"label": "Sales Price HT", "name": "sales_price_ht", 'default': '0'},
    {"label": "VAT rate", "name": "vat_rate", 'default': '1'},
    {"label": "Slide", "name": "slide", 'default': '1'},
    {"label": "Created at", "name": "created_at", 'default': '1'},
    {"label": "Updated at", "name": "updated_at", 'default': '1'},
]
sort_order = '99'
### FIN Variables ###

conn, tunnel = conn_init(env)
cur = conn.cursor()
i = 0
filtres_r = []
print ("***** Debut esus/column-gen.py *****")

# UNCOMMENT TO ADD FIRST TIME
cur.execute("INSERT INTO filtres (id, account_id, user_id, name, label, type, sort_order, val, is_signed, created_by, updated_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (str(uuid.uuid4()), '0', '0', 'Sort order supplier', 'sort_order_supplier', 'supplier_prestations', '0', '0', '0', '0', '0'))


# # Case 1 : For columns generation
# i = 1
# for object_type in object_types:
#     cur.execute("SELECT Distinct user_id FROM filtres WHERE (deleted_at is NULL OR deleted_at = '') AND type = %s", object_type)
#     conn.commit()
#     users = cur.fetchall()
#     for u in users:
#         print (str(i) + " - " + u["user_id"])
#         f_id = str(uuid.uuid4())[:-2]
#         j = 1
#         for idx, f in enumerate(filtres):
#             filtre_id = f_id
#             if j < 10:
#                 filtre_id += "0"
#             filtre_id += str(j)
#             filtres_r.append((filtre_id, '0', u["user_id"], f["name"], f["label"], object_type, idx, f["default"], '', '0', u["user_id"], u["user_id"]))
#             j += 1
#         i += 1
    


# # Excecute many
# cur.executemany("INSERT INTO filtres (id, account_id, user_id, name, label, type, sort_order, val, color, is_signed, created_by, updated_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", filtres_r)
conn.commit()
conn_close(conn, tunnel)