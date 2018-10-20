#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import os.path
import Queue

result = Queue.Queue()


def run():
    try:
        filename = "~/.config/google-chrome/Default/History"
        if os.path.isfile(filename) :
               conn = sqlite3.connect(filename)
               curs = conn.cursor()
               for row in curs.execute('SELECT * FROM urls'):
                   result.put(row)
               return result
    except Exception as e:
        print e



run()
