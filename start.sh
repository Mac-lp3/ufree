pg_ctl start -D /usr/local/pgsql/data -l db-logfile

sleep 3

source venv/bin/activate
python main.py