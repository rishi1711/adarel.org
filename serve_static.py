import flask
from app import app

import tool.datapathscsv as dpcsv

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

# @app.server.route('/static/2021_DataSet1.xlsx')
# def serve_2021_dataset1():
#     return flask.send_file("./data2021/2021 data set 1.xlsx", mimetype='text')
@app.server.route('/2021data/<dataset_name>')
def download_2021dataset(dataset_name):
    path = dpcsv.META_DATA_CSV[dataset_name]['path']
    return flask.send_file(path)


@app.server.route('/2021data/mae_dist_fig/<dataset_name>')
def get_mae_fig(dataset_name):
    path = dpcsv.META_DATA_CSV[dataset_name].get('mae_dist_fig_path', None)
    if path:
        return flask.send_file(path)
