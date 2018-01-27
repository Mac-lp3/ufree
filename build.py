from pybuilder.core import use_plugin, task, init
import subprocess
import sys
import os
import json
import builtins

use_plugin('python.core')
use_plugin('python.frosted')

config = {}
dir_path = os.path.dirname(os.path.realpath(__file__))

__spot = ''

def check_db_exists():

    @init
    def initialize(project):
        __spot = project.get_property(t)

    # check if ufree database exists
    print('Checking DB for required tables...')
    if not config['database']['password']:
        print('Password not found. Using default')
        arg_array = [
            'psql',
            '-U',
            config['database']['user'],
            os.environ['DB_NAME']
        ]
    else:
        arg_array = [
            'psql',
            '-U',
            config['database']['user'],
            os.environ['DB_NAME'],
            '-W',
            config['database']['password']
        ]

    print('Using arguments:', arg_array)
    db_exist = subprocess.Popen(
        arg_array,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out = db_exist.stdout.read()
    print('Start script output:', out)
    print('here')

    # check output for 'does not exist...' string
    check_string = str.encode('FATAL:  database \"' + os.environ['DB_NAME'] + '\" does not exist')
    if check_string in out:
        # initialize cluster if found
        print('Database not found. creating...')
        create_db = subprocess.Popen(
            ['createdb', '-U', config['database']['user'], os.environ['DB_NAME']],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, err = create_db.communicate()
        print(out, err)

    print('Check complete')

def check_db_cluster():
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

def start_db_server():
    print('Starting database...')
    check_db_cluster()
    port_arg = '-p ' + str(config['database']['port'])
    print('using port: ' +  str(config['database']['port']))
    start_db = subprocess.Popen(
        [
            'pg_ctl',
            '-o',
            '"' + port_arg + '"',
            '-D',
            './database',
            '-l',
            './db-logfile',
            'start'
        ],
        shell=True,
        stdin=subprocess.PIPE
    )
    print('Start-up message:', start_db.communicate())
    if start_db.returncode > 0:
        print('return code > 0. exiting.')
        sys.exit()

def stop_db():
    proc = subprocess.Popen(
        ['pg_ctl', 'stop'],
        stdin=subprocess.PIPE
    )
    print(proc.communicate())
    if proc.returncode > 0:
        sys.exit()

def build_client():
    prefix = os.path.join(dir_path, 'client')
    print(os.environ['PATH'])
    proc = subprocess.Popen(
        ['npm', '--prefix', prefix, 'run', 'build'],
        shell=True,
        stdout=subprocess.PIPE
    )
    print(proc.communicate())
    if proc.returncode > 0:
        sys.exit()

def start_app_server():
    print('starting the application server...')
    main_path = os.path.join(dir_path, 'main.py')
    print('starting ' + main_path)
    os.system('python ' + main_path)
    subprocess.call(
        ['python', main_path],
        shell=True,
        stdin=subprocess.PIPE
    )
    print(proc.communicate())
    if proc.returncode > 0:
        sys.exit()

def load_config():
    global config
    if os.environ['ENV'] != 'production':
        print('Loading dev configuration')
        with open('build_config_dev.json') as json_data_file:
            config = json.load(json_data_file)
    else:
        print('Loading production configuration')
        with open('build_config_prod.json') as json_data_file:
            config = json.load(json_data_file)

    # populate environment vars
    os.environ['TEST_DB_FAIL'] = 'False'
    os.environ['DAOS_PACKAGE'] = config['daoPackage']
    os.environ['FILTERS_PACKAGE'] = config['filterPackage']
    os.environ['SERVICES_PACKAGE'] = config['daoPackage']
    os.environ['VALIDATORS_PACKAGE'] = config['validatorPackage']
    os.environ['PSYCOPG2_PACKAGE'] = config['psycopg2Package']
    os.environ['DB_NAME'] = config['database']['name']

@task(description='pyb -P t="eventDao_test.py"')
def spot():
    os.environ['ENV'] = 'test'
    load_config()
    proc = subprocess.Popen(
        ['nosetests', '-v', '--tests=test\\{0}'.format(__spot)],
        shell=True,
        stdout=subprocess.PIPE
    )
    print(proc.communicate())

@task(description='Uses Nose to run all unit tests')
def test():
    os.environ['ENV'] = 'test'
    os.environ['TEST_DB_FAIL'] = 'False'
    load_config()
    #os.environ['DB_NAME'] = 'ufree_test'
    proc = subprocess.Popen(
        ['nosetests', '-v'],
        shell=True,
        stdout=subprocess.PIPE
    )
    print(proc.communicate())

@task(description='Compiles client-side code')
def build():
    print('Building client side code...')
    build_client()

@task(description='Starts the database and app server in production mode')
def start():
    os.environ['ENV'] = 'production'
    load_config()
    start_db_server()
    check_db_exists()
    start_app_server()

@task(description='Starts the database and app server in development mode')
def start_dev():
    os.environ['ENV'] = 'development'
    load_config()
    start_db_server()
    check_db_exists()
    start_app_server()
