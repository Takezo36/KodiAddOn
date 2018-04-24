# -*- coding: utf8 -*-

# Copyright (C) 2018 - Benjamin Hebgen
# This program is Free Software see LICENSE file for details

import sys
import subprocess
if (__name__ == "__main__"):
  subprocess.call(sys.argv[1:-1])
  subprocess.Popen(sys.argv[-1:])

