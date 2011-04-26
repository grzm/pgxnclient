"""
pgxn.client -- network interaction
"""

# Copyright (C) 2011 Daniele Varrazzo

# This file is part of the PGXN client

import os
import urllib2
from itertools import count

from pgxn.client import __version__
from pgxn.client.i18n import _
from pgxn.client.errors import NetworkError, ResourceNotFound, BadRequestError

import logging
logger = logging.getLogger('pgxn.client.network')

def get_file(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'pgxn.client/%s' % __version__)]
    logger.debug('opening url: %s', url)
    try:
        return opener.open(url)
    except urllib2.HTTPError, e:
        if e.code == 404:
            raise ResourceNotFound(_("resource not found"))
        elif e.code == 400:
            raise BadRequestError(_("bad request on '%s'") % e.url)
        elif e.code == 500:
            raise NetworkError(_("server error"))
        elif e.code == 503:
            raise NetworkError(_("service unavailable"))
        else:
            raise NetworkError(_("unexpected response %d for '%s'")
                % (e.code, e.url))

def download(f, fn, rename=True):
    """Download a file locally.

    :param f: open file read
    :param fn: name of the file to write
    :param rename: if true and a file *fn* exist, rename the downloaded file
        adding a prefix ``-1``, ``-2``... before the extension.
    
    Return the name of the file saved.
    """
    if rename:
        if os.path.exists(fn):
            base, ext = os.path.splitext(fn)
            for i in count(1):
                logger.debug(_("file %s exists"), fn)
                fn = "%s-%d%s" % (base, i, ext)
                if not os.path.exists(fn):
                    break

    logger.info(_("saving %s"), fn)
    fout = open(fn, "wb")
    try:
        while 1:
            data = f.read(8192)
            if not data: break
            fout.write(data)
    finally:
        fout.close()

    return fn

