from pybuilder.core import use_plugin, task
import subprocess
import sys

use_plugin("python.core")

def start_db ():
    proc = subprocess.Popen(
        ['pg_ctl', 'start', '-D', '/usr/local/pgsql/data', '-l', 'db-logfile'],
        stdin=subprocess.PIPE
    )
    print(proc.communicate())
    if proc.returncode > 0:
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
    proc = subprocess.Popen(
        ['python3.5', 'main.py'],
        stdin=subprocess.PIPE
    )
    print(proc.communicate())
    if proc.returncode > 0:
        sys.exit()

@task(description='''
    Starts the database, builds client-side code, and starts the server
''')
def start_stack ():
    start_db()
    build_client()
    start_server()
