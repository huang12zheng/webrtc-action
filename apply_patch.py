import subprocess
import json
import logging
import os
import urllib.parse
import zipfile
import tarfile
import shutil
import platform
import argparse
import collections
import re
from typing import Optional, Dict, List


class ChangeDirectory(object):
    def __init__(self, cwd):
        self._cwd = cwd

    def __enter__(self):
        self._old_cwd = os.getcwd()
        logging.debug(f'pushd {self._old_cwd} --> {self._cwd}')
        os.chdir(self._cwd)

    def __exit__(self, exctype, excvalue, trace):
        logging.debug(f'popd {self._old_cwd} <-- {self._cwd}')
        os.chdir(self._old_cwd)
        return False


def cmd(args, **kwargs):
    logging.debug(f'+{args} {kwargs}')
    if 'check' not in kwargs:
        kwargs['check'] = True
    if 'resolve' in kwargs:
        resolve = kwargs['resolve']
        del kwargs['resolve']
    else:
        resolve = True
    if resolve:
        args = [shutil.which(args[0]), *args[1:]]
    return subprocess.run(args, **kwargs)
    return


def apply_patch(patch, dir='webrtc-build', depth=1):
    with ChangeDirectory(dir):
        if platform.system() == 'Windows':
            cmd(['git', 'apply', f'-p{depth}',
                '--ignore-space-change', '--ignore-whitespace', '--whitespace=nowarn',
                 patch])
        else:
            with open(patch) as stdin:
                cmd(['patch', f'-p{depth}'], stdin=stdin)


if __name__ == '__main__':
    for patch in [
        'patch_min2',
        'faster_clone',
        'container_preparations_advance',
        'fix_window_scriptinvocationpath_error',
        # 'translation_into_english',
    ]:
        apply_patch(f'../{patch}.patch')
