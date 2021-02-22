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

Routines for extracting .xip files (only used by Xcode these days)
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


if __name__ == "__main__":
    print("This is a library of support tools for the Munki Suite.")
