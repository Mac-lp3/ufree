from pybuilder.core import use_plugin, task
import subprocess
import sys
import os

use_plugin("python.core")
dir_path = os.path.dirname(os.path.realpath(__file__))

def start_db ():
    db_status = subprocess.Popen(
        ['pg_ctl', 'status', '-D', './database'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    out, err = db_status.communicate()
    check_string = b'is not a database cluster'

    if check_string in out or check_string in err:
        print('Database not found. Initializing...')
        create_db = subprocess.Popen(
            ['pg_ctl', '-D', './database', 'initdb'],
            stdout=subprocess.PIPE
        )
        print(create_db.communicate())
        if create_db.returncode > 0:
            sys.exit()

    print('Starting database...')
    start_db = subprocess.Popen(
        ['pg_ctl', 'start', '-D', './database', '-l', './db-logfile'],
        stdin=subprocess.PIPE
    )
    print(start_db.communicate())
    if start_db.returncode > 0:
        sys.exit()

def stop_db ():
    proc = subprocess.Popen(
        ['pg_ctl', 'stop'],
        stdin=subprocess.PIPE
    )
    print(proc.communicate())
    if proc.returncode > 0:
        sys.exit()

def build_client ():
    proc = subprocess.Popen(
        ['npm', '--prefix', 'client/', 'run', 'build'],
        stdin=subprocess.PIPE
    )
    print(proc.communicate())
    if proc.returncode > 0:
        sys.exit()

def start_server ():
    main_path = os.path.join(dir_path, 'main.py')
    print('starting ' + main_path)
    proc = subprocess.Popen(
        ['python', main_path],
        stdin=subprocess.PIPE
    )
    print(proc.communicate())
    if proc.returncode > 0:
        sys.exit()

@task(description='''
    Starts the database, builds client-side code, and starts the server
''')
def build_and_start ():
    start_db()
    build_client()
    start_server()

@task(description='''
    Starts the database and server
''')
def start ():
    start_db()
    start_server()
