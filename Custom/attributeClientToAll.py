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

values = ["__uninformed__", "__card__", "__check__", "__cash__", "__wire__", "__paypal__", "__mobile__"]
cur.execute("SELECT id, client_id FROM projects p WHERE main_project = '0' AND deleted_at is NULL")
projects = cur.fetchall()
fields_values = []
for project in projects:
  fields_values.append([project["client_id"], project["id"]])
  print(project['client_id'])

sql_query = "UPDATE projects SET client_id = %s WHERE main_project = %s"
cur.executemany(sql_query, fields_values)

conn.commit()

print("Done")
conn_close(conn, tunnel)