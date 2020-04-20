#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import googlemaps
from datetime import datetime
import json

gmaps = googlemaps.Client(key='AIzaSyBq2e1RFVCsanHx0kFd-h1GsBegV6ez4XA')

for line in open('tkystatnames2.txt', 'r'):

    dist_json_resp  = gmaps.distance_matrix(line, '渋谷駅')

    try:

        print("'" + line.rstrip('\n') + "'" + ':' + "'" + str(dist_json_resp["rows"][0]["elements"][0]["duration"]["value"] / 60) + "',\n")

    except:

        print(line)
