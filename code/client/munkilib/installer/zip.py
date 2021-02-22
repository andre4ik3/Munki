# encoding: utf-8
#
# Copyright 2009-2021 Greg Neagle.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
installer.dmg

Created by andre4ik3 on 2021-02-21.

Routines for extracting .zip files
"""
from __future__ import absolute_import, print_function

import os
import shutil
import stat
import subprocess
import tempfile
import xattr

from .. import display
from .. import dmgutils
from .. import osutils
from .. import pkgutils


def remove_quarantine_from_item(some_path):
    """Removes com.apple.quarantine from some_path"""
    try:
        if "com.apple.quarantine" in xattr.xattr(some_path).list(
            options=xattr.XATTR_NOFOLLOW
        ):
            xattr.xattr(some_path).remove(
                "com.apple.quarantine", options=xattr.XATTR_NOFOLLOW
            )
    except BaseException as err:
        display.display_warning(
            "Error removing com.apple.quarantine from %s: %s", some_path, err
        )


def remove_quarantine(some_path):
    """Removes com.apple.quarantine from some_path, recursively"""
    remove_quarantine_from_item(some_path)
    if os.path.isdir(some_path):
        for (dirpath, dirnames, filenames) in os.walk(some_path, topdown=True):
            for filename in filenames:
                remove_quarantine_from_item(os.path.join(dirpath, filename))
            for dirname in dirnames:
                remove_quarantine_from_item(os.path.join(dirpath, dirname))


def ditto_with_progress(source_path, dest_path):
    """Uses ditto to copy an item and provides progress output"""
    source_size = get_size(source_path)
    total_bytes_copied = 0

    cmd = ["/usr/bin/ditto", "-Vxk", "--noqtn", source_path, dest_path]
    proc = subprocess.Popen(
        cmd,
        shell=False,
        bufsize=-1,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    while True:
        output = proc.stdout.readline().decode("UTF-8")
        if not output and (proc.poll() != None):
            break
        words = output.rstrip("\n").split()
        if len(words) > 1 and words[1] == "bytes":
            try:
                bytes_copied = int(words[0])
            except TypeError:
                pass
            else:
                total_bytes_copied += bytes_copied
                display.display_percent_done(total_bytes_copied, source_size)

    return proc.returncode


if __name__ == "__main__":
    print("This is a library of support tools for the Munki Suite.")
