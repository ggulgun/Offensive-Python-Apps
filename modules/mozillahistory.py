#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import os
import Queue

result = Queue.Queue()

def run():
    try:
        for file in os.listdir("~/.mozilla/firefox/"):
            if file.endswith(".default"):
               filename = os.path.join("~/.mozilla/firefox/",file)
               databasefile = filename + "/places.sqlite"
               conn = sqlite3.connect(databasefile)
               curs = conn.cursor()
               for row in curs.execute('SELECT * FROM moz_places'):
                   result.put(row)
               return result
    except Exception as e:
        print e



run()
