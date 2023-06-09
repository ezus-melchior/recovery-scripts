# -*- coding: utf-8 -*-
import time
from db_utils import conn_init, conn_close
import requests
import time
from PIL import Image
from io import BytesIO

#### VARIABLE #####
env ="esus_dev"
LIMIT = "100"
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
start_time = time.time()
has_media, i = True, 1
while has_media is True:
    cur.execute("SELECT id, value FROM brands WHERE deleted_at is NULL AND (size = -2 OR size is NULL) AND (field = 'logo' OR field = 'photo' OR field = 'favicon') ORDER BY created_at DESC LIMIT " + LIMIT)
    medias = cur.fetchall()
    has_media = True if len(medias) > 0 else False
    if has_media is True:
        print (f"batch brands {i}")
        size_values = []
        for media in medias:
            size_values.append([get_image_size(media["value"]), media["id"]])
        print("--- before update %s seconds ---" % (time.time() - start_time))
        sql_query = "UPDATE brands SET size = %s WHERE id = %s"
        cur.executemany(sql_query, size_values)
        conn.commit()
        print("--- after update %s seconds ---" % (time.time() - start_time))
        i += 1

has_media, i = True, 1
while has_media is True:
    cur.execute("SELECT id, favicon_path FROM accounts WHERE deleted_at is NULL AND (favicon_size = -2 OR favicon_size is NULL) ORDER BY created_at DESC LIMIT " + LIMIT)
    medias = cur.fetchall()
    has_media = True if len(medias) > 0 else False
    if has_media is True:
        print (f"batch favicon_path accounts {i}")
        size_values = []
        for media in medias:
            size_values.append([get_image_size(media["logo_path"]), media["id"]])
        print("--- before update %s seconds ---" % (time.time() - start_time))
        sql_query = "UPDATE accounts SET favicon_size = %s WHERE id = %s"
        cur.executemany(sql_query, size_values)
        conn.commit()
        print("--- after update %s seconds ---" % (time.time() - start_time))
        i += 1

has_media, i = True, 1
while has_media is True:
    cur.execute("SELECT id, logo_path FROM accounts WHERE deleted_at is NULL AND (logo_size = -2 OR logo_size is NULL) ORDER BY created_at DESC LIMIT " + LIMIT)
    medias = cur.fetchall()
    has_media = True if len(medias) > 0 else False
    if has_media is True:
        print (f"batch logo_path accounts {i}")
        size_values = []
        for media in medias:
            size_values.append([get_image_size(media["logo_path"]), media["id"]])
        print("--- before update %s seconds ---" % (time.time() - start_time))
        sql_query = "UPDATE accounts SET logo_size = %s WHERE id = %s"
        cur.executemany(sql_query, size_values)
        conn.commit()
        print("--- after update %s seconds ---" % (time.time() - start_time))
        i += 1

has_media, i = True, 1
while has_media is True:
    cur.execute("SELECT id, favicon_path FROM accounts WHERE deleted_at is NULL AND (logo_size = -2 OR logo_size is NULL) ORDER BY created_at DESC LIMIT " + LIMIT)
    medias = cur.fetchall()
    has_media = True if len(medias) > 0 else False
    if has_media is True:
        print (f"batch favicon_path accounts {i}")
        size_values = []
        for media in medias:
            size_values.append([get_image_size(media["favicon_path"]), media["id"]])
        print("--- before update %s seconds ---" % (time.time() - start_time))
        sql_query = "UPDATE accounts SET favicon_size = %s WHERE id = %s"
        cur.executemany(sql_query, size_values)
        conn.commit()
        print("--- after update %s seconds ---" % (time.time() - start_time))
        i += 1

has_media, i = True, 1
while has_media is True:
    cur.execute("SELECT id, photo_path FROM users WHERE deleted_at is NULL AND (photo_size = -2 OR photo_size is NULL) ORDER BY created_at DESC LIMIT " + LIMIT)
    medias = cur.fetchall()
    has_media = True if len(medias) > 0 else False
    if has_media is True:
        print (f"batch photo_path users {i}")
        size_values = []
        for media in medias:
            size_values.append([get_image_size(media["photo_path"]), media["id"]])
        print("--- before update %s seconds ---" % (time.time() - start_time))
        sql_query = "UPDATE users SET photo_size = %s WHERE id = %s"
        cur.executemany(sql_query, size_values)
        conn.commit()
        print("--- after update %s seconds ---" % (time.time() - start_time))
        i += 1

print("Done")
conn_close(conn, tunnel)