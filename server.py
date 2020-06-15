from waitress import serve
from app import server #so "app" is the name of my Dash script I want to serve
import flask
serve(server, host="0.0.0.0", port="8080")

#sudo nohup python serve.py > log.txt 2>&1 &
#21704

#22503


# As of now, change the line iN indedex.py