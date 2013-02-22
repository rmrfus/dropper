#!/usr/bin/env python

import sys
import os
import shutil
import subprocess

from md5 import md5
from datetime import datetime
from socket import gethostname
from random import randint


cfg = {
    'public_folder':     '%s/Dropbox/Public' % (os.environ['HOME']),
    'dropdrop_suffix':   'DD',
    'public_user_id':    '588290',
}


def getrandhex():
    '''
        returns some random md5 string
    '''
    md = md5()
    md.update(str(randint(0, 1e100)))
    md.update(str(datetime.now()))
    md.update(str(randint(0, 1e100)))
    md.update(gethostname())
    md.update(str(randint(0, 1e100)))
    return md.hexdigest()


def expand_filelist(filelist):
    '''
        removes unreadable/non-existing files, symlinks, etc
    '''
    output = []
    for l in filelist:
        l = l.strip()
        if not os.path.exists(l):
            continue
        if os.path.isfile(l):
            try:
                with open(l):
                    pass
            except IOError:
                continue
            output.append(l)
        if os.path.isdir(l):
            output.append(l)
    return output


def find_good_wd(filelist):
    '''
        Looking for common path for supplied filepathes in list
    '''

    last_slash_pos = 0
    good_wd = '/'

    while True:
        slash_pos = filelist[0].find('/', last_slash_pos + 1)
        if slash_pos == last_slash_pos or slash_pos < 0:
            break

        test_wd = filelist[0][:slash_pos]
        success = True

        for f in filelist:
            if f.find(test_wd, 0) < 0:
                success = False
                break

        if success:
            last_slash_pos = slash_pos
            good_wd = test_wd
        else:
            break

    if not good_wd.endswith('/'):
        good_wd += "/"

    return good_wd


def zip_files(zip_file, filelist):
    good_wd = find_good_wd(filelist)
    p = subprocess.Popen(["/bin/sh", "-c",
            "cd %s && /usr/bin/zip -rq@ %s" % (good_wd, zip_file)],
            stdin=subprocess.PIPE)
    feed = "%s\n" % ("\n".join([l[len(good_wd):] for l in filelist]))
    p.communicate(input=feed)
    p.wait()


def main():

    inpoot = sys.stdin.readlines()
    filelist = expand_filelist(inpoot)

    if len(filelist) == 0:
        sys.exit(-1)

    randhex = getrandhex()
    dropdir = os.path.join(
        cfg['public_folder'], cfg['dropdrop_suffix'], randhex)
    dropurl = "https://dl.dropbox.com/u/%s/%s/%s" % (
        cfg['public_user_id'], cfg['dropdrop_suffix'], randhex)

    filename = os.path.basename(filelist[0])

    os.makedirs(dropdir)

    if len(filelist) == 1 and os.path.isfile(filelist[0]):
        shutil.copy(filelist[0], os.path.join(dropdir, filename))
    else:
        filename = 'archive.zip'
        zip_files(os.path.join(dropdir, filename), filelist)

    print("%s/%s" % (dropurl, filename))


if __name__ == "__main__":
    main()
