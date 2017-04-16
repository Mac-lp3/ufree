pg_ctl start -D /usr/local/pgsql/data -l db-logfile
npm --prefix client/ run build

source venv/bin/activate
python3.5 main.py
