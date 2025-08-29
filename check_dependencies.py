#!/usr/bin/env python3
"""
Dependency checker for DankMemer/imgen
Run this script to verify all dependencies are properly installed.
"""

import sys
import subprocess

def check_python_package(package_name, import_name=None):
    """Check if a Python package is installed and importable."""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✓ {package_name} - OK")
        return True
    except ImportError:
        print(f"✗ {package_name} - MISSING")
        return False

def check_system_command(command):
    """Check if a system command is available."""
    try:
        subprocess.run([command, '--version'], capture_output=True, check=True)
        print(f"✓ {command} - OK")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"✗ {command} - MISSING")
        return False

def main():
    print("DankMemer/imgen Dependency Check")
    print("=" * 40)
    
    all_good = True
    
    print("\n1. Checking Python packages...")
    python_packages = [
        ('flask', 'flask'),
        ('pillow', 'PIL'),
        ('requests', 'requests'),
        ('wand', 'wand'),
        ('rethinkdb', 'rethinkdb'),
        ('requests_oauthlib', 'requests_oauthlib'),
        ('sentry_sdk', 'sentry_sdk'),
        ('blinker', 'blinker'),
        ('moviepy', 'moviepy'),
        ('redis', 'redis'),
        ('numpy', 'numpy'),
        ('keras', 'keras'),
        ('scipy', 'scipy'),
        ('gevent', 'gevent'),
        ('tensorflow', 'tensorflow'),
        ('gunicorn', 'gunicorn'),
    ]
    
    for package, import_name in python_packages:
        if not check_python_package(package, import_name):
            all_good = False
    
    print("\n2. Checking optional packages...")
    optional_packages = [
        ('ujson', 'ujson'),
        ('hiredis', 'hiredis'),
        ('pillow-simd', None),  # Can't easily test import name
    ]
    
    for package, import_name in optional_packages:
        if import_name:
            check_python_package(package, import_name)
    
    print("\n3. Checking system commands...")
    system_commands = ['convert', 'gm', 'ffmpeg', 'rethinkdb', 'redis-cli']
    
    for command in system_commands:
        if not check_system_command(command):
            if command in ['convert', 'gm']:
                print("  Note: ImageMagick/GraphicsMagick required for image processing")
            elif command == 'ffmpeg':
                print("  Note: FFmpeg required for video processing endpoints")
            elif command == 'rethinkdb':
                print("  Note: RethinkDB required for database")
                all_good = False
            elif command == 'redis-cli':
                print("  Note: Redis required for caching and rate limiting")
                all_good = False
    
    print("\n4. Checking configuration...")
    try:
        import json
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        required_keys = ['client_id', 'client_secret', 'admins', 'rdb_address', 'rdb_port', 'rdb_db']
        for key in required_keys:
            if key in config:
                print(f"✓ config.json has {key}")
            else:
                print(f"✗ config.json missing {key}")
                all_good = False
    except FileNotFoundError:
        print("✗ config.json not found")
        all_good = False
    except json.JSONDecodeError:
        print("✗ config.json is not valid JSON")
        all_good = False
    
    print("\n" + "=" * 40)
    if all_good:
        print("✓ All critical dependencies check passed!")
        print("You can now start the application with: ./start.sh")
    else:
        print("✗ Some dependencies are missing.")
        print("Please install missing packages before starting the application.")
        sys.exit(1)

if __name__ == '__main__':
    main()