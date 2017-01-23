pg_ctl start -D /usr/local/pgsql/data -l db-logfile

sleep 3

browserify app/app.js -o static/js/bundle.js

source venv/bin/activate
python main.py