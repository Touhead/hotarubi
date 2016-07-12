#!/usr/bin/env python

import os
import sys
import locale

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotarubi_webapp.settings")
    locale.setlocale(locale.LC_CTYPE, 'japanese')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
