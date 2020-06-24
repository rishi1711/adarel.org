
needs python 2.7
deploy, change lines in index.py
Flask-Caching==1.7.2


gunicorn index:app.server -b :8080 --daemon


To see the processes is ps ax|grep gunicorn
to kill pkill gunicorn

old : nohup python -u index.py > adarel.out 2>&1 &