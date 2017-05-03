from pybuilder.core import use_plugin, task
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import connect
import subprocess
import sys
import os
import json

use_plugin('python.core')
use_plugin('python.frosted')

dir_path = os.path.dirname(os.path.realpath(__file__))

config = {}
with open('build_config.json') as json_data_file:
    config = json.load(json_data_file)

def check_db_exists ():
    # check if ufree database exists
    arg_array = ['psql', '-U', config['postgres']['user'], 'ufree', '-W', config['postgres']['passwd']]
    if not config['postgres']['passwd']:
        arg_array = ['psql', '-U', config['postgres']['user'], 'ufree']

    db_exist = subprocess.Popen(
        arg_array,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = db_exist.communicate()
    print(out, err)

    # check output for 'does not exist...' string
    check_string = b'FATAL:  database \"ufree\" does not exist'
    if check_string in out or check_string in err:
        # initialize cluster if found
        print('ufree database not found. creating...')
        create_db = subprocess.Popen(
            ['createdb', '-U', config['postgres']['user'], 'ufree'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, err = create_db.communicate()
        print(out, err)

def check_db_cluster ():
    # get status of the /database directory
    db_status = subprocess.Popen(
        ['pg_ctl', 'status', '-D', './database'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = db_status.communicate()
    print(out, err)

    # check output for 'is not database...' message
    check_string = b'is not a database cluster'
    if check_string in out or check_string in err:
        # initialize cluster if found
        print('Database cluster not found. Initializing...')
        create_db = subprocess.Popen(
            ['pg_ctl', '-D', './database', 'initdb'],
            stdout=subprocess.PIPE
        )
        print(create_db.communicate())
        if create_db.returncode > 0:
            sys.exit()

def start_db ():
    print('Starting database...')
    check_db_cluster()
    port_arg = '\"-p ' + str(config['postgres']['port']) + '\"'
    print('using port: ' + port_arg)
    start_db = subprocess.Popen([
        'pg_ctl',
        '-o',
        port_arg,
        '-D',
        './database',
        '-l',
        './db-logfile',
        'start'
    ], stdin=subprocess.PIPE)
    print(start_db.communicate())
    if start_db.returncode > 0:
        sys.exit()
    check_db_exists()

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
