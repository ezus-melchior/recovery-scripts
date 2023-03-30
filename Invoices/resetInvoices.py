# -*- coding: utf-8 -*-
from db_utils import conn_init, conn_close
import pandas as pd
import uuid

#### VARIABLE #####
env ="esus_dev"
#### END OFVARIABLE #####

conn, tunnel = conn_init(env)
cur = conn.cursor()

print("Start")

cur.execute("SELECT id FROM accounts")
accounts = cur.fetchall()
fields_values_r = []
values = ["__uninformed__", "__card__", "__check__", "__cash__", "__wire__", "__paypal__", "__mobile__"]
for index, item in enumerate(values):
  cur.execute("UPDATE templates_settings SET value = %s WHERE value = %s AND field = 'payment_method'", (item, str(index)))
  cur.execute("UPDATE invoices SET payment_method = %s WHERE payment_method = %s", (item, index))
  cur.execute("SELECT accounts.id, fields.id AS fieldId FROM esus_dev.fields fields LEFT JOIN esus_dev.accounts accounts ON fields.account_id = accounts.id WHERE fields.name = %s AND fields.deleted_at is NULL AND fields.object_type = 'payment_means' GROUP BY accounts.id", item)
  res = cur.fetchall()
  for account in accounts:
    exist = 0
    for r in res:
      if r['id'] == account['id']:
        exist = 1
    if exist == 0:
      field_id = str(uuid.uuid4())
      fields_values_r.append(field_id, account['id'], '0', 'text', 'payment_means', item, item)
      if index == 0:
        cur.execute("UPDATE deposits SET payment_mean = %s WHERE payment_mean = %s", (field_id, str(index)))
    else:
      if index == 0:
        cur.execute("UPDATE deposits SET payment_mean = %s WHERE payment_mean = %s", (r["fieldId"], str(index)))

sql_query = "INSERT INTO fields (id, account_id, family_id, type, object_type, name, technical_name, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())"
cur.executemany(sql_query, fields_values_r)

conn.commit()

print("Done")
conn_close(conn, tunnel)