#!/usr/bin/env python
"""
durga.py — Dev runner for taxessaver
Usage: python durga.py
"""
import os
import sys
import subprocess


def run():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

    # Clear Python cache
    subprocess.run(['find', '.', '-type', 'd', '-name', '__pycache__',
                    '-exec', 'rm', '-rf', '{}', '+'], capture_output=True)

    # Build Tailwind CSS
    print("Building Tailwind CSS...")
    subprocess.run(['npx', 'tailwindcss', '-i', './static/css/input.css',
                    '-o', './static/css/output.css'], check=False)

    # Run Django dev server
    print("\nStarting Django server at http://127.0.0.1:8000/")
    print("Admin: http://127.0.0.1:8000/sd/ | username: admin | password: admin123\n")
    os.execv(sys.executable, [sys.executable, 'manage.py', 'runserver'])


if __name__ == '__main__':
    run()
