
# adarel.org
This is a dash & flask based app. 
needs python 3.8+

## Development
Do let me know if docker method has some features missing. as of now, it is literally mounted as a internal filesystem in the docker container.
### Docker

We do not need to restart the docker compose after every change. Any change made in the file should reflect automatically! 
```
docker-compose --profile dev up --build     
```

### Native
Just in case you want to give this a shot.

- Create a new Anaconda environment. 
- Install requirements.; No way the requirements.txt is complete! If something is not installed, you will see the error & just install that using pip! 
- numpy, pandas etc etc too.
- I know that to serve static conrtent, we should use `serve_directory` or even better `nginx` but this is a TODO. for now, we use serve_static file. [refererece if you have time](https://stackoverflow.com/a/20648053/3262852)

```python 
python index.py
```
## Production
```

docker-compose --profile prod up --build 
```

### Dont know why i had this earlier.
gunicorn index:app.server -b :8080 --daemon


To see the processes is ps ax|grep gunicorn
to kill pkill gunicorn

old : nohup python -u index.py > adarel.out 2>&1 &