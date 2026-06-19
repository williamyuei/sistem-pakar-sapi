#!/usr/bin/env python
"""Titik masuk command-line untuk Django."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Tidak dapat mengimpor Django. Pastikan virtual environment aktif "
            "dan Django sudah terinstall."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
