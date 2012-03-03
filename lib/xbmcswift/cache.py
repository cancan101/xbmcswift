import os
try:
    import json
except ImportError:
    import simplejson as json
import time
from datetime import datetime
from xbmcswift import xbmc


def put_cached_data(contents, filename, timestamp_fn):
    '''Writes contents to filename and writes time.time() to timestamp_fn'''
    file = open(filename, 'w')
    file.write(contents)
    file = open(timestamp_fn, 'w')
    file.write('%d' % time.time())

def put_cached_data_as_json(contents, filename, timestamp_fn):
    put_cached_data(json.dumps(contents), filename, timestamp_fn)

def get_cached_data(json_fn, timestamp_fn, TTL):
    '''Returns a JSON object from json_fn if json_fn exists and if the
    timestamp in timestamp_fn is not older than TTL. Returns None if cache
    isn't valid for any reason.
    '''
    if not os.path.exists(json_fn):
        xbmc.log('Missing XBMC Swift cache file at %s' % json_fn)
        return None

    if not os.path.exists(timestamp_fn):
        xbmc.log('Missing XBMC Swift cache timestamp file at %s' % timestamp_fn)
        return None

    now = datetime.utcnow()
    file = open(timestamp_fn)
    timestamp = datetime.utcfromtimestamp(float(file.read()))

    if now - timestamp > TTL:
        xbmc.log('XBMC Swift cache file is older than TTL.')
        return None

    file = open(json_fn)
    xbmc.log('Returning XBMC Swift from cache.')
    return json.load(file)
