#!/usr/bin/python
# -*- coding: utf-8 -*-
import mss
import base64


def run():
    try:
        with mss.mss() as screenshot:
            img = screenshot.grab(screenshot.monitors[0])
        return base64.b64encode(img)
    except Exception as e:
        print e
run()
