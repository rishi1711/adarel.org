import flask

from app import app

@app.server.route("/static/ds1.csv")
def serve_ds1():
    return flask.send_file("./raw_data/ds1.csv", mimetype="text")

@app.server.route("/static/ds2.csv")
def serve_ds2():
    return flask.send_file("./raw_data/ds2.csv", mimetype="text")

@app.server.route("/static/ds3.csv")
def serve_ds3():
    return flask.send_file("./raw_data/ds3.csv", mimetype="text")

@app.server.route("/static/ds4.csv")
def serve_ds4():
    return flask.send_file("./raw_data/ds4.csv", mimetype="text")

@app.server.route('/static/2021_DataSet1.xlsx')
def serve_2021_dataset1():
    return flask.send_file("./data2021/2021 data set 1.xlsx", mimetype='text')

