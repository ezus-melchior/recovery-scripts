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
    data = requests.get(url).content
    im = Image.open(BytesIO(data))
    return str(len(im.fp.read()))

conn, tunnel = conn_init(env)
cur = conn.cursor()

print("Start")

cur.execute("SELECT id, path_full FROM media")
medias = cur.fetchall()
for media in medias:
    print(get_image_size(media["path_full"]))
    print(media["path_full"])

conn.commit()

print("Done")
conn_close(conn, tunnel)