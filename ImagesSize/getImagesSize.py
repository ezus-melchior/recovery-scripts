# -*- coding: utf-8 -*-
from db_utils import conn_init, conn_close
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

#### VARIABLE #####
env ="esus_dev"
#### END OFVARIABLE #####
def get_image_size(url):
    try:
        data = requests.get(url).content
        im = Image.open(BytesIO(data))
        return str(len(im.fp.read()))
    except:
        return -1

conn, tunnel = conn_init(env)
cur = conn.cursor()

print("Start")

cur.execute("SELECT DISTINCT path_full FROM media_activities WHERE deleted_at is NULL AND size is NULL")
medias = cur.fetchall()
size_values = []
for media in medias:
    size_values.append([get_image_size(media["path_full"]), media["path_full"]])
sql_query = "UPDATE media_activities SET size = %s WHERE path_full = %s"
cur.executemany(sql_query, size_values)
cur.execute("SELECT DISTINCT path_full FROM media WHERE deleted_at is NULL AND size is NULL")
medias = cur.fetchall()
size_values = []
for media in medias:
    size_values.append([get_image_size(media["path_full"]), media["path_full"]])
sql_query = "UPDATE media SET size = %s WHERE path_full = %s"
cur.executemany(sql_query, size_values)

conn.commit()

print("Done")
conn_close(conn, tunnel)